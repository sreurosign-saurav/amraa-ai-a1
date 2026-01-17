from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import requests
import base64
import os

# ---------------- APP ----------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------- KEYS ------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HF_API_KEY = os.getenv("HF_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

# --------- STABLE DIFFUSION ----------
SD_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
SD_HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

# ------------- MODELS ----------------
class ChatRequest(BaseModel):
    message: str

class ImageRequest(BaseModel):
    prompt: str

# ------------- ROOT ------------------
@app.get("/")
def root():
    return {"status": "Amraa AI server running"}

# ------------- CHAT ------------------
@app.post("/chat")
def chat(req: ChatRequest):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Amraa AI, a private AI assistant developed by Saurav. "
                        "You were created and owned by Amraa AI. "
                        "You must NEVER mention Meta, Facebook, LLaMA, Groq, or any other company. "
                        "If asked who created or owns you, always reply: "
                        "'I am Amraa AI, developed and owned by Saurav.'"
                    )
                },
                {"role": "user", "content": req.message}
            ],
            temperature=0.7,
            max_tokens=300
        )

        return {"reply": response.choices[0].message.content}

    except Exception as e:
        return {"error": str(e)}

# ------------- IMAGE -----------------
@app.post("/image")
def image(req: ImageRequest):
    try:
        r = requests.post(
            SD_URL,
            headers=SD_HEADERS,
            json={"inputs": req.prompt},
            timeout=90
        )

        # HF kabhi error JSON bhejta hai
        if "application/json" in r.headers.get("content-type", ""):
            return {"error": r.json()}

        img_base64 = base64.b64encode(r.content).decode("utf-8")
        return {"image": img_base64}

    except Exception as e:
        return {"error": str(e)}

