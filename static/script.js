let sessionId = null;

const chatForm = document.getElementById("chat-form");
const messageInput = document.getElementById("message-input");
const chatBox = document.getElementById("chat-box");
const sendButton = chatForm.querySelector("button");
const newChatButton = document.getElementById("new-chat-button");

sendButton.disabled = true;

/* =========================
   CREATE SESSION
========================= */

async function createSession() {
    const response = await fetch("/session", {
        method: "POST"
    });

    if (!response.ok) {
        throw new Error("Failed to create session");
    }

    const data = await response.json();

    sessionId = data.session_id;
}

/* =========================
   INITIAL SESSION
========================= */

createSession()
    .then(() => {
        sendButton.disabled = false;
    })
    .catch((error) => {
        console.error(error);
    });

/* =========================
   NEW CHAT
========================= */

newChatButton.addEventListener("click", async () => {
    sendButton.disabled = true;
    newChatButton.disabled = true;

    try {
        await createSession();

        chatBox.innerHTML = `
            <div class="message bot-message">
                Hello! How can I help you?
            </div>
        `;

        messageInput.value = "";
        messageInput.style.height = "46px";

        messageInput.focus();

    } catch (error) {
        console.error(error);

        const errorMessage = document.createElement("div");

        errorMessage.className = "message bot-message";

        errorMessage.textContent =
            "⚠️ Unable to start a new chat. Please try again.";

        chatBox.appendChild(errorMessage);

    } finally {
        newChatButton.disabled = false;

        if (sessionId) {
            sendButton.disabled = false;
        }
    }
});

/* =========================
   SEND MESSAGE
========================= */

chatForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    if (!sessionId) {
        return;
    }

    const message = messageInput.value.trim();

    if (!message) {
        return;
    }

    messageInput.value = "";
    messageInput.style.height = "46px";

    sendButton.disabled = true;

    /* User message */

    const userMessage = document.createElement("div");

    userMessage.className = "message user-message";

    userMessage.textContent = message;

    chatBox.appendChild(userMessage);

    chatBox.scrollTop = chatBox.scrollHeight;

    /* Typing indicator */

    const typingMessage = document.createElement("div");

    typingMessage.className = "message bot-message";

    typingMessage.innerHTML =
        '<span class="typing-dots">● ● ●</span>';

    chatBox.appendChild(typingMessage);

    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        const response = await fetch("/chat", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                session_id: sessionId,
                message: message
            })
        });

        if (!response.ok) {
            throw new Error("AI request failed");
        }

        const data = await response.json();

        /* Remove typing indicator */

        typingMessage.remove();

        /* Bot message */

        const botMessage = document.createElement("div");

        botMessage.className = "message bot-message";

        botMessage.innerHTML = DOMPurify.sanitize(
            marked.parse(data.response)
        );

        /* Code blocks */

        const codeBlocks = botMessage.querySelectorAll("pre");

        codeBlocks.forEach((block) => {
            const copyButton = document.createElement("button");

            copyButton.textContent = "Copy";

            copyButton.className = "copy-code-button";

            copyButton.addEventListener("click", async () => {
                const codeElement = block.querySelector("code");

                if (!codeElement) {
                    return;
                }

                try {
                    await navigator.clipboard.writeText(
                        codeElement.innerText
                    );

                    copyButton.textContent = "Copied ✓";

                    setTimeout(() => {
                        copyButton.textContent = "Copy";
                    }, 1500);

                } catch (error) {
                    console.error(error);

                    copyButton.textContent = "Failed";

                    setTimeout(() => {
                        copyButton.textContent = "Copy";
                    }, 1500);
                }
            });

            block.appendChild(copyButton);
        });

        chatBox.appendChild(botMessage);

        chatBox.scrollTop = chatBox.scrollHeight;

    } catch (error) {
        console.error(error);

        typingMessage.remove();

        const errorMessage = document.createElement("div");

        errorMessage.className = "message bot-message";

        errorMessage.textContent =
            "⚠️ AI is temporarily unavailable. Please try again later.";

        chatBox.appendChild(errorMessage);

        chatBox.scrollTop = chatBox.scrollHeight;

    } finally {
        sendButton.disabled = false;
    }
});

/* =========================
   ENTER / SHIFT + ENTER
========================= */

messageInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();

        chatForm.requestSubmit();
    }
});

/* =========================
   AUTO-RESIZE TEXTAREA
========================= */

messageInput.addEventListener("input", () => {
    messageInput.style.height = "auto";

    messageInput.style.height =
        Math.min(messageInput.scrollHeight, 140) + "px";
});