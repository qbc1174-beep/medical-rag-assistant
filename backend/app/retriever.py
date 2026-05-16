from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from safety import calculate_confidence, should_refuse

BASE_DIR = Path(__file__).resolve().parent.parent
VECTOR_DIR = BASE_DIR / "vector_store"

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_store = FAISS.load_local(
    str(VECTOR_DIR),
    embeddings,
    allow_dangerous_deserialization=True,
)

def retrieve_medical_evidence(query: str, k: int = 5):
    results = vector_store.similarity_search_with_score(query, k=k)

    if not results:
        return {
            "refused": True,
            "reason": "No relevant medical evidence found.",
            "confidence": {"label": "Low", "value": 0.0},
            "evidence": [],
        }

    evidence = []

    for doc, score in results:
        evidence.append(
            {
                "content": doc.page_content,
                "score": float(score),
                "metadata": doc.metadata,
            }
        )

    best_score = evidence[0]["score"]
    confidence = calculate_confidence(best_score)
    refused = should_refuse(best_score, len(evidence))

    return {
        "refused": refused,
        "reason": "Insufficient evidence found." if refused else None,
        "confidence": confidence,
        "best_score": best_score,
        "evidence": evidence,
    }


if __name__ == "__main__":
    query = "What are possible causes of chest pain in a diabetic patient?"
    result = retrieve_medical_evidence(query)

    print(f"\nQuery: {query}\n")
    print(f"Refused: {result['refused']}")
    print(f"Reason: {result['reason']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Best score: {result['best_score']}")
    print("-" * 80)

    for index, item in enumerate(result["evidence"], start=1):
        metadata = item["metadata"]

        print(f"Result {index}")
        print(f"Title: {metadata.get('title')}")
        print(f"Source: {metadata.get('source')}")
        print(f"Page: {metadata.get('page')}")
        print(f"Score: {item['score']}")
        print(item["content"][:500])
        print("-" * 80)