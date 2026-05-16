from pathlib import Path

from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

PDF_METADATA = {
    "acs.pdf": {
        "title": "Acute Coronary Syndromes Guideline",
        "source": "American Heart Association",
        "url": "https://www.ahajournals.org",
        "document_type": "clinical_guideline",
        "year": "2025",
    },
    "chest_pain.pdf": {
        "title": "2021 AHA/ACC/ASE Chest Pain Guideline",
        "source": "American Heart Association / American College of Cardiology",
        "url": "https://www.ahajournals.org",
        "document_type": "clinical_guideline",
        "year": "2021",
    },
    "cardiovascular.pdf": {
        "title": "WHO Prevention of Cardiovascular Disease Guideline",
        "source": "World Health Organization",
        "url": "https://www.who.int",
        "document_type": "clinical_guideline",
        "year": "2007",
    },
    "hypertension.pdf": {
        "title": "2017 ACC/AHA Hypertension Guideline",
        "source": "American College of Cardiology / American Heart Association",
        "url": "https://www.ahajournals.org",
        "document_type": "clinical_guideline",
        "year": "2017",
    },
    "diabetes.pdf": {
        "title": "Standards of Care in Diabetes 2025",
        "source": "American Diabetes Association",
        "url": "https://diabetesjournals.org/care",
        "document_type": "clinical_guideline",
        "year": "2025",
    },
}

BASE_DIR = Path(__file__).resolve().parent.parent
PDF_DIR = BASE_DIR / "data" / "pdfs"
VECTOR_DIR = BASE_DIR / "vector_store"

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150,
)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

documents = []

pdf_files = list(PDF_DIR.glob("*.pdf"))

if not pdf_files:
    raise FileNotFoundError(f"No PDF files found in {PDF_DIR}")

print(f"Looking for PDFs in: {PDF_DIR}")

for pdf_file in pdf_files:
    print(f"\nProcessing: {pdf_file.name}")

    base_metadata = PDF_METADATA.get(
        pdf_file.name,
        {
            "title": pdf_file.stem,
            "source": "Unknown",
            "url": "",
            "document_type": "medical_document",
            "year": "",
        },
    )

    try:
        reader = PdfReader(str(pdf_file))
    except Exception as e:
        print(f"Skipping {pdf_file.name}: {e}")
        continue

    file_chunk_count = 0

    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if not text or not text.strip():
            continue

        chunks = splitter.split_text(text)

        for chunk_index, chunk in enumerate(chunks, start=1):
            documents.append(
                Document(
                    page_content=chunk,
                    metadata={
                        **base_metadata,
                        "file_name": pdf_file.name,
                        "page": page_num,
                        "chunk_index": chunk_index,
                    },
                )
            )

        file_chunk_count += len(chunks)

    print(f"Created {file_chunk_count} chunks")

print(f"\nTotal chunks: {len(documents)}")

if not documents:
    raise ValueError("No chunks created. Check PDFs.")

print("\nGenerating embeddings and saving FAISS index...")

vector_store = FAISS.from_documents(documents, embeddings)
vector_store.save_local(str(VECTOR_DIR))

print(f"Vector store saved to: {VECTOR_DIR}")