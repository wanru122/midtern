console.log("Hello from talk.js");

var ws = new WebSocket("/chat");
    
ws.onopen = function(event) {
    console.log("Connected to WebSocket server.");
};

document.addEventListener("DOMContentLoaded", function () {
  // 當點擊 "Send" 按鈕時發送訊息
  document.getElementById("send-button").addEventListener("click", function () {
    var inputValue = document.getElementById('user-input').value;
            document.getElementById('user-input').value = '';
            ws.send(inputValue);
    // var userMessage = document.getElementById("user-input").value.trim();
    if (inputValue) {
      // 顯示用戶的訊息
      appendMessage("你: " + inputValue, "user");

      
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
  };
  ws.onmessage = function(event) {
    console.log("Received message: " + event.data);
    appendMessage("BOT: " + event.data, "bot");
  };
});

