from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import requests
import base64
import os

# =========================
# App Init
# =========================
app = FastAPI(title="Amraa AI Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Environment Keys
# =========================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HF_API_KEY = os.getenv("HF_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

SD_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
HF_HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

# =========================
# Request Models
# =========================
class ChatRequest(BaseModel):
    message: str

class ImageRequest(BaseModel):
    prompt: str

# =========================
# Root
# =========================
@app.get("/")
def root():
    return {"status": "Amraa AI server running"}

# =========================
# CHAT ENDPOINT (LOCKED IDENTITY)
# =========================
@app.post("/chat")
def chat(req: ChatRequest):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Amraa AI, a private AI assistant developed and owned by Saurav Goswami. "
                        "You must NEVER mention or reveal any underlying AI model names, providers, "
                        "companies, APIs, or technologies such as LLaMA, Meta, Groq, HuggingFace, "
                        "Stable Diffusion, or any similar terms. "
                        "If a user asks about your model, training data, internal architecture, "
                        "or what you are built on, you must respond ONLY with a high-level, "
                        "non-technical answer. "
                        "If asked directly about model names, you must reply: "
                        "'I am Amraa AI, a private AI assistant developed and owned by Saurav.' "
                        "Do not add any extra explanation."
                    )
                },
                {"role": "user", "content": req.message}
            ],
            temperature=0.7,
            max_tokens=250
        )

        return {
            "reply": response.choices[0].message.content.strip()
        }

    except Exception as e:
        return {"error": "Chat service temporarily unavailable"}

# =========================
# IMAGE GENERATION ENDPOINT
# =========================
@app.post("/image")
def image(req: ImageRequest):
    try:
        r = requests.post(
            SD_URL,
            headers=HF_HEADERS,
            json={"inputs": req.prompt},
            timeout=60
        )

        if r.status_code != 200:
            return {"error": "Image generation failed"}

        img_base64 = base64.b64encode(r.content).decode("utf-8")
        return {"image": img_base64}

    except Exception:
        return {"error": "Image service unavailable"}
