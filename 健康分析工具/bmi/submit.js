async function submitHealthData() {
    const age = document.getElementById('age').value;
    const height = document.getElementById('height').value;
    const weight = document.getElementById('weight').value;

    // 获取性别输入
    const genderInput = document.querySelector('input[name="gender"]:checked');
    const gender = genderInput ? genderInput.value : null; // 防止 gender 未选择时出错

    // 验证输入是否完整
    if (!age || !height || !weight || !gender) {
        document.getElementById('advice').innerHTML = `<span style="color: red;">請填寫全部欄位。</span>`;
        return;
    }

    // 计算 BMI
    const bmi = (weight / ((height / 100) ** 2)).toFixed(2);

    // 计算 BMR
    const bmr = gender === "男" 
        ? (10 * weight + 6.25 * height - 5 * age + 5).toFixed(2)
        : (10 * weight + 6.25 * height - 5 * age - 161).toFixed(2);

    // 理想体重范围
    const idealWeightMin = (18.5 * ((height / 100) ** 2)).toFixed(2);
    const idealWeightMax = (24.9 * ((height / 100) ** 2)).toFixed(2);

    // 判断 BMI 是否正常，并给出具体评估
    let bmiStatus;
    let adviceText;

    if (bmi < 18.5) {
        bmiStatus = "過輕";
        adviceText = getRandomAdvice([
            "您的體重偏輕，建議多攝取營養均衡的食物，並適量增加體重。",
            "現在可能有些過輕，考慮添加健康的卡路里來源如堅果或酪梨！",
            "體重不足可能會影響免疫力，試著多補充優質蛋白質和全穀雜糧吧！"
        ]);
    } else if (bmi >= 18.5 && bmi <= 24.9) {
        bmiStatus = "正常";
        adviceText = getRandomAdvice([
            "您的體重維持得很好，繼續保持健康的生活方式！",
            "恭喜！目前的體重狀態非常理想，維持規律的運動與飲食就可以了。",
            "健康就在您身邊，繼續保持穩定的體重和積極的心態吧！"
        ]);
    } else {
        bmiStatus = "過重";
        adviceText = getRandomAdvice([
            "您的體重偏重，建議多進行有氧運動，如快走或游泳，並調整飲食。",
            "可能需要稍微調整飲食計劃，選擇低熱量但高營養的食物。",
            "為了健康，試著減少加工食品，多吃新鮮蔬果和瘦肉類吧！"
        ]);
    }

    // 整理结果输出
    const advice = `
        <p>BMI: ${bmi} (${bmiStatus})</p>
        <p>BMR (基礎代謝率): ${bmr} 大卡/天</p>
        <p>理想體重範圍: ${idealWeightMin} 公斤 - ${idealWeightMax} 公斤</p>
        <div class="advice-text">${adviceText}</div>
    `;

    document.getElementById('advice').innerHTML = advice;
}

// 獲取隨機建議函數
function getRandomAdvice(adviceArray) {
    return adviceArray[Math.floor(Math.random() * adviceArray.length)];
}
