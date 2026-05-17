from fastapi import FastAPI
from pydantic import BaseModel

from app.rag import generate_medical_answer

app = FastAPI(
    title="SafeMed AI",
    description="Evidence-grounded medical RAG assistant",
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