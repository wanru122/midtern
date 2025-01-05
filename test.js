console.log("連到了幹");

const questions = [
    {
        question: "問題 1:闌尾炎是什麼病？",
        answers: [
            { text: "A: 闌尾腫脹和發炎", correct: true },
            { text: "B: 大腸腫瘤", correct: false },
            { text: "C: 小腸感染", correct: false },
            { text: "D: 胃部潰瘍", correct: false }
        ]
    },
    {
        question: "問題 2:大腸癌的常見症狀包括以下哪一項？",
        answers: [
            { text: "A: 持續腹痛與便血", correct: true },
            { text: "B: 頻繁頭痛", correct: false },
            { text: "C: 皮膚紅疹", correct: false },
            { text: "D: 咳嗽和呼吸困難", correct: false }
        ]
    },
    {
        question: "問題 3:哪一種疾病是女性生殖系統中最常見的癌症之一，並且通常影響卵巢？",
        answers: [
            { text: "A: 子宮頸癌", correct: false },
            { text: "B: 卵巢癌", correct: true },
            { text: "C: 子宮內膜癌", correct: false },
            { text: "D: 乳腺癌", correct: false }
        ]
    },
    {
        question: "問題 4:哪一種女性生殖系統的疾病可能會導致不孕？",
        answers: [
            { text: "A: 多囊卵巢綜合症（PCOS）", correct: true },
            { text: "B: 更年期", correct: false },
            { text: "C: 子宮肌瘤", correct: false },
            { text: "D: 絕經後出血", correct: false }
        ]
    },
    {
        question: "問題 5:以下哪一種疾病屬於神經系統疾病，並且通常與神經元的損傷和死亡有關？",
        answers: [
            { text: "A: 抑鬱症", correct: false },
            { text: "B: 阿茲海默症", correct: true },
            { text: "C: 焦慮症", correct: false },
            { text: "D: 精神分裂症難", correct: false }
        ]
    },
    {
        question: "問題 6:以下哪一項不是焦慮症的常見症狀？",
        answers: [
            { text: "A: 呼吸急促", correct: false },
            { text: "B: 持續的無緣無故的擔心", correct: false },
            { text: "C: 噁心和腹痛", correct: false },
            { text: "D: 幻覺和妄想", correct: true }
        ]
    },
    {
        question: "問題 7:哪一種疾病會導致甲狀腺功能亢進，並且通常伴隨有眼睛突出等症狀？",
        answers: [
            { text: "A: 艾迪生病", correct: false },
            { text: "B: 橋本病", correct: false },
            { text: "C: 格雷夫氏病", correct: true },
            { text: "D: 甲狀腺結節", correct: false }
        ]
    },
    {
        question: "問題 8:甲狀腺癌最常見的類型是哪一種？",
        answers: [
            { text: "A: 乳頭狀甲狀腺癌", correct: true },
            { text: "B: 鱗狀甲狀腺癌", correct: false },
            { text: "C: 小細胞甲狀腺癌", correct: false },
            { text: "D: 腺癌", correct: false }
        ]
    },
    {
        question: "問題 9:哪一種疾病是由紅血球數量過少引起的，並且通常導致貧血症狀？",
        answers: [
            { text: "A: 白血病", correct: false },
            { text: "B: 血友病", correct: false },
            { text: "C: 貧血", correct: true },
            { text: "D: 血栓形成", correct: false }
        ]
    },
    {
        question: "問題 10:哪一項症狀是白血病患者常見的？",
        answers: [
            { text: "A: 經常性感冒", correct: false },
            { text: "B: 易出血或瘀傷", correct: true },
            { text: "C: 高血糖", correct: false },
            { text: "D: 心跳過慢", correct: false }
        ]
    },
    {
        question: "問題 11:哪一種疾病會導致男性陰莖出現不正常的彎曲，並影響性生活？",
        answers: [
            { text: "A: 前列腺癌", correct: false },
            { text: "B: Peyronie病（陰莖彎曲病）", correct: true },
            { text: "C: 睾丸癌", correct: false },
            { text: "D: 睾丸扭轉", correct: false }
        ]
    },
    {
        question: "問題 12:哪一項是肝硬化的常見症狀？",
        answers: [
            { text: "A: 常便秘（黃疸）", correct: false },
            { text: "B: 皮膚和眼睛發黃", correct: true },
            { text: "C: 噁心和嘔吐", correct: false },
            { text: "D: 呼吸急促", correct: false }
        ]
    },
    {
        question: "問題 13:哪一項是肺炎的常見症狀？",
        answers: [
            { text: "A: 持續高燒、咳嗽並伴隨痰液", correct: true },
            { text: "B: 頭痛、腹痛", correct: false },
            { text: "C: 喉嚨痛和耳鳴", correct: false },
            { text: "D: 胸痛和腹脹", correct: false }
        ]
    },
    {
        question: "問題 14:慢性阻塞性肺疾病（COPD）通常由哪一種原因引起？",
        answers: [
            { text: "A: 長期吸煙", correct: true },
            { text: "B: 空氣污染", correct: false },
            { text: "C: 肥胖症", correct: false },
            { text: "D: 遺傳疾病", correct: false }
        ]
    },
    {
        question: "問題 15:哪一項是肺結核的傳播途徑？",
        answers: [
            { text: "A: 飛沫傳播", correct: true },
            { text: "B: 血液傳播", correct: false },
            { text: "C: 飲食污染", correct: false },
            { text: "D: 空氣接觸", correct: false }
        ]
    },
    {
        question: "問題 16:胃食道逆流病（GERD）的主要症狀是？",
        answers: [
            { text: "A: 胸痛、噯氣和吞嚥困難", correct: true },
            { text: "B: 嘔吐和腹瀉", correct: false },
            { text: "C: 喉嚨痛和耳鳴", correct: false },
            { text: "D: 頭暈和頭痛", correct: false }
        ]
    },
    {
        question: "問題 17:胃癌的常見風險因素是？",
        answers: [
            { text: "A: 長期吸煙和不健康飲食", correct: true },
            { text: "B: 肥胖症和高血糖", correct: false },
            { text: "C: 乙型肝炎病毒", correct: false },
            { text: "D: 乙型肝炎病毒", correct: false }
        ]
    },
    {
        question: "問題 18:哪一項是膀胱炎的典型症狀？",
        answers: [
            { text: "A: 高燒、發冷", correct: false },
            { text: "B: 頻尿、尿急和尿痛", correct: true },
            { text: "C: 嘔吐和腹痛", correct: false },
            { text: "D: 食慾不振和體重減輕", correct: false }
        ]
    },
    {
        question: "問題 19:哪一種疾病會導致膀胱內形成硬塊，並影響排尿功能？",
        answers: [
            { text: "A: 膀胱結石", correct: false },
            { text: "B: 膀胱癌", correct: true },
            { text: "C: 膀胱炎", correct: false },
            { text: "D: 膀胱過度活動症", correct: false }
        ]
    },
    {
        question: "問題 20:胰臟癌最常見的症狀是？",
        answers: [
            { text: "A: 便秘和腹脹", correct: false },
            { text: "B: 背痛、體重減輕、黃疸（皮膚和眼睛發黃）", correct: true },
            { text: "C: 頭痛和聽力下降", correct: false },
            { text: "D: 持續咳嗽和喘", correct: false }
        ]
    },
    {
        question: "問題 21:什麼是腎結石的常見症狀？",
        answers: [
            { text: "A: 頭痛和發燒", correct: false },
            { text: "B: 低血壓和呼吸困難", correct: false },
            { text: "C: 突然的劇烈腰痛，並可能伴隨血尿", correct: true },
            { text: "D: 食慾不振和腹瀉", correct: false }
        ]
    },
    {
        question: "問題 22:哪一種疾病會導致腎臟無法有效地過濾血液並排出廢物？",
        answers: [
            { text: "A: 持續腹痛與便血", correct: true },
            { text: "B: 頻繁頭痛", correct: false },
            { text: "C: 皮膚紅疹", correct: false },
            { text: "D: 咳嗽和呼吸困難", correct: false }
        ]
    },
    {
        question: "問題 23:哪一種疾病與胰臟分泌過多胰島素有關？",
        answers: [
            { text: "A: 糖尿病", correct: false },
            { text: "B: 胰島素瘤", correct: true },
            { text: "C: 胰臟炎", correct: false },
            { text: "D: 胰臟癌", correct: false }
        ]
    },
    {
        question: "問題 24:以下哪一種是過敏性鼻炎的常見症狀？",
        answers: [
            { text: "A: 發燒和咳嗽", correct: false },
            { text: "B: 鼻塞、流鼻水、打噴嚏和眼睛癢", correct: true },
            { text: "C: 胸痛和呼吸困難", correct: false },
            { text: "D: 腹痛和嘔吐", correct: false }
        ]
    },
    {
        question: "問題 25:哪一項是心臟病的常見風險因素？",
        answers: [
            { text: "A: 高血壓、高膽固醇、吸煙", correct: true },
            { text: "B: 長期飲酒、缺乏運動、過度勞累", correct: false },
            { text: "C: 體重過輕、過多睡眠、食慾不振", correct: false },
            { text: "D: 眼睛乾澀、咳嗽、咽喉痛", correct: false }
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
