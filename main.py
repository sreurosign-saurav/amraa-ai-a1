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

HF_MODEL_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
HF_HEADERS = {
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
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Amraa AI, a helpful, friendly AI assistant. "
                    "Never repeat the user's message. "
                    "Always answer naturally like a human."
                )
            },
            {
                "role": "user",
                "content": req.message
            }
        ],
        temperature=0.7,
        max_tokens=200
    )

    return {
        "reply": response.choices[0].message.content.strip()
    }

@app.post("/image")
def image(req: ImageRequest):
    r = requests.post(
        HF_MODEL_URL,
        headers=HF_HEADERS,
        json={"inputs": req.prompt},
        timeout=60
    )

    image_base64 = base64.b64encode(r.content).decode("utf-8")
    return {"image": image_base64}
