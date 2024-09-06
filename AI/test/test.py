#%%
import json

from app.services.question_maker import category_question_generation,question_categorize,question_generation
import asyncio

# 비동기 함수 호출


# 동기식으로 비동기 함수 실행


testtxt = '''토큰화(Tokenization)
자연어 처리에서 크롤링 등으로 얻어낸 코퍼스 데이터가 필요에 맞게 전처리되지 않은 상태라면, 해당 데이터를 사용하고자하는 용도에 맞게 토큰화(tokenization) & 정제(cleaning) & 정규화(normalization)하는 일을 하게 됩니다. 이번에는 그 중에서도 토큰화에 대해서 학습합니다.
주어진 코퍼스(corpus)에서 토큰(token)이라 불리는 단위로 나누는 작업을 토큰화(tokenization)라고 합니다. 토큰의 단위가 상황에 따라 다르지만, 보통 의미있는 단위로 토큰을 정의합니다. 여기서는 토큰화에 대한 발생할 수 있는 여러가지 상황에 대해서 언급하여 토큰화에 대한 개념을 이해합니다. 이어서 NLTK, KoNLPY를 통해 실습을 진행하며 토큰화를 수행합니다.
    1) 단어 토큰화(Word Tokenization)
토큰의 기준을 단어(word)로 하는 경우, 단어 토큰화(word tokenization)라고 합니다. 다만, 여기서 단어(word)는 단어 단위 외에도 단어구, 의미를 갖는 문자열로도 간주되기도 합니다.
예를 들어보겠습니다. 아래의 입력으로부터 구두점(punctuation)과 같은 문자는 제외시키는 간단한 단어 토큰화 작업을 해봅시다. 구두점이란 마침표(.), 컴마(,), 물음표(?), 세미콜론(;), 느낌표(!) 등과 같은 기호를 말합니다.
입력: Time is an illusion. Lunchtime double so!
이러한 입력으로부터 구두점을 제외시킨 토큰화 작업의 결과는 다음과 같습니다.
출력 : "Time", "is", "an", "illustion", "Lunchtime", "double", "so"
이 예제에서 토큰화 작업은 굉장히 간단합니다. 구두점을 지운 뒤에 띄어쓰기(whitespace)를 기준으로 잘라냈습니다. 하지만 이 예제는 토큰화의 가장 기초적인 예제를 보여준 것에 불과합니다.
보통 토큰화 작업은 단순히 구두점이나 특수문자를 전부 제거하는 정제(cleaning) 작업을 수행하는 것만으로 해결되지 않습니다. 구두점이나 특수문자를 전부 제거하면 토큰이 의미를 잃어버리는 경우가 발생하기도 합니다. 심지어 띄어쓰기 단위로 자르면 사실상 단어 토큰이 구분되는 영어와 달리, 한국어는 띄어쓰기만으로는 단어 토큰을 구분하기 어렵습니다. 그 이유는 뒤에서 언급하겠습니다.
언어 모델(Language Model)이란?
언어 모델(Language Model, LM)은 언어라는 현상을 모델링하고자 단어 시퀀스(문장)에 확률을 할당(assign)하는 모델입니다.
언어 모델을 만드는 방법은 크게는 통계를 이용한 방법과 인공 신경망을 이용한 방법으로 구분할 수 있습니다. 최근에는 통계를 이용한 방법보다는 인공 신경망을 이용한 방법이 더 좋은 성능을 보여주고 있습니다. 최근 핫한 자연어 처리의 기술인 GPT나 BERT 또한 인공 신경망 언어 모델의 개념을 사용하여 만들어졌습니다. 이번 챕터에서는 언어 모델의 개념과 언어 모델의 전통적 접근 방식인 통계적 언어 모델에 대해서 배웁니다.
언어 모델(Language Model)
언어 모델은 단어 시퀀스에 확률을 할당(assign) 하는 일을 하는 모델입니다. 이를 조금 풀어서 쓰면, 언어 모델은 가장 자연스러운 단어 시퀀스를 찾아내는 모델입니다. 단어 시퀀스에 확률을 할당하게 하기 위해서 가장 보편적으로 사용되는 방법은 언어 모델이 이전 단어들이 주어졌을 때 다음 단어를 예측하도록 하는 것입니다.
다른 유형의 언어 모델로는 주어진 양쪽의 단어들로부터 가운데 비어있는 단어를 예측하는 언어 모델이 있습니다. 이는 문장의 가운데에 있는 단어를 비워놓고 양쪽의 문맥을 통해서 빈 칸의 단어인지 맞추는 고등학교 수험 시험의 빈칸 추론 문제와 비슷합니다. 이 유형의 언어 모델은 BERT 챕터에서 다루게 될 예정이고, 그때까지는 이전 단어들로부터 다음 단어를 예측하는 방식에만 집중합니다.
언어 모델에 -ing를 붙인 언어 모델링(Language Modeling)은 주어진 단어들로부터 아직 모르는 단어를 예측하는 작업을 말합니다. 즉, 언어 모델이 이전 단어들로부터 다음 단어를 예측하는 일은 언어 모델링입니다.
자연어 처리로 유명한 스탠포드 대학교에서는 언어 모델을 문법(grammar)이라고 비유하기도 합니다. 언어 모델이 단어들의 조합이 얼마나 적절한지, 또는 해당 문장이 얼마나 적합한지를 알려주는 일을 하는 것이 마치 문법이 하는 일 같기 때문입니다.
머신 러닝(Machine Learning) 개요
머신 러닝은 영상 처리, 번역기, 음성 인식, 스팸 메일 탐지 등 굉장히 다양한 분야에서 응용되고 있습니다. 특히 머신 러닝의 한 갈래인 딥 러닝은 자연어 처리 엔지니어에게 필수 역량이 되어가고 있습입니다. 이번 챕터에서는 머신 러닝의 개념과 선형 회귀, 로지스틱 회귀, 소프트맥스 회귀와 같은 기본적인 모델을 이해합니다. 그리고 이러한 이해를 바탕으로 다음 딥 러닝 챕터에서 기본적인 모델로부터 딥 러닝 모델로 개념을 확장해보겠습니다.
    1) 선형 회귀(Linear Regression)
딥 러닝을 이해하기 위해서는 선형 회귀(Linear Regression)와 로지스틱 회귀(Logsitic Regression)를 이해할 필요가 있습니다. 이번 챕터에서는 머신 러닝에서 쓰이는 용어인 가설(Hypothesis), 손실 함수(Loss Function) 그리고 경사 하강법(Gradient Descent)에 대한 개념과 선형 회귀에 대해서 이해합니다.
선형 회귀(Linear Regression)
시험 공부하는 시간을 늘리면 늘릴 수록 성적이 잘 나옵니다. 하루에 걷는 횟수를 늘릴 수록, 몸무게는 줄어듭니다. 집의 평수가 클수록, 집의 매매 가격은 비싼 경향이 있습니다. 이는 수학적으로 생각해보면 어떤 요인의 수치에 따라서 특정 요인의 수치가 영향을 받고있다고 말할 수 있습니다. 조금 더 수학적인 표현을 써보면 어떤 변수의 값에 따라서 특정 변수의 값이 영향을 받고 있다고 볼 수 있습니다. 다른 변수의 값을 변하게하는 변수를 , 변수
에 의해서 값이 종속적으로 변하는 변수 라고 해봅시다.
이때 변수 x의 값은 독립적으로 변할 수 있는 것에 반해, y값은 계속해서 x의 값에 의해서, 종속적으로 결정되므로 x를 독립 변수, y를 종속 변수라고도 합니다. 선형 회귀는 한 개 이상의 독립 변수 x와 y의 선형 관계를 모델링합니다. 만약, 독립 변수 x가 1개라면 단순 선형 회귀라고 합니다.
    2) 벡터와 행렬 연산
앞서 독립 변수 x가 2개 이상인 선형 회귀와 로지스틱 회귀에 대해서 배웠습니다. 그런데 다음 실습인 소프트맥스 회귀에서는 종속 변수 y의 종류도 3개 이상이 되면서 더욱 복잡해집니다. 그리고 이러한 식들이 겹겹이 누적되면 인공 신경망의 개념이 됩니다.
케라스는 사용하기가 편리해서 이런 고민을 할 일이 상대적으로 적지만, Numpy나 텐서플로우의 로우-레벨(low-level)의 머신 러닝 개발을 하게되면 각 변수들의 연산을 벡터와 행렬 연산으로 이해할 수 있어야 합니다. 다시 말해 사용자가 데이터와 변수의 개수로부터 행렬의 크기, 더 나아가 텐서의 크기를 산정할 수 있어야 합니다. 기본적인 벡터와 행렬 연산에 대해서 이해해보겠습니다.
딥 러닝(Deep Learning) 개요
딥 러닝(Deep Learning)은 머신 러닝(Machine Learning)의 특정한 한 분야로서 인공 신경망(Artificial Neural Network)의 층을 연속적으로 깊게 쌓아올려 데이터를 학습하는 방식을 말합니다. 딥 러닝이 화두가 되기 시작한 것은 2010년대의 비교적 최근의 일이지만, 딥 러닝의 기본 구조인 인공 신경망의 역사는 생각보다 오래되었습니다. 이번 챕터에서는 딥 러닝을 보다 쉽게 이해하기 위해 1957년의 초기 인공 신경망인 퍼셉트론에서부터 설명을 시작하여 층을 깊게 쌓아 학습하는 딥 러닝까지 개념을 점차적으로 확장해보겠습니다. 추가적으로 이번 챕터에서는 피드 포워드 신경망과 같은 기본적인 인공 신경망 용어들과 케라스의 사용 방법에 대해서 학습합니다.
- 케라스(Keras) 훑어보기: 이 책에서는 딥 러닝을 쉽게 할 수 있는 파이썬 라이브러리인 케라스(Keras)를 사용합니다. 케라스는 유저가 손쉽게 딥 러닝을 구현할 수 있도록 도와주는 상위 레벨의 인터페이스로 딥 러닝을 쉽게 구현할 수 있도록 해줍니다.
- Tokenizer() : 토큰화와 정수 인코딩을 위해 사용됩니다. 다음은 훈련 데이터로부터 단어 집합을 생성하고, 해당 단어 집합으로 임의의 문장을 정수 인코딩하는 과정을 보여줍니다.
- 워드 임베딩(Word Embedding): 워드 임베딩 챕터에서 다루겠지만, 워드 임베딩이란 텍스트 내의 단어들을 밀집 벡터(dense vector)로 만드는 것을 말합니다. 앞서 배운 개념인 원-핫 벡터와 비교해봅시다. 원-핫 벡터는 대부분이 0의 값을 가지고, 단 하나의 1의 값을 가지는 벡터이며 벡터의 차원이 대체적으로 크다는 성질을 가졌습니다.
텍스트 분류(Text Classification)
텍스트 분류(Text Classification)는 텍스트를 입력으로 받아 텍스트가 어떤 종류의 범주에 속하는지를 구분하는 작업을 말합니다. 가령, 스팸 메일 분류를 한다고 한다면, 스팸 메일 분류는 일반 메일과 스팸 메일이라는 두 개의 범주를 정해놓고 입력받은 메일 본문을 두 개의 메일 종류 중 하나로 분류하는 작업이 될 것입니다.
텍스트 분류에서 분류해야할 범주가 두 가지라면 이진 분류(Binary Classification) 라고 하며, 세 가지 이상이라면 다중 클래스 분류(Multi-Class Classification) 라고 합니다. 일반 메일과 스팸 메일 두 개의 범주를 가진 스팸 메일 분류는 이진 분류에 해당됩니다.
스팸 메일 분류 외에도 영화 리뷰와 같은 텍스트를 입력 받아서 이 리뷰가 긍정 리뷰인지 부정 리뷰인지를 분류하는 '감성 분석', 입력 받은 텍스트로부터 사용자의 의도를 질문, 명령, 거절 등과 같은 의도를 분류하는 '의도 분석' 과 같은 분류 문제들이 있습니다.
이번 챕터에서는 RNN 계열의 신경망 바닐라 RNN, LSTM, GRU를 사용하여 텍스트 분류를 수행해보고, 딥 러닝 코드에 대한 이해도를 높입니다.'''
#%%
testquestion = question_categorize(testtxt)

#%%

if isinstance(testquestion, str):
    testquestion_parsed = json.loads(testquestion)
    print(testquestion_parsed)  # 파싱된 결과 출력
    print(type(testquestion_parsed))  # 파이썬 객체 타입 확인
else:
    print("testquestion은 이미 파이썬 객체입니다:", type(testquestion))
# print(testquestion)
# print(type(testquestion))
