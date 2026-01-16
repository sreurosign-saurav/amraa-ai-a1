from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "amraa ai server running"}

@app.post("/chat")
def chat(req: ChatRequest):
    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "llama3-8b-8192",
                "messages": [
                    {"role": "user", "content": req.message}
                ],
            },
            timeout=30
        )

        data = r.json()
        return {
            "reply": data["choices"][0]["message"]["content"]
        }

    except Exception as e:
        return {
            "error": str(e)
        }


