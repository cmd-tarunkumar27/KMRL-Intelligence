from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database import get_db
from app.models.document import Relationship
from app.schemas.alert import RelationshipResponse

router = APIRouter(prefix="/documents", tags=["related"])


@router.get("/{document_id}/related", response_model=list[RelationshipResponse])
def get_related_documents(document_id: str, db: Session = Depends(get_db)):
    return (
        db.query(Relationship)
        .filter(
            or_(
                Relationship.document_id_1 == document_id,
                Relationship.document_id_2 == document_id,
            )
        )
        .all()
    )