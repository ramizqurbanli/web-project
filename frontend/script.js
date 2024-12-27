const chatBox = document.getElementById('chat-box');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');

const backendUrl = 'http://127.0.0.1:8000/chat'; // URL for your FastAPI backend


// Append a message to the chat box
function appendMessage(text, sender) {
  const messageDiv = document.createElement('div');
  const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  
  messageDiv.classList.add('message', sender);
  
  // Combine the message text with timestamp
  messageDiv.innerHTML = `
      ${text}
      <span class="time">${currentTime}</span>
  `;
  
  chatBox.appendChild(messageDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}
// Send a message to the backend
async function sendMessage(message) {
  appendMessage(message, 'user');

  try {
    const response = await fetch(backendUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message }),
    });

    if (response.ok) {
      const data = await response.json();
      appendMessage(data.response, 'bot'); // Adjusted to match backend response
    } else {
      appendMessage('Error: Could not fetch a response.', 'bot');
    }
  } catch (error) {
    appendMessage('Error: Unable to connect to the server.', 'bot');
  }
}

// Event listener for the send button
sendBtn.addEventListener('click', () => {
  const message = chatInput.value.trim();
  if (message) {
    sendMessage(message);
    chatInput.value = '';
  }
});

chatInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    sendBtn.click();
  }
});
