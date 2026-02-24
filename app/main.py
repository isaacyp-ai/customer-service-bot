from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import httpx
import os
from dotenv import load_dotenv
from app.prompt import SYSTEM_PROMPT

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

MODEL = os.getenv("MODEL", "llama3.2:3b")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Message]] = []

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.post("/chat")
async def chat(req: ChatRequest):
    messages = []
    for msg in req.history:
        messages.append({"role": msg.role, "content": msg.content})
    messages.append({"role": "user", "content": req.message})

    if MODEL.startswith("gpt"):
        return await call_openai(messages)
    elif MODEL.startswith("claude"):
        return await call_anthropic(messages)
    else:
        return await call_ollama(messages)

async def call_ollama(messages):
    ollama_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "http://localhost:11434/api/chat",
            json={"model": MODEL, "messages": ollama_messages, "stream": False}
        )
    result = response.json()
    return {"response": result["message"]["content"]}

async def call_openai(messages):
    openai_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={"model": MODEL, "messages": openai_messages}
        )
    result = response.json()
    return {"response": result["choices"][0]["message"]["content"]}

async def call_anthropic(messages):
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "max_tokens": 1024,
                "system": SYSTEM_PROMPT,
                "messages": messages
            }
        )
    result = response.json()
    return {"response": result["content"][0]["text"]}
