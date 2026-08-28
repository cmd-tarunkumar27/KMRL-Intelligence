from app.database import engine, Base
from app.models.document import Document, Relationship, Alert

Base.metadata.create_all(bind=engine)
print("Tables created successfully!")