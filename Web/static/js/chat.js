
// 将消息添加到聊天界面中
function appendMessage(sender, message) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    messageElement.classList.add(sender === 'user' ? 'user-message' : 'chatgpt-message');
    messageElement.innerHTML = `
        <span class="icon"><i class="${sender === 'user' ? 'fas fa-user user-icon' : 'fas fa-robot chatgpt-icon'}"></i></span>
        ${message}
    `;

    chatOutput.appendChild(messageElement);

    // 如果消息来自用户，则显示AI回答框
    if (sender === 'user') {
        const thinkingElement = document.createElement('div');
        thinkingElement.classList.add('message');
        thinkingElement.classList.add('chatgpt-message');
        thinkingElement.innerHTML = '<span class="icon"><i class="fas fa-robot chatgpt-icon"></i></span>正在思考中...';
        chatOutput.appendChild(thinkingElement);
    }

    chatOutput.scrollTop = chatOutput.scrollHeight;
}


// 发送用户消息到服务器
function sendUserMessage(post, message) {
    // 发送POST请求到服务器
    fetch(post, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            message: message,
        }),
    })
        .then((response) => response.json())
        .then((data) => {
            const thinkingMessage = chatOutput.lastElementChild;
            thinkingMessage.innerHTML = `<span class="icon"><i class="fas fa-robot chatgpt-icon"></i></span>${thinkingMessage.innerText}<span class="typing-cursor"></span>`;
            showChatGptResponse(data.completion.trim());
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

// 逐字显示问答系统的回答
function showChatGptResponse(response) {
    const aiResponseElement = chatOutput.lastElementChild;

    const typingCursor = aiResponseElement.querySelector('.typing-cursor');
    typingCursor.style.visibility = 'visible';

    let index = 0;
    const delay = 50; // 每个字符的延迟时间间隔（毫秒）

    const intervalId = setInterval(() => {
        aiResponseElement.innerHTML = `<span class="icon"><i class="fas fa-robot chatgpt-icon"></i></span>${response.slice(
            0,
            index
        )}<span class="typing-cursor"></span>`;
        index++;

        if (index > response.length) {
            clearInterval(intervalId);
            typingCursor.style.visibility = 'hidden';
        }
    }, delay);
}



