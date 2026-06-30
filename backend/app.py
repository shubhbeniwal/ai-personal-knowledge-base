from fastapi import FastAPI

from fastapi import UploadFile, File
import os

from document_loader import load_pdf

from ingest import ingest_document

from pydantic import BaseModel
from rag_engine import ask_rag

from fastapi.middleware.cors import CORSMiddleware

class QuestionRequest(BaseModel):
    question: str

app = FastAPI(
    title="AI Personal Knowledge Base",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

    import os

    os.makedirs(
        "uploads",
        exist_ok=True
    )

    file_path = os.path.join(
        "uploads",
        file.filename
    )

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
        f"{file.filename} uploaded successfully",

        "chunks_stored":
        chunk_count
    }
    
@app.post("/ask")
def ask_question(
    request: QuestionRequest
):

    result = ask_rag(
        request.question
    )

    return {
        "question": request.question,
        "answer": result["answer"],
        "sources": result["sources"]
    }
    