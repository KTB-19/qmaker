import { React, useState, useEffect } from "react";
import QuizNums from "./QuizNums";
import QuizContents from "./QuizContents";
import ProgressBar from "./ProgressBar";
import "./Quiz.css"
import ProblemTestData, { ProblemTestDataSet } from "../TestDataSet/ProblemTestData";

function Quiz() {
    // 문제 상태 배열 관리, 길이 10의 배열에 푼 문제의 답 넣기, 초기값은 모두 -1로
    // 값이 -1이면 안풀었고, 0~3이면 풀었다고 인식
    // 문제 상태 리스트에 -1이 아닌 값이 몇개인지에 따라 usestate로 푼 문제 개수 체크=>progressbar로 전달
    // ..progressbar에서는 전체 화면 너비를 10등분하여 10 중 푼 문제의 개수만큼 얇은 사각형의 가로 길이 조정
    // ..하나도 안풀었으면 사각형 길이 0, 다 풀었으면 사각형 길이==화면 가로 길이

    // 문제 상태 배열
    const [problemStates, setProblemStates] = useState(Array(10).fill(-1));
    const [solvedCount, setSolvedCount] = useState('');

    // 푼 문제의 개수 카운팅
    useEffect(() => {
        setSolvedCount(problemStates.filter(state => state !== -1).length);
    }, [problemStates]);
    

    // sample 문제 데이터 세션 스토리지에 저장
    sessionStorage.setItem('problemId', JSON.stringify(ProblemTestDataSet.problem_set_id));
    ProblemTestDataSet.problems.forEach((problem, index) => {
        sessionStorage.setItem(`problem_${index}`, JSON.stringify(problem));
    })


    const [currentProblem, setCurrentProblem] = useState(null); // 현재 선택한 문제 인덱스 저장
    // QuizNums에서 선택한 문제의 인덱스를 받아서 currentProblem 업데이트
    const handleProblemSelect = (index) => {
        setCurrentProblem(index);
    };

    // QuizContents에서 답 선택 후 문제 상태를 업데이트
    const handleAnswerSubmit = (index, answer) => {
        const updatedStates = [...problemStates];
        updatedStates[index] = answer;
        setProblemStates(updatedStates);
        sessionStorage.setItem('answers',updatedStates);
        console.log(problemStates);
    };


    // 퀴즈넘에서 특정 숫자의 버튼 클릭하면 그 버튼의 숫자(인덱스)를 컨텐츠로 전달
    // ..컨텐츠에서 해당 인덱스의 문제 세션 스토리지에서 불러와서 렌더링
    // ..컨텐츠에서 해당 인덱스의 문제 답 클릭하면 해당 인덱스의 문제 상태 배열에 바로 반영

    // Quiz 파일에서는 TestDataSet/ProblemTestData.jsx를 불러와 안의 값들을 세션스토리지에 구분하여 저장. 
    return (
        <>
            <div className="progress-bar">
                <ProgressBar solvedCount={solvedCount} />
            </div>
            <div className="width-container">
                <div className="sidebar">
                    <QuizNums onProblemSelect={handleProblemSelect} />
                </div>
                <div className="quiz">
                    {currentProblem !== null && (
                        <QuizContents 
                            answers={problemStates}
                            problemIndex={currentProblem} 
                            onAnswerSubmit={handleAnswerSubmit} 
                        />
                    )}
                </div>
            </div>
        </>
    );
}

export default Quiz;
