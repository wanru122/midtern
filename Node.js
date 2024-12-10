console.log("連到了拉幹0.0");

document.addEventListener('DOMContentLoaded', function() {
    // 綁定發送按鈕的點擊事件
    document.getElementById('sendButton').addEventListener('click', async function() {
        const userInput = document.getElementById('user-input').value;
        
        if (userInput) {
            displayUserMessage(userInput); // 顯示使用者訊息
            document.getElementById('user-input').value = ''; // 清空輸入框
            await sendMessage(userInput); // 發送訊息並獲取回應
        }
    });

    // 綁定評論提交事件
    document.getElementById('commentForm').addEventListener('submit', function(event) {
        event.preventDefault(); // 防止表單提交
        const comment = document.getElementById('commentInput').value;
        displayComment(comment); // 顯示評論
        document.getElementById('commentInput').value = ''; // 清空輸入框
    });
});

// 顯示使用者的訊息
function displayUserMessage(message) {
    const messagesDiv = document.getElementById('messages');
    const userMessage = document.createElement('div');
    userMessage.classList.add('message', 'user-message');
    userMessage.textContent = message;
    messagesDiv.appendChild(userMessage);
    messagesDiv.scrollTop = messagesDiv.scrollHeight; // 自動滾動到底部
}

// 發送訊息至 Azure OpenAI 並顯示回應
async function sendMessage(message) {
    const apiKey = ''; // 替換成您的 API Key
    const endpoint = ''; // 替換成您的端點 URL

    const headers = {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${apiKey}`
    };

    const requestBody = {
        "messages": [
            {"role": "user", "content": message}
        ],
        "max_tokens": 50 // 調整此值根據需求
    };

    try {
        const response = await fetch(endpoint, {
            method: "POST",
            headers: headers,
            body: JSON.stringify(requestBody)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`HTTP error! Status: ${response.status} - ${errorData.message}`);
        }

        const data = await response.json();
        
        // 顯示機器人回應
        displayBotMessage(data.choices[0].message.content);
    } catch (error) {
        console.error("Error:", error);
        displayBotMessage("無法取得回應。");
    }
}

// 顯示機器人的回應
function displayBotMessage(message) {
    const messagesDiv = document.getElementById('messages');
    const botMessage = document.createElement('div');
    botMessage.classList.add('message', 'bot-message');
    botMessage.textContent = message;
    messagesDiv.appendChild(botMessage);
    messagesDiv.scrollTop = messagesDiv.scrollHeight; // 自動滾動到底部
}

// 顯示評論
function displayComment(comment) {
    const commentsContainer = document.getElementById('commentsContainer');
    const commentDiv = document.createElement('div');
    commentDiv.classList.add('comment');
    commentDiv.textContent = comment;
    commentsContainer.appendChild(commentDiv);
}
