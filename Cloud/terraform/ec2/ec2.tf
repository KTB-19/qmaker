locals {
  common_tags = {
    Project     = "ktb-qmaker"
    Owner       = "Cloud-Team-Bryan"
    CreatedBy   = "Terraform"
    CreatedDate = formatdate("YYYY-MM-DD", timestamp())
  }
}# EC2 인스턴스를 위한 보안 그룹 생성
resource "aws_security_group" "backend_sg" {
  vpc_id = var.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 9100
    to_port     = 9100
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 9090
    to_port     = 9090
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, {
    Name = "ktb-qmaker-backend-sg"
  })
}

resource "aws_security_group" "python_sg" {
  vpc_id = var.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 9100
    to_port     = 9100
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 9090
    to_port     = 9090
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, {
    Name = "ktb-qmaker-python-sg"
  })
}

# Backend용 ALB 생성
resource "aws_lb" "backend_alb" {
  name               = "backend-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = var.public_subnets

  tags = merge(local.common_tags, {
    Name = "ktb-qmaker-backend-alb"
  })
}

resource "aws_lb_target_group" "backend_tg" {
  name        = "backend-tg"
  port        = 8080
  protocol    = "HTTP"
  vpc_id      = var.vpc_id

  health_check {
    path                = "/health"
    protocol            = "HTTP"
    matcher             = "200-299"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 3
    unhealthy_threshold = 3
  }
}

resource "aws_lb_listener" "backend_listener" {
  load_balancer_arn = aws_lb.backend_alb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.backend_tg.arn
  }
}

# ALB를 위한 보안 그룹 생성
resource "aws_security_group" "alb" {
  vpc_id = var.vpc_id
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "moive-${terraform.workspace}-sg-alb"
  }
}

# Backend용 EC2 인스턴스 생성 (각 AZ에 하나씩)
resource "aws_instance" "backend_instances" {
  count         = 2
  ami           = "ami-0c2acfcb2ac4d02a0" # Amazon Linux 2 AMI (최신 확인 필요)
  instance_type = "t2.small"
  subnet_id     = element(var.private_subnets, count.index)
  key_name = "kakao-tech-bootcamp"
  security_groups = [aws_security_group.backend_sg.id]
  private_ip    = lookup({
    0 = "10.0.3.222"
    1 = "10.0.4.16"
  }, count.index)

  tags = merge(local.common_tags, {
    Name = "ktb-qmaker-backend-instance-${count.index}"
  })
}

# Backend 인스턴스를 Backend ALB Target Group에 연결
resource "aws_lb_target_group_attachment" "backend_tg_attachment" {
  count            = 2
  target_group_arn = aws_lb_target_group.backend_tg.arn
  target_id        = aws_instance.backend_instances[count.index].id
  port             = 8080
}


# Python용 EC2 인스턴스 생성 (각 AZ에 하나씩)
resource "aws_instance" "python_instances" {
  count         = 2
  ami           = "ami-0c2acfcb2ac4d02a0"  # Amazon Linux 2 AMI (최신 확인 필요)
  instance_type = "t3.small"
  key_name = "kakao-tech-bootcamp"
  subnet_id     = element(var.private_subnets, count.index)
  security_groups = [aws_security_group.python_sg.id]
  private_ip    = lookup({
    0 = "10.0.3.224"
    1 = "10.0.4.152"
  }, count.index)

  tags = merge(local.common_tags, {
    Name = "ktb-qmaker-ai-instance-${count.index}"
  })
}

# Qmaker-Dev-Host 인스턴스 생성
resource "aws_instance" "qmaker_dev_host" {
  ami           = "ami-05d768df76a2b8bd8" # Amazon Linux 2 AMI (최신 확인 필요)
  instance_type = "t3.small"
  subnet_id     = var.public_subnets[0] # 퍼블릭 서브넷 중 하나에 배치
  security_groups = [aws_security_group.backend_sg.id]

  tags = merge(local.common_tags, {
    Name = "ktb-qmaker-dev-host"
  })
}

# DB 인스턴스 생성
resource "aws_instance" "db_instance" {
   ami           = "ami-05d768df76a2b8bd8"
   instance_type = "t3.small"
   subnet_id     = var.db_subnets[0]
   security_groups = [aws_security_group.db_sg.id]
   private_ip    = "10.0.5.12"
   key_name = "kakao-tech-bootcamp"

   tags = merge(local.common_tags, {
    Name = "ktb-qmaker-db-host"
  })
}

resource "aws_security_group" "db_sg" {
  vpc_id = var.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 27017
    to_port     = 27017
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 9100
    to_port     = 9100
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 9090
    to_port     = 9090
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, {
    Name = "ktb-qmaker-db-sg"
  })
}