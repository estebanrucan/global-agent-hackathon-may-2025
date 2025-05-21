document.addEventListener('DOMContentLoaded', function() {
    const sendBtn = document.getElementById('send-btn');
    const userInput = document.getElementById('user-input');
    const chatWindow = document.getElementById('chat-window');
    const loadingIndicator = document.getElementById('loading-indicator');

    // Ajustar altura del textarea dinámicamente
    userInput.addEventListener('input', function () {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });

    function appendMessage(sender, text, isHtml = false) {
        const msgArticle = document.createElement('article');
        msgArticle.classList.add('chat-message', sender);
        
        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message');

        if (sender === 'bot' && isHtml) {
            contentDiv.innerHTML = text; // Asume que text es HTML seguro (proveniente de marked.parse)
        } else {
            contentDiv.textContent = text;
        }
        
        msgArticle.appendChild(contentDiv);
        chatWindow.appendChild(msgArticle);
        chatWindow.scrollTop = chatWindow.scrollHeight; // Mantener el scroll abajo
    }

    function showLoading(isLoading) {
        if (isLoading) {
            loadingIndicator.style.display = 'block';
            sendBtn.disabled = true;
            userInput.disabled = true;
        } else {
            loadingIndicator.style.display = 'none';
            sendBtn.disabled = false;
            userInput.disabled = false;
            userInput.focus();
        }
    }

    async function handleSendMessage() {
        const text = userInput.value.trim();
        if (!text) return;

        appendMessage('user', text);
        userInput.value = '';
        userInput.style.height = 'auto'; // Resetear altura del textarea

        showLoading(true);

        try {
            const res = await fetch('/api/chat', { // Endpoint de la API
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: text})
            });
            
            if (!res.ok) {
                let errorMsg = `Error del servidor: ${res.status}`;
                try {
                    const errorData = await res.json();
                    errorMsg = errorData.error || errorMsg;
                } catch (e) { /* No hacer nada si el cuerpo del error no es JSON */ }
                throw new Error(errorMsg);
            }

            const data = await res.json();
            if (data.error) {
                appendMessage('bot', `Error: ${data.error}`);
            } else {
                const htmlResponse = marked.parse(data.response); // Usa marked.js
                appendMessage('bot', htmlResponse, true);
            }
        } catch (e) {
            appendMessage('bot', `Error de comunicación: ${e.message}`);
        } finally {
            showLoading(false);
        }
    }

    sendBtn.addEventListener('click', handleSendMessage);

    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    });

    userInput.focus(); // Enfocar el input al cargar la página
}); 