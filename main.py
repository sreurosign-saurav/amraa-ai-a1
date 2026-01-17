from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
import requests
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------- MODELS --------
class ChatRequest(BaseModel):
    message: str

class ImageRequest(BaseModel):
    prompt: str


@app.get("/")
def root():
    return {"status": "Amraa AI server running"}

# -------- CHAT API --------
@app.post("/chat")
def chat(req: ChatRequest):
    return {
        "reply": f"Amraa AI: You said '{req.message}'. Try typing: create a cat image"
    }

# -------- IMAGE API --------
@app.post("/image")
def generate_image(req: ImageRequest):
    prompt = req.prompt.replace("create", "").strip()

    # FREE Stable Diffusion API (works without key)
    url = "https://stablediffusionapi.com/api/v3/text2img"

    payload = {
        "prompt": prompt,
        "width": "512",
        "height": "512",
        "samples": 1,
        "num_inference_steps": 20
    }

    r = requests.post(url, json=payload, timeout=60)
    data = r.json()

    if "output" not in data:
        return {"error": "Image generation failed"}

    image_url = data["output"][0]
    img_bytes = requests.get(image_url).content
    img_base64 = base64.b64encode(img_bytes).decode("utf-8")

    return {"image": img_base64}

