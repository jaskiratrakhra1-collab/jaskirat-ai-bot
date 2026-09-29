import os
import uuid
import time

from pathlib import Path
from dotenv import load_dotenv

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from google import genai
from google.genai import types, errors

from pydantic import BaseModel


class ChatRequest(BaseModel):
    session_id: str
    message: str


# Load environment variables
load_dotenv(Path(__file__).with_name(".env"))

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not configured")


# Gemini client
client = genai.Client(api_key=api_key)


# FastAPI
app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(directory="templates")


# Temporary in-memory sessions
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

    return {
        "session_id": session_id
    }


@app.post("/chat")
def chat(request: ChatRequest):

    # Validate message
    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )

    # Validate session
    if request.session_id not in sessions:
        raise HTTPException(
            status_code=404,
            detail="Invalid session ID"
        )

    history = sessions[request.session_id]

    # Add user's message
    history.append(
        types.Content(
            role="user",
            parts=[
                types.Part(text=request.message)
            ]
        )
    )

    # Retry Gemini request
    max_retries = 3
    bot_reply = None

    for attempt in range(max_retries):

        try:

            print(
                f"Gemini request attempt "
                f"{attempt + 1}/{max_retries}"
            )

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=history
            )

            bot_reply = response.text

            break

        except errors.APIError as e:

            print(
                f"Gemini API error: "
                f"code={e.code}, message={e.message}"
            )

            # Retry temporary errors
            if e.code in [429, 500, 502, 503, 504]:

                if attempt < max_retries - 1:

                    delay = 2 ** attempt

                    print(
                        f"Retrying in {delay} seconds..."
                    )

                    time.sleep(delay)

                    continue

            # Permanent / final error
            break

        except Exception as e:

            print("Unexpected Gemini error:", e)

            if attempt < max_retries - 1:

                delay = 2 ** attempt

                print(
                    f"Retrying in {delay} seconds..."
                )

                time.sleep(delay)

                continue

            break

    # Gemini failed after retries
    if bot_reply is None:

        # Remove user's message because no response was generated
        history.pop()

        raise HTTPException(
            status_code=503,
            detail="AI service is temporarily unavailable. Please try again."
        )

    # Save Gemini response
    history.append(
        types.Content(
            role="model",
            parts=[
                types.Part(text=bot_reply)
            ]
        )
    )

    return {
        "response": bot_reply
    }
