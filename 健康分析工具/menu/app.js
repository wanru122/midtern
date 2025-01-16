async function fetchHealthAdvice(payload) {
    const response = await fetch('http://localhost:5000/get_advice', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
}

async function submitHealthData() {
    const payload = {
        bmi: document.getElementById('bmi').value,
        bmr: document.getElementById('bmr').value,
        diet: document.getElementById('diet').value,
        exercise: document.getElementById('exercise').value,
        goal: document.getElementById('goal').value,
        meal_plan: '一日三餐',
        exercise_plan: '運動計畫'
    };

    const adviceDiv = document.getElementById('advice');
    const submitButton = document.querySelector("button[type='button']");

    // 确保所有必要字段都有值
    if (!payload.bmi || !payload.bmr || !payload.goal || !payload.exercise) {
        adviceDiv.innerHTML = `<p style="color: red;">請填寫所有必要欄位。</p>`;
        return;
    }

    // 禁用提交按钮，防止重复提交
    submitButton.disabled = true;
    adviceDiv.innerHTML = `<p style="color: blue;">正在生成建議，請稍候...</p>`;

    try {
        const data = await fetchHealthAdvice(payload);

        // 检查返回的结果并更新提示
        if (data.error) {
            adviceDiv.innerHTML = `<p style="color: red;">錯誤: ${data.error}</p>`;
        } else {
            // 对返回的建议文本进行格式化，使其显示为易读的多行文本
            const formattedAdvice = data.advice.replace(/\n/g, '<br>');
            adviceDiv.innerHTML = `<p style="color: green;">AI 建議：<br>${formattedAdvice}</p>`;
        }
    } catch (error) {
        console.error('錯誤:', error);
        adviceDiv.innerHTML = '<p style="color: red;">發生錯誤，請稍後再試。</p>';
    } finally {
        // 恢复提交按钮可用
        submitButton.disabled = false;
    }
}
