async function fetchMessages() {
    const res = await fetch('/chat/get');
    const messages = await res.json();
    const box = document.getElementById('chatbox');
    box.innerHTML = messages.map(m=> `<p><b>${m.username} ${m.trip_id}:</b> ${m.message}</p>`).join('');
}

async function sendMessage() {
    const username = document.getElementById('username').value || "Guest";
    const text = document.getElementById('message').value;
    if (!text.trim()) return;

    await fetch('/chat/send', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username, text})
    });

    document.getElementById('message').value = '';
    fetchMessages();
}


document.getElementById('sendBtn').onclick = sendMessage;
setInterval(fetchMessages, 3000);
fetchMessages();