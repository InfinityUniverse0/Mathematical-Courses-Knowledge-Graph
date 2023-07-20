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
            message: message
        }),
    })
        .then(response => response.json())
        .then(data => {
            // 将问答系统的回复逐字添加到聊天界面中
            showChatGptResponse(data.completion.trim());
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// 逐字显示问答系统的回答
function showChatGptResponse(response) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    messageElement.classList.add('chatgpt-message');
    chatOutput.appendChild(messageElement);

    let index = 0;
    const delay = 10; // 每个字符的延迟时间间隔（毫秒）

    const intervalId = setInterval(() => {
        messageElement.innerHTML += response[index];
        index++;

        if (index >= response.length) {
            clearInterval(intervalId);
        }
    }, delay);
}