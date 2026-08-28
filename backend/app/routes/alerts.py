from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.document import Alert
from app.schemas.alert import AlertResponse

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("", response_model=list[AlertResponse])
def get_alerts(db: Session = Depends(get_db)):
    return db.query(Alert).filter(Alert.is_resolved == 0).order_by(Alert.created_at.desc()).all()


@router.post("/{alert_id}/resolve")
def resolve_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.is_resolved = 1
    db.commit()
    return {"message": f"Alert {alert_id} marked as resolved"}