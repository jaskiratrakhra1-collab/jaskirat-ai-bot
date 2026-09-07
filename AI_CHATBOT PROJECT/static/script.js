let sessionId = null;

const chatForm = document.getElementById("chat-form");
const messageInput = document.getElementById("message-input");
const chatBox = document.getElementById("chat-box");
async function createSession() {
    const response = await fetch("/session", {
        method: "POST"
    });

    const data = await response.json();

    sessionId = data.session_id;
}
createSession();