from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Settings(Base):
    __tablename__ = "settings"
    
    id = Column(Integer, primary_key=True, index=True)
    llm_provider = Column(String, default="openai")
    llm_api_key = Column(String)
    gmail_server = Column(String)
    gmail_username = Column(String)
    gmail_password = Column(String)
    auto_check_email = Column(Boolean, default=False)
    check_interval = Column(Integer, default=60)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    filepath = Column(String)
    document_type = Column(String)
    analysis_result = Column(Text)
    file_size = Column(Integer)
    processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class FinancialProfile(Base):
    __tablename__ = "financial_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True)
    subcategory = Column(String)
    amount = Column(Float)
    date = Column(DateTime)
    description = Column(Text)
    source_document_id = Column(Integer, ForeignKey("documents.id"))
    metadata = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    source_document = relationship("Document", backref="financial_entries")

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text)
    response = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    context_used = Column(Text)

class RAGDocument(Base):
    __tablename__ = "rag_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    filepath = Column(String)
    content = Column(Text)
    embedding_id = Column(String)
    chunk_count = Column(Integer, default=0)
    processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)