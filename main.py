from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import base64

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        return {
            "reply": "Creating image, please wait..."
        }

    return {
        "reply": f"Amraa AI: You said '{req.message}'"
    }


@app.post("/image")
def image(req: ImageRequest):
    prompt = req.prompt.replace("create", "").replace("generate", "").strip()

    url = "https://stablediffusionapi.com/api/v3/text2img"

    payload = {
        "prompt": prompt,
        "width": "512",
        "height": "512",
        "samples": 1,
        "num_inference_steps": 20
    }

    try:
        r = requests.post(url, json=payload, timeout=90)
        data = r.json()

        if "output" not in data:
            return {"error": "Image generation failed"}

        image_url = data["output"][0]
        img_bytes = requests.get(image_url).content
        img_base64 = base64.b64encode(img_bytes).decode("utf-8")

        return {"image": img_base64}

    except Exception as e:
        return {"error": str(e)}
