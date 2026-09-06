import os
import uuid
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from google import genai


load_dotenv(Path(__file__).with_name(".env"))

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

app = FastAPI()

sessions = {}