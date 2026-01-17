from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

# Groq client (ENV se key)
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

@app.get("/")
def root():
    return {"status": "amraa ai server running"}

@app.post("/chat")
def chat(req: ChatRequest):
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are Amraa AI assistant."},
                {"role": "user", "content": req.message}
            ],
            temperature=0.7,
            max_tokens=300
        )

        reply = completion.choices[0].message.content
        return {"reply": reply}

    except Exception as e:
        return {"error": str(e)}

