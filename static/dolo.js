
function sendMessage() {
    var messageInput = document.getElementById('messageInput');
    var message = messageInput.value;

    if (message.trim() !== '') {
        var chat = document.getElementById('chat');

        var messageDiv = document.createElement('div');
        messageDiv.className = 'message1';
        messageDiv.textContent = message;

        chat.appendChild(messageDiv);
        messageInput.value = '';

        // Scroll to the bottom of the chat
        chat.scrollTop = chat.scrollHeight;

        // Simulate receiving a message after a short delay
        setTimeout(function () {
            receiveMessage("This is a reply from server.");
        }, 100);
    }
}

function receiveMessage(message) {
    var chat = document.getElementById('chat');

    var messageDiv = document.createElement('div');
    messageDiv.className = 'message';
    messageDiv.textContent = message;

    chat.appendChild(messageDiv);

    // Scroll to the bottom of the chat
    chat.scrollTop = chat.scrollHeight;
}

// Simulate an initial received message
window.onload = function () {
    receiveMessage("Hello! How can I help you?");
};