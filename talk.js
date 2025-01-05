console.log("f*ck");

  // Chatbot 配置
// token here

// 發送消息到 Azure OpenAI API
async function sendMessageToAPI(message) {
  try {
    const response = await fetch(endpointUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "api-key": apiKey,
      },
      body: JSON.stringify({
        messages: [
          { role: "system", content: "你是一個用繁體中文回答問題的智慧助手，請確保你的回應最多為 50 個字。" },
          { role: "user", content: message },
        ],
        max_tokens: 150, // 為了確保有足夠空間生成，設定為約略字數的 3 倍
        temperature: 0.7,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP Error: ${response.status}`);
    }

    const data = await response.json();
    let reply = data.choices[0].message.content;

    // 限制回應為 50 個字
    const maxWords = 50;
    reply = reply.split(' ').slice(0, maxWords).join(' ');

    return reply;
  } catch (error) {
    console.error("Error sending message to API:", error);
    return "抱歉，我無法處理您的請求，請稍後再試。";
  }
}

// 更新聊天記錄
function updateChat(role, message) {
  const chatContainer = document.getElementById("chat-container");
  const messageElement = document.createElement("div");
  messageElement.classList.add("message", role === "user" ? "user-message" : "bot-message");
  messageElement.textContent = message;
  chatContainer.appendChild(messageElement);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

// 初始化事件監聽
document.addEventListener("DOMContentLoaded", () => {
  const sendButton = document.getElementById("send-button");
  const userInput = document.getElementById("user-input");

  sendButton.addEventListener("click", async () => {
    const userMessage = userInput.value.trim();
    if (userMessage === "") return;

    // 顯示用戶訊息
    updateChat("user", userMessage);
    userInput.value = "";

    // 顯示機器人回應
    const botResponse = await sendMessageToAPI(userMessage);
    updateChat("bot", botResponse);
  });

  // 允許按 Enter 發送消息
  userInput.addEventListener("keypress", async (event) => {
    if (event.key === "Enter") {
      sendButton.click();
    }
  });
});
