from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import base64
import os
from groq import Groq

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HF_API_KEY = os.getenv("HF_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

SD_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
SD_HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

class ChatRequest(BaseModel):
    message: str

class ImageRequest(BaseModel):
    prompt: str

@app.get("/")
def root():
    return {"status": "Amraa AI server running"}

@app.post("/chat")
def chat(req: ChatRequest):
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are Amraa AI Assistant."},
                {"role": "user", "content": req.message}
            ]
        )
        return {"reply": completion.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}

@app.post("/image")
def image(req: ImageRequest):
    try:
        r = requests.post(
            SD_URL,
            headers=SD_HEADERS,
            json={"inputs": req.prompt},
            timeout=60
        )
        img_base64 = base64.b64encode(r.content).decode("utf-8")
        return {"image": img_base64}
    except Exception as e:
        return {"error": str(e)}

