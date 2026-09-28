# Jaskirat AI Bot

A full-stack AI chatbot built with **FastAPI** and **Google Gemini**, with a modern glassmorphism interface, session-based conversations, Markdown support, and code-block handling.

The project is designed as a lightweight AI application that demonstrates how a frontend, backend API, session management, and an LLM service can work together.

---

## Features

- 🤖 AI-powered conversations using Google Gemini
- 💬 Session-based conversation history
- 🔄 Start a new conversation with one click
- 📝 Markdown response rendering
- 💻 Code block rendering with copy functionality
- 🔒 Environment-based API key management
- 📱 Responsive interface for desktop and mobile
- ⌨️ Enter to send messages
- ↵ Shift + Enter for a new line
- 📏 Auto-expanding message input
- ⏳ Typing indicator while waiting for responses
- ⚠️ Graceful API and service error handling
- 🌍 Earth-themed glassmorphism interface

---

## Tech Stack

### Frontend

- HTML5
- CSS3
- JavaScript
- Marked.js
- DOMPurify

### Backend

- Python
- FastAPI
- Uvicorn
- Pydantic

### AI

- Google Gemini API
- `google-genai`

### Supporting Technologies

- `python-dotenv`
- UUID-based sessions
- In-memory conversation storage

---

## Architecture

```text
Browser
   │
   │ HTML / CSS / JavaScript
   ▼
FastAPI Backend
   │
   ├── Session Management
   │
   ├── Conversation History
   │
   ▼
Google Gemini API
   │
   ▼
AI Response
   │
   ▼
FastAPI
   │
   ▼
Browser
