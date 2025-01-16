let currentQuestionIndex = 0;
let score = 0;

// 初始化遊戲
fetch('/start')
    .then(response => response.json())
    .then(data => {
        showQuestion(data);
    });

function showQuestion(question) {
    document.getElementById('question').innerText = question.question;
    const answerButtons = document.getElementById('answer-buttons');
    answerButtons.innerHTML = ''; // 清空按鈕

    question.answers.forEach(answer => {
        const button = document.createElement('button');
        button.innerText = answer.text;
        button.classList.add('btn');
        button.addEventListener('click', () => selectAnswer(answer.text, question));
        answerButtons.appendChild(button);
    });
}

function selectAnswer(answerText, question) {
    fetch('/answer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            answer: answerText,
            questionIndex: currentQuestionIndex
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.result === 'correct') {
            score++;
            alert("答對了！你太強了！");
        } else {
            alert("答錯了！加油！");
        }

        // 更新分數顯示
        document.getElementById('score').innerText = `分數：${score}`;

        // 顯示下一題或者遊戲結束
        currentQuestionIndex++;
        if (data.game_over) {
            alert(`遊戲結束！你的分數是：${score}`);
        } else {
            showQuestion(questions[currentQuestionIndex]);
        }
    });
}
