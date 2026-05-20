# =========================================================
# Banking AI Chatbot API
# =========================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from chatbot import chat

# ---------------- APP ----------------
app = FastAPI(
    title="Banking AI Chatbot API",
    version="1.0"
)

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- REQUEST ----------------


class Query(BaseModel):
    question: str

# ---------------- HEALTH ----------------


@app.get("/")
def home():
    return {"status": "running"}

# ---------------- CHAT ENDPOINT ----------------


@app.post("/chat")
def chat_api(q: Query):

    try:
        result = chat(q.question)

        return {
            "status": "success",
            "question": q.question,
            "answer": result["answer"],
            "strategy": result["strategy"]
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "strategy": "error"
        }
