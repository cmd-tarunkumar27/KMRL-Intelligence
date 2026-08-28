from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models.document import Document

router = APIRouter(tags=["ai"])


class SearchRequest(BaseModel):
    query: str


class AskRequest(BaseModel):
    question: str


@router.post("/search")
def search_documents(request: SearchRequest, db: Session = Depends(get_db)):
    # TODO: Group 2 Member 2 will replace this with real RAG/semantic search.
    # For now, do a simple text match on summary/issue so the endpoint works end-to-end.
    results = (
        db.query(Document)
        .filter(
            Document.summary.ilike(f"%{request.query}%")
            | Document.issue.ilike(f"%{request.query}%")
        )
        .limit(10)
        .all()
    )
    return {
        "query": request.query,
        "results": [
            {"document_id": d.document_id, "filename": d.filename, "summary": d.summary}
            for d in results
        ],
    }


@router.post("/ask")
def ask_question(request: AskRequest):
    # TODO: Group 2 Member 2 will replace this with real RAG-based answer + sources.
    return {
        "question": request.question,
        "answer": "AI answering not yet connected. This is a placeholder response.",
        "sources": [],
    }


@router.post("/process/{document_id}")
def process_document(document_id: str, db: Session = Depends(get_db)):
    # TODO: Group 2 Member 1 will call this (or the backend will call their service)
    # to trigger AI extraction and update the document with structured info.
    doc = db.query(Document).filter(Document.document_id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    doc.status = "processing"
    db.commit()
    return {"message": f"Processing started for {document_id}", "status": doc.status}
