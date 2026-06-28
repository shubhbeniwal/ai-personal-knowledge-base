from fastapi import FastAPI

from fastapi import UploadFile, File
import os

from document_loader import load_pdf

from ingest import ingest_document


app = FastAPI(
    title="AI Personal Knowledge Base",
    version="1.0.0"
)

@app.get("/")
def home():

    return {
        "message": "AI Personal Knowledge Base Backend Running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }
    
@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...)
):

    file_path = file.filename

    with open(
        file_path,
        "wb"
    ) as buffer:

        buffer.write(
            await file.read()
        )

    chunk_count = ingest_document(
        file_path
    )

    return {
        "message":
        "Document Uploaded Successfully",

        "chunks_stored":
        chunk_count
    }