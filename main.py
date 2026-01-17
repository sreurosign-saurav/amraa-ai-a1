from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ImageRequest(BaseModel):
    prompt: str

@app.get("/")
def root():
    return {"status": "LLAMA + Stable Diffusion Server Running"}

# 🦙 LLAMA CHAT
@app.post("/chat")
def chat_llama(req: ChatRequest):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": req.message,
            "stream": False
        }
    )

    return {
        "reply": response.json()["response"]
    }

# 🎨 STABLE DIFFUSION IMAGE
@app.post("/image")
def generate_image(req: ImageRequest):
    response = requests.post(
        "http://127.0.0.1:7860/sdapi/v1/txt2img",
        json={
            "prompt": req.prompt,
            "steps": 20
        }
    )

    image_base64 = response.json()["images"][0]
    return {"image": image_base64}

