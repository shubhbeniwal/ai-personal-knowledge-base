from fastapi import FastAPI

from fastapi import UploadFile, File
import os

from document_loader import load_pdf


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
async def upload_document(
    file: UploadFile = File(...)
):

    os.makedirs(
        "uploads",
        exist_ok=True
    )

    file_path = f"uploads/{file.filename}"

    with open(
        file_path,
        "wb"
    ) as buffer:

        buffer.write(
            await file.read()
        )

    document_text = load_pdf(
        file_path
    )

    return {
        "filename": file.filename,
        "characters": len(document_text),
        "status": "uploaded"
    }