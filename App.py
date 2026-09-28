import os
import uuid
from pathlib import Path
from dotenv import load_dotenv
from httpx import request
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from google import genai
from google.genai import types
from pydantic import BaseModel

class ChatRequest(BaseModel):
    session_id: str
    message: str


load_dotenv(Path(__file__).with_name(".env"))

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not configured")

client = genai.Client(api_key=api_key)
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

sessions = {}

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )
@app.post("/session")
def create_session():
    session_id = str(uuid.uuid4())

    sessions[session_id] = []

    return {"session_id": session_id}


@app.post("/chat")
def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )
    if request.session_id not in sessions:
        raise HTTPException(
            status_code=404,
            detail="Invalid session ID"
        )
    history = sessions[request.session_id]

    history.append(
        types.Content(
            role="user",
            parts=[types.Part(text=request.message)]
        )
    )

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=history
        )
        bot_reply = response.text
    except Exception as e:
        print("Gemini error:", e)
        history.pop()
        raise HTTPException(
            status_code=503,
            detail="AI service is temporarily unavailable"
        )

    history.append(
        types.Content(
            role="model",
            parts=[types.Part(text=bot_reply)]
        )
    )
    return {"response": bot_reply}