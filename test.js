console.log("連到了幹");

const questions = [
    {
        question: "問題 1: 000喜歡吃什麼?",
        answers: [
            { text: "A: 芋頭", correct: false },
            { text: "B: 大便", correct: true },
            { text: "C: 芋頭口味的大便", correct: false },
            { text: "D: 大便口味的芋頭", correct: false }
        ]
    },
    {
        question: "問題 2: ?",
        answers: [
            { text: "A: ", correct: false },
            { text: "B: ", correct: true },
            { text: "C: ", correct: false },
            { text: "D: ", correct: false }
        ]
    },
    {
        // question: "問題 2: 魚的主要呼吸器官是?",
        // answers: [
        //     { text: "A: 肺", correct: false },
        //     { text: "B: 鳃", correct: true },
        //     { text: "C: 胃", correct: false },
        //     { text: "D: 皮膚", correct: false }
        // ]
    },
    // 添加更多問題
];

let currentQuestionIndex = 0;
let score = 0;

function startGame() {
    currentQuestionIndex = 0;
    score = 0;
    showQuestion(questions[currentQuestionIndex]);
}

function showQuestion(question) {
    const questionContainer = document.getElementById('question-container');
    questionContainer.querySelector('#question').innerText = question.question;
    const answerButtons = questionContainer.querySelector('#answer-buttons');
    answerButtons.innerHTML = ''; // 清空按鈕

    question.answers.forEach(answer => {
        const button = document.createElement('button');
        button.innerText = answer.text;
        button.classList.add('btn');
        button.addEventListener('click', () => selectAnswer(answer));
        answerButtons.appendChild(button);
    });
}

function selectAnswer(answer) {
    if (answer.correct) {
        score++;
        alert("答對了 你太強了吧");
    } else {
        alert("答錯了唷 你是不是沒讀書");
    }
    currentQuestionIndex++;
    if (currentQuestionIndex < questions.length) {
        showQuestion(questions[currentQuestionIndex]);
    } else {
        alert(`遊戲結束咯 你的分數是: ${score}`);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    startGame(); // 在 DOM 加載完成後啟動遊戲
});
