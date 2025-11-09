document.getElementById("chat-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const message = document.getElementById("message").value;
    const tripcode = document.getElementById("tripcode").value;

    if (!username || !message) return;

    await fetch("/chat/send", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, message, tripcode })
    });

    document.getElementById("message").value = "";
    loadMessages();
});

async function loadMessages() {
    const res = await fetch("/chat/get");
    const data = await res.json();

    const chatBox = document.getElementById("chat-box");
    chatBox.innerHTML = "";

    data.forEach(msg => {
        const p = document.createElement("p");
        p.innerHTML = `<strong>${msg.username}</strong> ${msg.trip_id}: ${msg.message}`;
        chatBox.appendChild(p);
    });

    chatBox.scrollTop = chatBox.scrollHeight;
}

setInterval(loadMessages, 2000);
loadMessages();
