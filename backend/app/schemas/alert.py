from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AlertResponse(BaseModel):
    id: int
    document_id: str
    alert_type: Optional[str] = None
    message: Optional[str] = None
    is_resolved: int
    created_at: datetime

    class Config:
        from_attributes = True


class RelationshipResponse(BaseModel):
    id: int
    document_id_1: str
    document_id_2: str
    relationship_type: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True