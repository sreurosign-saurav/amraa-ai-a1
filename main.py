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

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "Amraa AI server running"}

# =========================
# CHAT (HARD RULED BACKEND)
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
                        "'I Am using Amraa A1 Model Developed By Amraa AI, Owned by Saurav Goswami.' "
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
