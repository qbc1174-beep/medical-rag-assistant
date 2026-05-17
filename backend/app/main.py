import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.rag import generate_medical_answer

app = FastAPI(
    title="SafeMed AI",
    description="Evidence-grounded medical RAG assistant",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        os.getenv("FRONTEND_URL"),
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {
        "message": "Medical RAG Assistant Backend Running"
    }


@app.post("/ask")
def ask_question(payload: QuestionRequest):
    result = generate_medical_answer(payload.question)

    return {
        "answer": result["answer"],
        "confidence": result["confidence"],
        "refused": result["refused"],
        "sources": result["sources"],
        "warning": "Not a medical diagnosis. Responses are evidence-grounded but should be clinically verified.",
    }