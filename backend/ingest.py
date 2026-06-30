from document_loader import load_pdf
from chunker import create_chunks
from vectorstore import store_chunks


def ingest_document(pdf_path):

    text = load_pdf(
        pdf_path
    )

    chunks = create_chunks(
        text
    )

    store_chunks(
        chunks,
        pdf_path
    )

    return len(chunks)