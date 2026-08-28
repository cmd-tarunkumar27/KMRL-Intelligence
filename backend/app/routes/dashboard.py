from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.database import get_db
from app.models.document import Document, Alert, Relationship

router = APIRouter(tags=["dashboard"])


@router.get("/dashboard")
def get_dashboard(db: Session = Depends(get_db)):
    total_documents = db.query(Document).count()
    critical = db.query(Document).filter(Document.priority == "Critical").count()
    high = db.query(Document).filter(Document.priority == "High").count()
    medium = db.query(Document).filter(Document.priority == "Medium").count()

    upcoming_deadline_cutoff = datetime.utcnow() + timedelta(days=7)
    upcoming_deadlines = (
        db.query(Document)
        .filter(Document.deadline != None)
        .filter(Document.deadline <= upcoming_deadline_cutoff)
        .filter(Document.deadline >= datetime.utcnow())
        .count()
    )

    pending_actions = db.query(Document).filter(Document.status == "processed", Document.action_required != None).count()

    potential_conflicts = db.query(Relationship).filter(Relationship.relationship_type == "conflict").count()

    recent_documents = (
        db.query(Document)
        .order_by(Document.created_at.desc())
        .limit(5)
        .all()
    )

    return {
        "total_documents": total_documents,
        "critical_documents": critical,
        "high_priority_documents": high,
        "medium_priority_documents": medium,
        "upcoming_deadlines": upcoming_deadlines,
        "pending_actions": pending_actions,
        "potential_conflicts": potential_conflicts,
        "recent_documents": [
            {
                "document_id": d.document_id,
                "filename": d.filename,
                "priority": d.priority,
                "status": d.status,
                "created_at": d.created_at,
            }
            for d in recent_documents
        ],
    }
