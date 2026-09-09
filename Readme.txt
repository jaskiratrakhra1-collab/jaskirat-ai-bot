🤖 AI Chatbot

A full-stack AI chatbot web application built with FastAPI and Google Gemini, with a polished responsive interface and session-based conversation history.

✨ Features
🤖 AI-powered conversations using Google Gemini
💬 Session-based conversation history
🔄 New Chat functionality
📝 Markdown response rendering
💻 Code block rendering with Copy buttons
🔒 Secure API key management using .env
📱 Responsive design for desktop and mobile
⌨️ Enter to send and Shift + Enter for a new line
📏 Auto-expanding message input
⏳ Typing indicator while waiting for the AI
⚠️ Graceful handling of API/service errors
🌍 Custom Earth-themed glassmorphism interface
🛠️ Tech Stack

Frontend

HTML5
CSS3
JavaScript
Marked.js
DOMPurify

Backend

Python
FastAPI
Uvicorn
Pydantic

AI

Google Gemini API
google-genai

Other

python-dotenv
UUID-based sessions
In-memory conversation storage
🏗️ Architecture
                    Browser
                       │
                       ▼
              HTML / CSS / JavaScript
                       │
                       │ HTTP Requests
                       ▼
                  FastAPI
                       │
                 Session Lookup
                       │
                       ▼
              Conversation History
                       │
                       ▼
                 Gemini API
                       │
                       ▼
                 AI Response
                       │
                       ▼
                  FastAPI
                       │
                       ▼
                    Browser
📁 Project Structure
AI CHATBOT PROJECT/
│
├── App.py
├── .env
├── .gitignore
├── requirements.txt
│
├── templates/
│   └── index.html
│
└── static/
    ├── style.css
    ├── script.js
    │
    └── assets/
        └── earth.png
🔐 Environment Variables

The Gemini API key is stored in a .env file rather than directly inside the source code.

Create:

.env

and add:

GEMINI_API_KEY=your_api_key_here

Never commit .env to GitHub.

The project uses .gitignore to prevent the API key from being uploaded.

⚙️ Installation
1. Clone the repository
git clone <your-repository-url>
cd "AI CHATBOT PROJECT"
2. Create a virtual environment
python3 -m venv .venv
3. Activate it

macOS/Linux:

source .venv/bin/activate
4. Install dependencies
pip install -r requirements.txt
5. Configure the Gemini API key

Create a .env file:

GEMINI_API_KEY=your_api_key_here
6. Start the application
python3 -m uvicorn App:app --reload

The application will be available at:

http://127.0.0.1:8000
💬 How Sessions Work

Each new chat receives a unique UUID-based session ID.

Session ABC
    ↓
User message
    ↓
Conversation history
    ↓
Gemini

A different session gets its own history:

Session ABC → Conversation A

Session XYZ → Conversation B

This prevents conversations from sharing context with each other.

Current limitation

Conversation history is stored in memory:

sessions = {}

Therefore:

Starting a new chat creates a new session.
Different sessions have separate conversation histories.
Restarting the FastAPI server clears all stored conversations.
There is currently no database or persistent user account system.

Persistent storage and authentication can be added in a future version.

⚠️ API Usage Limits

The application currently uses a Gemini API project with its applicable usage limits.

If the chatbot displays:

⚠️ AI is temporarily unavailable. Please try again later.

it may mean that the Gemini API usage/rate limit has been reached.

In that case, wait for the applicable quota/rate limit to reset and try again later.

Because the current application uses a shared Gemini API project, API usage is not independently allocated per browser session.

🛡️ Security

The application follows basic API-key security practices:

API keys are stored in .env
.env is excluded through .gitignore
The Gemini key is never exposed in frontend JavaScript
AI-generated Markdown is sanitized with DOMPurify before being inserted into the page
🚀 Future Improvements

Planned improvements include:

User authentication
Persistent conversation storage
Database integration
Per-user rate limiting
Better API quota handling
Streaming AI responses
Conversation history sidebar
Production deployment
More advanced AI features
📌 Project Status

Current status: Functional MVP

The core chatbot, session management, Gemini integration, responsive interface, Markdown rendering, code-copy functionality, and error handling are implemented.

The next major step is production deployment.

👨‍💻 Author

Aryan Bhasin

Built as a full-stack AI project to explore AI integration, backend development, API communication, session management, frontend engineering, and deployment.