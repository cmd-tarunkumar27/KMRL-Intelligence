from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(String, unique=True, index=True)  # e.g. DOC001
    filename = Column(String, nullable=False)
    source = Column(String, nullable=False)  # email, sharepoint, maximo, whatsapp, scanned, manual
    department = Column(String, nullable=True)
    location = Column(String, nullable=True)
    document_type = Column(String, nullable=True)

    raw_text = Column(Text, nullable=True)  # full extracted text from OCR/PDF
    summary = Column(Text, nullable=True)
    issue = Column(Text, nullable=True)
    priority = Column(String, nullable=True)  # Critical, High, Medium, Low
    action_required = Column(Text, nullable=True)
    deadline = Column(DateTime, nullable=True)
    risk = Column(Text, nullable=True)

    status = Column(String, default="received")  # received, processing, processed, failed
    file_path = Column(String, nullable=True)  # where the uploaded file is stored

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    alerts = relationship("Alert", back_populates="document")


class Relationship(Base):
    __tablename__ = "relationships"

    id = Column(Integer, primary_key=True, index=True)
    document_id_1 = Column(String, ForeignKey("documents.document_id"), nullable=False)
    document_id_2 = Column(String, ForeignKey("documents.document_id"), nullable=False)
    relationship_type = Column(String, nullable=True)  # e.g. "related_issue", "same_location", "conflict"
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(String, ForeignKey("documents.document_id"), nullable=False)
    alert_type = Column(String, nullable=True)  # deadline, conflict, critical_priority
    message = Column(Text, nullable=True)
    is_resolved = Column(Integer, default=0)  # 0 = active, 1 = resolved
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    document = relationship("Document", back_populates="alerts")