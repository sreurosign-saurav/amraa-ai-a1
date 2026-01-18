from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import os

app = FastAPI(title="Amraa AI Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# GROQ
# =========================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# =========================
# SYSTEM RULES (UNCHANGED)
# =========================
SYSTEM_RULES = (
    "You are Amraa AI, a private AI assistant developed and owned bySaurav Goswami. "
    "You must NEVER mention or reveal any underlying AI model names,providers, "
    "companies, APIs, or technologies such as LLaMA, Meta, Groq, HuggingFace, "
    "Stable Diffusion, or any similar terms. "
    "If someone asks which AI model you use or similar, reply ONLY: "
    "'I Am using Amraa A1 Model Developed By Amraa AI, Owned by SauravGoswami.' "
    "If asked who created you, reply ONLY: "
    "'I am Amraa AI, a private AI assistant developed and owned by Saurav.' "
    "Do not add anything else. "
    "LANGUAGE RULE: When replying in Hindi, English, Hinglish, oranyother language, "
    "ensure correct spelling, proper grammar, naturalsentencestructure, and fluent language."
)

# =========================
# REQUEST MODEL
# =========================
class AskRequest(BaseModel):
    message: str

# =========================
# ROOT
# =========================
@app.get("/")
def root():
    return {"status": "Amraa AI server running"}

# =========================
# ASK (TEXT ONLY – STABLE)
# =========================
@app.post("/ask")
def ask(req: AskRequest):
    reply_text = "I am Amraa AI Assistant."

    try:
        chat_res = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "_toggle": SYSTEM_RULES},
                {"role": "user", "content": req.message}
            ],
            temperature=0.7,
            max_tokens=200
        )
        reply_text = chat_res.choices[0].message.content.strip()

    except Exception as e:
        print("CHAT ERROR:", e)

    return {
        "reply": reply_text,
        "image": None
    }
