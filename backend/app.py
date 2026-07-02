from fastapi import FastAPI

from fastapi import UploadFile, File
import os

from document_loader import load_pdf

from ingest import ingest_document

from pydantic import BaseModel

from rag_engine import (ask_rag, ask_rag_stream)

from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import StreamingResponse

class QuestionRequest(BaseModel):
    question: str
    selected_documents: list[str] = []
    chat_history: list = []

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
    
    print(
        "Selected Documents:",
        request.selected_documents
    )

    result = ask_rag(
        request.question,
        request.selected_documents,
        request.chat_history
    )

    return {
        "question": request.question,
        "answer": result["answer"],
        "sources": result["sources"]
    }
    
@app.post("/ask-stream")
def ask_stream(
    request: QuestionRequest
):

    return StreamingResponse(

        ask_rag_stream(
            request.question,
            request.selected_documents,
            request.chat_history
        ),

        media_type="text/plain"

    )

@app.get("/documents")
def get_documents():

    import os

    uploads_folder = "uploads"

    if not os.path.exists(
        uploads_folder
    ):
        return {
            "documents": []
        }

    files = os.listdir(
        uploads_folder
    )

    return {
        "documents": files
    }
    
@app.delete("/documents/{filename}")
def delete_document(filename: str):

    import os

    file_path = os.path.join(
        "uploads",
        filename
    )

    if os.path.exists(
        file_path
    ):

        os.remove(
            file_path
        )

        return {
            "message":
            f"{filename} deleted"
        }

    return {
        "message":
        "File not found"
    }