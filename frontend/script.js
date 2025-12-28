const API_URL = "http://127.0.0.1:8000";

async function sendQuestion() {
    const input = document.getElementById("user-input");
    const question = input.value.trim();

    if (!question) return;

    addMessage("user", question);
    input.value = "";

    const response = await fetch(`${API_URL}/ask`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ query: question }) 
    });

    const data = await response.json();
    addMessage("bot", data.answer);
}

function addMessage(role, text) {
    const box = document.getElementById("chat-box");
    const div = document.createElement("div");

    div.className = role;
    div.textContent = text;

    box.appendChild(div);
    box.scrollTop = box.scrollHeight;
}
