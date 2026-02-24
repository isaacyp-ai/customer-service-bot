from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import httpx
from app.prompt import SYSTEM_PROMPT

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

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
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    for msg in req.history:
        messages.append({"role": msg.role, "content": msg.content})
    
    messages.append({"role": "user", "content": req.message})

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "llama3.2:3b",
                "messages": messages,
                "stream": False
            }
        )
    result = response.json()
    return {"response": result["message"]["content"]}
