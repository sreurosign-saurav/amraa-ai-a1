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
HEADERS = {
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
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are Amraa AI assistant."},
            {"role": "user", "content": req.message}
        ]
    )
    return {
        "reply": completion.choices[0].message.content
    }

@app.post("/image")
def image(req: ImageRequest):
    response = requests.post(
        SD_URL,
        headers=HEADERS,
        json={"inputs": req.prompt},
        timeout=60
    )
    image_base64 = base64.b64encode(response.content).decode("utf-8")
    return {
        "image": image_base64
    }

