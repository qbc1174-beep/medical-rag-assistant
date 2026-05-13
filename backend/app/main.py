from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {
        "message": "Medical RAG Assistant Backend Running"
    }


@app.post("/ask")
def ask_question(payload: QuestionRequest):
    return {
        "answer": "This is a sample medical response.",
        "citations": ["WHO"],
        "confidence": "high",
        "warning": "Not a medical diagnosis."
    }