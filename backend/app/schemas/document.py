from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DocumentBase(BaseModel):
    filename: str
    source: str
    department: Optional[str] = None
    location: Optional[str] = None
    document_type: Optional[str] = None


class DocumentCreate(DocumentBase):
    pass


class DocumentResponse(DocumentBase):
    id: int
    document_id: str
    summary: Optional[str] = None
    issue: Optional[str] = None
    priority: Optional[str] = None
    action_required: Optional[str] = None
    deadline: Optional[datetime] = None
    risk: Optional[str] = None
    status: str
    file_path: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True