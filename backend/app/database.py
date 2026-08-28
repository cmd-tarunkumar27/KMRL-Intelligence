from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# Get the database connection string from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the database engine (this manages the actual connection)
engine = create_engine(DATABASE_URL)

# Create a session factory (each request will get its own session)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class that all our database models will inherit from
Base = declarative_base()

# Dependency function - FastAPI will use this to give each API request
# its own database session, and automatically close it when done
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()