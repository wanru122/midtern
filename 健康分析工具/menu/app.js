async function submitHealthData() {
    const bmi = document.getElementById('bmi').value;
    const bmr = document.getElementById('bmr').value;
    const diet = document.getElementById('diet').value;
    const exercise = document.getElementById('exercise').value;
    const goal = document.getElementById('goal').value;
    const mealPlan = '一日三餐';  // 這是觸發語言
    const exercisePlan ='運動計畫';
    // 在提交時先顯示提示文字
    const adviceDiv = document.getElementById('advice');
    adviceDiv.innerHTML = `<p style="color: blue;">正在生成菜單，請稍等...</p>`;

    
    try {
        const response = await fetch('http://localhost:5000/get_advice', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ bmi, bmr, diet, exercise, goal, meal_plan: mealPlan ,exercise_plan: exercisePlan})
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (data.error) {
            document.getElementById('advice').innerText = `錯誤: ${data.error}`;
        } else {
            document.getElementById('advice').innerText = `AI 建議：${data.advice}`;
        }
    } catch (error) {
        console.error('錯誤:', error);
        document.getElementById('advice').innerText = '發生錯誤，請稍後再試。';
    }
}
