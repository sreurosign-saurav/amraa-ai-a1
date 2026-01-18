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

# ENV KEY
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# =========================
# SYSTEM RULES (UNCHANGED)
# =========================
SYSTEM_RULES = (
    "You are Amraa AI, a private AI assistant developed and owned by Saurav Goswami. "
    "You must NEVER mention or reveal any underlying AI model names, providers, "
    "companies, APIs, or technologies. "
    "If someone asks which AI model you use, reply ONLY: "
    "'I Am using Amraa A1 Model Developed By Amraa AI, Owned by Saurav Goswami.' "
    "If asked who created you, reply ONLY: "
    "'I am Amraa AI, a private AI assistant developed and owned by Saurav.' "
)

class AskRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "Amraa AI server running"}

# =========================
# CORE FUNCTION
# =========================
def handle_chat(message: str):
    try:
        chat_res = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_RULES},
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            max_tokens=200
        )
        return chat_res.choices[0].message.content.strip()
    except Exception as e:
        print("CHAT ERROR:", e)
        return "Server error. Please try again."

# =========================
# BOTH ROUTES (FIX)
# =========================
@app.post("/ask")
def ask(req: AskRequest):
    return {"reply": handle_chat(req.message)}

@app.post("/chat")   # 🔥 THIS WAS MISSING
def chat(req: AskRequest):
    return {"reply": handle_chat(req.message)}
