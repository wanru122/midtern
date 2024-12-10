console.log("f*ck");
const endpointUrl = "";
    const apiKey = "";

    // 发送消息到 Azure OpenAI API
    async function sendMessageToAPI(message) {
      const response = await fetch(endpointUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "api-key": apiKey,
        },
        body: JSON.stringify({
          messages: [{ role: "user", content: message }],
          max_tokens: 100,
          temperature: 0.7,
        }),
      });
      const data = await response.json();
      return data.choices[0].message.content;
    }

    // 更新聊天记录
    function updateChat(role, message) {
      const chatContainer = document.getElementById("chat-container");
      const messageElement = document.createElement("div");
      messageElement.classList.add("message", role === "user" ? "user-message" : "bot-message");
      messageElement.textContent = message;
      chatContainer.appendChild(messageElement);
      chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // 发送按钮点击事件
    document.getElementById("sendButton").addEventListener("click", async () => {
      const userInput = document.getElementById("user-input");
      const userMessage = userInput.value.trim();
      if (userMessage === "") return;

      // 显示用户消息
      updateChat("user", userMessage);
      userInput.value = "";

      // 获取并显示机器人回复
      const botResponse = await sendMessageToAPI(userMessage);
      updateChat("bot", botResponse);
    });