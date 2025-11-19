// DOM Elements
const chatbotIcon = document.getElementById('chatbot-icon');
const chatWindow = document.getElementById('chat-window');
const closeChat = document.getElementById('close-chat');
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const promptCards = document.querySelectorAll('.prompt-card');

let sessionId = '';

// Chatbot functionality
chatbotIcon.addEventListener('click', function() {
    chatWindow.style.display = 'flex';
    if (studentName && chatMessages.children.length === 0) {
        addBotMessage(`Hello ${studentName}! I'm your CareerGuide AI assistant. I'm here to help you with career-related questions. How can I assist you today?`);
    } else if (chatMessages.children.length === 0) {
        addBotMessage("Hello! I'm your CareerGuide AI assistant. I'm here to help you with career-related questions. How can I assist you today?");
    }
});

closeChat.addEventListener('click', function() {
    chatWindow.style.display = 'none';
});

// Send message on button click
sendBtn.addEventListener('click', function() {
    sendMessage();
});

// Send message on Enter key
userInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Prompt cards
promptCards.forEach(card => {
    card.addEventListener('click', function() {
        const prompt = this.getAttribute('data-prompt');
        chatWindow.style.display = 'flex';
        addUserMessage(prompt);
        sendMessageToAPI(prompt);
    });
});

// Function to send message
function sendMessage() {
    const message = userInput.value.trim();
    if (message === '') return;
    
    addUserMessage(message);
    userInput.value = '';
    sendMessageToAPI(message);
}

// Function to add user message
function addUserMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', 'user-message');
    messageDiv.textContent = message;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Function to add bot message
function addBotMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', 'bot-message');
    messageDiv.textContent = message;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Function to show typing indicator
function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.classList.add('typing-indicator');
    typingDiv.id = 'typing-indicator';
    
    const typingDots = document.createElement('div');
    typingDots.classList.add('typing-dots');
    
    for (let i = 0; i < 3; i++) {
        const dot = document.createElement('span');
        typingDots.appendChild(dot);
    }
    
    typingDiv.appendChild(typingDots);
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    return typingDiv;
}

// Function to send message to Django API
function sendMessageToAPI(message) {
    const typingIndicator = showTypingIndicator();
    
    fetch(chatApiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            message: message,
            session_id: sessionId
        })
    })
    .then(response => response.json())
    .then(data => {
        typingIndicator.remove();
        
        if (data.response) {
            addBotMessage(data.response);
            sessionId = data.session_id;
        } else if (data.error) {
            addBotMessage("Sorry, I encountered an error. Please try again.");
        }
    })
    .catch(error => {
        typingIndicator.remove();
        addBotMessage("Sorry, I'm having trouble connecting. Please check your internet connection and try again.");
    });
}

// Function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}