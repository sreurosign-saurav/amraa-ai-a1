from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import base64
from groq import Groq

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key="PASTE_GROQ_API_KEY_HERE")

HF_API_KEY = "PASTE_HUGGINGFACE_API_KEY_HERE"
SD_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

class ChatRequest(BaseModel):
    message: str

class ImageRequest(BaseModel):
    prompt: str


@app.post("/chat")
def chat(req: ChatRequest):
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are Amraa AI assistant."},
            {"role": "user", "content": req.message}
        ]
    )
    return {"reply": completion.choices[0].message.content}


@app.post("/image")
def generate_image(req: ImageRequest):
    response = requests.post(
        SD_URL,
        headers=headers,
        json={"inputs": req.prompt}
    )

    image_base64 = base64.b64encode(response.content).decode("utf-8")
    return {"image": image_base64}


