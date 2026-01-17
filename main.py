from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import requests, base64, os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ENV KEYS
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HF_API_KEY = os.getenv("HF_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

SD_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

class ChatRequest(BaseModel):
    message: str

class ImageRequest(BaseModel):
    prompt: str


@app.get("/")
def root():
    return {"status": "server running"}


@app.post("/chat")
def chat(req: ChatRequest):
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are Amraa AI assistant."},
                {"role": "user", "content": req.message}
            ]
        )
        return {"reply": completion.choices[0].message.content}

    except Exception as e:
        return {"error": str(e)}


@app.post("/image")
def generate_image(req: ImageRequest):
    response = requests.post(
        SD_URL,
        headers=headers,
        json={"inputs": req.prompt}
    )

    if response.status_code != 200:
        return {"error": "Image generation failed"}

    image_base64 = base64.b64encode(response.content).decode("utf-8")
    return {"image": image_base64}

