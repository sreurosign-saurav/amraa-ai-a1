from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import base64
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

HF_API_KEY = os.getenv("HF_API_KEY")

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
    return {"status": "Amraa AI backend running"}


@app.post("/chat")
def chat(req: ChatRequest):
    msg = req.message.lower()

    if msg.startswith("create") or msg.startswith("generate"):
        return {"reply": "Creating image, please wait..."}

    return {"reply": f"Amraa AI: {req.message}"}


@app.post("/image")
def image(req: ImageRequest):
    payload = {
        "inputs": req.prompt
    }

    try:
        response = requests.post(
            HF_MODEL_URL,
            headers=HF_HEADERS,
            json=payload,
            timeout=120
        )

        if response.status_code != 200:
            return {"error": "HuggingFace API error"}

        img_base64 = base64.b64encode(response.content).decode("utf-8")
        return {"image": img_base64}

    except Exception as e:
        return {"error": str(e)}
