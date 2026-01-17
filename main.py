from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import requests
import base64
import os
import time

app = FastAPI(title="Amraa AI Server")

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
HF_HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

class ChatRequest(BaseModel):
    message: str

class ImageRequest(BaseModel):
    prompt: str

@app.get("/")
def root():
    return {"status": "Amraa AI server running"}

# =========================
# CHAT
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
                        "If someone asks which AI model you use or similar, reply ONLY: "
                        "'Saurav Goswami dwara viksit Amraa.Tech ka Amraa A1 AI model.' "
                        "If asked who created you, reply ONLY: "
                        "'I am Amraa AI, a private AI assistant developed and owned by Saurav.' "
                        "Do not add anything else."
                    )
                },
                {"role": "user", "content": req.message}
            ],
            temperature=0.7,
            max_tokens=250
        )

        return {"reply": response.choices[0].message.content.strip()}

    except Exception:
        return {"error": "Chat service unavailable"}

# =========================
# IMAGE (FINAL FIX)
# =========================
@app.post("/image")
def image(req: ImageRequest):
    for _ in range(3):
        try:
            r = requests.post(
                SD_URL,
                headers=HF_HEADERS,
                json={"inputs": req.prompt},
                timeout=120
            )

            content_type = r.headers.get("content-type", "")

            # JSON response = loading or error
            if "application/json" in content_type:
                data = r.json()
                if "loading" in str(data).lower():
                    time.sleep(10)
                    continue
                return {"error": "Image generation failed"}

            # Image response
            img_base64 = base64.b64encode(r.content).decode("utf-8")
            return {
                "type": "image",
                "url": f"data:image/png;base64,{img_base64}"
            }

        except Exception:
            time.sleep(5)

    return {"error": "Model busy, try again later"}
