from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from pathlib import Path

data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

DATABASE_URL = f"sqlite:///{data_dir}/finance_agent.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    from .models import Settings, Document, FinancialProfile, ChatMessage, RAGDocument
    Base.metadata.create_all(bind=engine)