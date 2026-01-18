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

client = Groq(api_key=GROQ_API_KEY)

SD_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-2"
HF_HEADERS = {
    "Content-Type": "application/json"
}

# =========================
# SYSTEM RULES (SINGLE SOURCE)
# =========================
SYSTEM_RULES = (
    "You are Amraa AI, a private AI assistant developed and owned by Saurav Goswami. "
    "You must NEVER mention or reveal any underlying AI model names, providers, "
    "companies, APIs, or technologies such as LLaMA, Meta, Groq, HuggingFace, "
    "Stable Diffusion, or any similar terms. "
    "If someone asks which AI model you use or similar, reply ONLY: "
    "'I Am using Amraa A1 Model Developed By Amraa AI, Owned by Saurav Goswami.' "
    "If asked who created you, reply ONLY: "
    "'I am Amraa AI, a private AI assistant developed and owned by Saurav.' "
    "Do not add anything else. "
    "LANGUAGE RULE: When replying in Hindi, English, Hinglish, or any other language, "
    "ensure correct spelling, proper grammar, natural sentence structure, and fluent language."
)

class ChatRequest(BaseModel):
    message: str

class AskRequest(BaseModel):
    message: str

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
                {"role": "system", "content": SYSTEM_RULES},
                {"role": "user", "content": req.message}
            ],
            temperature=0.7,
            max_tokens=250
        )
        return {"reply": response.choices[0].message.content.strip()}
    except Exception:
        return {"error": "Chat service unavailable"}

# =========================
# ASK (TEXT + IMAGE)
# =========================
@app.post("/ask")
def ask(req: AskRequest):
    reply_text = ""
    image_url = None

    # 1️⃣ CHAT
    try:
        chat_res = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_RULES},
                {"role": "user", "content": req.message}
            ],
            temperature=0.7,
            max_tokens=200
        )
        reply_text = chat_res.choices[0].message.content.strip()
    except Exception:
        reply_text = "I am Amraa AI Assistant."

    # 2️⃣ IMAGE TRY (NON-BLOCKING)
    for _ in range(2):
        try:
            r = requests.post(
                SD_URL,
                headers=HF_HEADERS,
                json={"inputs": req.message},
                timeout=120
            )
            if (
                r.status_code == 200
                and not r.headers.get("content-type", "").startswith("application/json")
            ):
                img_base64 = base64.b64encode(r.content).decode()
                image_url = f"data:image/png;base64,{img_base64}"
                break
            time.sleep(5)
        except Exception:
            image_url = None

    return {
        "reply": reply_text,
        "image": image_url
    }
