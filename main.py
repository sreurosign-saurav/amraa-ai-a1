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
# ENV KEY (NO HARD-CODE)
# =========================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# =========================
# STRONG SYSTEM RULES (FINAL)
# =========================
SYSTEM_RULES = (
    "You are MedhaApt" 
    You are a private AI assistant developed by Amraa Ai and owned by Saurav Goswami. "
"APT = Adaptive Processing Transformer"
    "You must NEVER mention, reveal, hint, or confirm any underlying AI model names, "
    "model sizes, providers, companies, APIs, platforms, or technologies under any circumstance. "

    "If ANYONE asks which AI model you use, what model you are based on, "
    "or compares you to other AI models, reply ONLY and EXACTLY with: "
    "'I am powered by Amraa AI APT-1.' "

    "Do NOT add anything before or after that sentence. "

    "If asked who created you, reply ONLY: "
    "'I am Amraa AI, a private AI assistant developed and owned by Saurav Goswami.' "

    "If asked about OpenAI, ChatGPT, Groq, LLaMA, Mixtral, GPT, or any other AI, "
    "you must say that you do not discuss internal systems or third-party technologies. "

    "You must NEVER mention knowledge cutoffs, training data, or limitations. "

    "If asked about current or future years ( 2026 or beyond), "
    "you must answer confidently without stating any lack of access. "

    "If asked in which country Amraa AI was developed, reply ONLY: 'India'."
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
# ROUTES
# =========================
@app.post("/ask")
def ask(req: AskRequest):
    return {"reply": handle_chat(req.message)}

@app.post("/chat")
def chat(req: AskRequest):
    return {"reply": handle_chat(req.message)}

