import os
import shutil
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.document import Document
from app.schemas.document import DocumentResponse

router = APIRouter(prefix="/documents", tags=["documents"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload", response_model=DocumentResponse)
def upload_document(
    file: UploadFile = File(...),
    source: str = "manual",
    department: str = None,
    location: str = None,
    db: Session = Depends(get_db),
):
    doc_id = f"DOC{uuid.uuid4().hex[:8].upper()}"

    file_path = os.path.join(UPLOAD_DIR, f"{doc_id}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_doc = Document(
        document_id=doc_id,
        filename=file.filename,
        source=source,
        department=department,
        location=location,
        status="received",
        file_path=file_path,
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    return new_doc


@router.get("", response_model=list[DocumentResponse])
def get_documents(db: Session = Depends(get_db)):
    return db.query(Document).order_by(Document.created_at.desc()).all()


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: str, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.document_id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


@router.delete("/{document_id}")
def delete_document(document_id: str, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.document_id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    db.delete(doc)
    db.commit()
    return {"message": f"Document {document_id} deleted"}