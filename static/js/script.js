function addMessage(text, sender) {
  const chatMessages = document.getElementById("chat-messages");
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${sender}`;

  // Create avatar container
  const avatarContainer = document.createElement("div");
  avatarContainer.className = "avatar-container";

  // Create avatar image
  const avatar = document.createElement("img");
  avatar.className = "avatar";

  if (sender === "bot") {
    avatar.src = "static/images/Image_ema.png";
    avatar.alt = "Ema";
  } else {
    avatar.src = "https://cdn-icons-png.flaticon.com/512/1144/1144760.png";
    avatar.alt = "User";
  }

  avatarContainer.appendChild(avatar);

  // Create message content
  const messageContent = document.createElement("div");
  messageContent.className = "message-content";
  messageContent.innerHTML = formatMessage(text);

  // Add elements in correct order based on sender
  if (sender === "bot") {
    messageDiv.appendChild(avatarContainer);
    messageDiv.appendChild(messageContent);
  } else {
    messageDiv.appendChild(messageContent);
    messageDiv.appendChild(avatarContainer);
  }

  chatMessages.appendChild(messageDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function formatMessage(text) {
  // Format bold text
  text = text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
  // Convert line breaks to <br>
  text = text.replace(/\n/g, "<br>");
  return text;
}

let isProcessing = false;

async function sendMessage() {
  if (isProcessing) return;

  const inputElement = document.getElementById("user-input");
  const userMessage = inputElement.value.trim();

  if (userMessage === "") return;

  // Clear input and add user message
  inputElement.value = "";
  addMessage(userMessage, "user");
  isProcessing = true;

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: userMessage }),
    });

    if (!response.ok) throw new Error("Network response was not ok");

    const data = await response.json();
    addMessage(data.response, "bot");
  } catch (error) {
    console.error("Error:", error);
    addMessage(
      "I apologize, but I encountered an error. Please try again.",
      "bot"
    );
  } finally {
    isProcessing = false;
  }
}

// Send message on Enter key
document
  .getElementById("user-input")
  .addEventListener("keypress", function (e) {
    if (e.key === "Enter" && !isProcessing) {
      sendMessage();
    }
  });
