
import os

from dotenv import load_dotenv
from groq import Groq

from retriever import retrieve_medical_evidence

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

SYSTEM_PROMPT = """
You are a safety-first clinical information assistant for doctors.

Rules:
- Answer ONLY using the retrieved evidence.
- Do NOT use outside medical knowledge.
- Do NOT invent facts.
- Do NOT give a final diagnosis.
- If evidence is insufficient, say: "I don't know based on current evidence."
- Keep the answer concise and clinically useful.
"""

def build_context(evidence_items):
    context_parts = []

    for index, item in enumerate(evidence_items, start=1):
        metadata = item["metadata"]

        context_parts.append(
            f"""
            Source {index}
            Title: {metadata.get("title")}
            Source: {metadata.get("source")}
            Year: {metadata.get("year")}
            Page: {metadata.get("page")}
            Evidence:
            {item["content"]}
            """
        )

    return "\n\n".join(context_parts)


def generate_medical_answer(question: str):
    retrieval = retrieve_medical_evidence(question)

    if retrieval["refused"]:
        return {
            "answer": "Insufficient evidence found. I don't know based on current evidence.",
            "refused": True,
            "confidence": retrieval["confidence"],
            "sources": [],
        }

    context = build_context(retrieval["evidence"])

    user_prompt = f"""
        Clinical question:
        {question}

        Retrieved evidence:
        {context}

        Answer format:
        - Brief clinical answer
        - Differential considerations
        - Red flags / urgent considerations
        - Evidence used
        """

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.1,
        max_tokens=700,
    )

    return {
        "answer": response.choices[0].message.content,
        "refused": False,
        "confidence": retrieval["confidence"],
        "sources": [
            {
                "title": item["metadata"].get("title"),
                "source": item["metadata"].get("source"),
                "year": item["metadata"].get("year"),
                "page": item["metadata"].get("page"),
                "url": item["metadata"].get("url"),
                "score": item["score"],
            }
            for item in retrieval["evidence"]
        ],
    }


if __name__ == "__main__":
    question = "How to repair a motorcycle engine?"
    result = generate_medical_answer(question)

    print("\nAnswer:\n")
    print(result["answer"])

    print("\nConfidence:")
    print(result["confidence"])

    print("\nSources:")
    for source in result["sources"]:
        print(source)