console.log("Hello from talk.js");

document.addEventListener("DOMContentLoaded", function () {
  // 當點擊 "Send" 按鈕時發送訊息
  document.getElementById("send-button").addEventListener("click", function () {
    var userMessage = document.getElementById("user-input").value.trim();
    if (userMessage) {
      // 顯示用戶的訊息
      appendMessage("你: " + userMessage, "user");

      // 發送訊息到 Flask 後端
      fetch("http://127.0.0.1:5000/send_message", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: userMessage })
      })
      .then(response => response.json())
      .then(data => {
        if (data.reply) {
          appendMessage("聊天機器人: " + data.reply, "bot");
        } else if (data.error) {
          appendMessage("錯誤: " + data.error, "error");
        }
      })
      .catch(error => {
        appendMessage("錯誤: 無法連接到伺服器", "error");
      });

      // 清空輸入框
      document.getElementById("user-input").value = "";
    }
  });

  // 允許按 Enter 發送訊息
  document.getElementById("user-input").addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
      document.getElementById("send-button").click();
    }
  });

  // 顯示訊息的函數
  function appendMessage(message, sender) {
    var chatContainer = document.getElementById("chat-container");
    var messageElement = document.createElement("div");
    messageElement.classList.add(sender); // 根據發送者設置樣式（user 或 bot）
    messageElement.textContent = message;
    chatContainer.appendChild(messageElement);
    chatContainer.scrollTop = chatContainer.scrollHeight; // 讓聊天框自動滾動到最新訊息
  }
});
