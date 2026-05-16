from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

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

    evidence = []

    for doc, score in results:
        evidence.append({
            "content": doc.page_content,
            "score": float(score),
            "metadata": doc.metadata,
        })

    return evidence


if __name__ == "__main__":
    query = "What are possible causes of chest pain in a diabetic patient?"
    results = retrieve_medical_evidence(query)

    print(f"\nQuery: {query}\n")

    for index, item in enumerate(results, start=1):
        metadata = item["metadata"]

        print(f"Result {index}")
        print(f"Title: {metadata.get('title')}")
        print(f"Source: {metadata.get('source')}")
        print(f"Page: {metadata.get('page')}")
        print(f"Score: {item['score']}")
        print(item["content"][:500])
        print("-" * 80)