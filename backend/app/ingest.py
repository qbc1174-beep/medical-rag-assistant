from pathlib import Path

from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

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

pdf_dir = Path(__file__).resolve().parent.parent / "data" / "pdfs"

print(f"Looking for PDFs in: {pdf_dir}")

pdf_files = list(pdf_dir.glob("*.pdf"))

if not pdf_files:
    raise FileNotFoundError(f"No PDF files found in {pdf_dir}")

all_chunks = []

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150,
)

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

    print(f"Pages: {len(reader.pages)}")

    file_chunk_count = 0

    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if not text or not text.strip():
            continue

        page_chunks = splitter.split_text(text)

        for chunk_index, chunk in enumerate(page_chunks, start=1):
            all_chunks.append(
                {
                    "content": chunk,
                    "metadata": {
                        **base_metadata,
                        "file_name": pdf_file.name,
                        "page": page_num,
                        "chunk_index": chunk_index,
                    },
                }
            )

        file_chunk_count += len(page_chunks)

    print(f"Created {file_chunk_count} chunks")

print(f"\nTotal chunks: {len(all_chunks)}")

if all_chunks:
    print("\nSample chunk:\n")
    print(all_chunks[0]["content"][:500])
    print("\nMetadata:")
    print(all_chunks[0]["metadata"])
else:
    print("No chunks created. Check if PDFs are present and text-based.")