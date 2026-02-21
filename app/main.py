from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import httpx
from app.prompt import SYSTEM_PROMPT

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

class ChatRequest(BaseModel):
    message: str

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.post("/chat")
async def chat(req: ChatRequest):
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "llama3.2:3b",
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": req.message}
                ],
                "stream": False
            }
        )
    result = response.json()
    return {"response": result["message"]["content"]}
