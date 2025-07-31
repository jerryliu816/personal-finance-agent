from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
import json
from pathlib import Path
from typing import List, Optional

from .database import get_db, init_db
from .models import Settings, Document, FinancialProfile, ChatMessage
from .schemas import (
    SettingsCreate, SettingsResponse,
    DocumentCreate, DocumentResponse,
    ChatRequest, ChatResponse,
    FinancialProfileResponse
)
from ...core.llm_client import LLMClient
from ...core.document_processor import DocumentProcessor
from ...core.finance_profile import FinanceProfileManager

app = FastAPI(title="Personal Finance Agent API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/settings")
async def get_settings(db: Session = Depends(get_db)):
    settings = db.query(Settings).first()
    if not settings:
        return SettingsResponse(
            llm_provider="openai",
            llm_api_key="",
            gmail_server="",
            gmail_username="",
            gmail_password="",
            auto_check_email=False,
            check_interval=60
        )
    return SettingsResponse.from_orm(settings)

@app.post("/api/settings")
async def update_settings(settings_data: SettingsCreate, db: Session = Depends(get_db)):
    settings = db.query(Settings).first()
    if settings:
        for key, value in settings_data.dict().items():
            setattr(settings, key, value)
    else:
        settings = Settings(**settings_data.dict())
        db.add(settings)
    
    db.commit()
    db.refresh(settings)
    return SettingsResponse.from_orm(settings)

@app.post("/api/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    document_type: str = "financial",
    db: Session = Depends(get_db)
):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    upload_dir = Path("data/uploads")
    upload_dir.mkdir(exist_ok=True)
    
    file_path = upload_dir / file.filename
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    processor = DocumentProcessor()
    analysis_result = await processor.process_document(str(file_path))
    
    doc = Document(
        filename=file.filename,
        filepath=str(file_path),
        document_type=document_type,
        analysis_result=json.dumps(analysis_result),
        file_size=len(content)
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    
    return DocumentResponse.from_orm(doc)

@app.get("/api/documents")
async def get_documents(db: Session = Depends(get_db)) -> List[DocumentResponse]:
    documents = db.query(Document).all()
    return [DocumentResponse.from_orm(doc) for doc in documents]

@app.delete("/api/documents/{document_id}")
async def delete_document(document_id: int, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if os.path.exists(document.filepath):
        os.remove(document.filepath)
    
    db.delete(document)
    db.commit()
    return {"message": "Document deleted successfully"}

@app.get("/api/profile")
async def get_financial_profile(db: Session = Depends(get_db)):
    profile_manager = FinanceProfileManager(db)
    profile_data = profile_manager.get_profile_summary()
    return FinancialProfileResponse(**profile_data)

@app.post("/api/chat")
async def chat_with_agent(request: ChatRequest, db: Session = Depends(get_db)):
    settings = db.query(Settings).first()
    if not settings or not settings.llm_api_key:
        raise HTTPException(status_code=400, detail="LLM settings not configured")
    
    llm_client = LLMClient(
        provider=settings.llm_provider,
        api_key=settings.llm_api_key
    )
    
    profile_manager = FinanceProfileManager(db)
    context = profile_manager.get_chat_context()
    
    response = await llm_client.chat_with_context(request.message, context)
    
    chat_message = ChatMessage(
        message=request.message,
        response=response,
        timestamp=request.timestamp
    )
    db.add(chat_message)
    db.commit()
    
    return ChatResponse(response=response)

@app.get("/api/chat/history")
async def get_chat_history(db: Session = Depends(get_db)):
    messages = db.query(ChatMessage).order_by(ChatMessage.timestamp.desc()).limit(50).all()
    return [{"message": msg.message, "response": msg.response, "timestamp": msg.timestamp} for msg in messages]

frontend_path = Path(__file__).parent.parent / "frontend" / "build"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path / "static")), name="static")
    
    @app.get("/{path:path}")
    async def serve_frontend(path: str):
        file_path = frontend_path / path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(frontend_path / "index.html")
else:
    @app.get("/")
    async def root():
        return {"message": "Personal Finance Agent API is running. Frontend not built yet."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)