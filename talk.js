console.log("Message from talk.js");

var ws = new WebSocket("/chat");

ws.onopen = function (event) {
  console.log("Connected to WebSocket server.");
};

ws.onerror = function (error) {
  console.error("WebSocket error:", error);
};

ws.onclose = function () {
  console.log("WebSocket connection closed.");
};

document.addEventListener("DOMContentLoaded", function () {
  const chatContainer = document.getElementById("chat-container");
  const userInput = document.getElementById("user-input");
  const sendButton = document.getElementById("send-button");

  sendButton.addEventListener("click", sendMessage);

  userInput.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
      sendMessage();
    }
  });

  
  function sendMessage() {
    const inputValue = userInput.value.trim();
    if (inputValue) {
      appendMessage(inputValue, "user");
      ws.send(inputValue); 
      userInput.value = ""; 
    }
  }
  
  ws.onmessage = function (event) {
    console.log("Received message:", event.data);
    appendMessage(event.data, "bot");
  };

  
  function appendMessage(message, sender) {
    const messageElement = document.createElement("div");
    messageElement.classList.add("message", sender === "user" ? "user-message" : "bot-message");
    messageElement.textContent = message;

    
    messageElement.style.opacity = 0;
    chatContainer.appendChild(messageElement);
    setTimeout(() => (messageElement.style.opacity = 1), 10);

    
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }
});
