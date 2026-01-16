from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HF_API_KEY = os.getenv("HF_API_KEY")

class ChatRequest(BaseModel):
    message: str

class ImageRequest(BaseModel):
    prompt: str

@app.get("/")
def root():
    return {"status": "AMRAA AI SERVER LIVE"}

@app.get("/check-key")
def check_key():
    return {
        "groq_key": "FOUND" if GROQ_API_KEY else "MISSING"
    }

@app.post("/chat")
def chat(req: ChatRequest):
    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama3-8b-8192",
            "messages": [{"role": "user", "content": req.message}]
        }
    )

    data = r.json()

    if "choices" not in data:
        return {
            "reply": "API ERROR",
            "raw": data
        }

    return {
        "reply": data["choices"][0]["message"]["content"]
    }

@app.post("/image")
def image(req: ImageRequest):
    r = requests.post(
        "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0",
        headers={"Authorization": f"Bearer {HF_API_KEY}"},
        json={"inputs": req.prompt}
    )
    return {"image": r.content.hex()}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)


