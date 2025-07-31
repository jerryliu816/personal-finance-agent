from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Dict, Any, List

class SettingsCreate(BaseModel):
    llm_provider: str = "openai"
    llm_api_key: str
    gmail_server: Optional[str] = None
    gmail_username: Optional[str] = None
    gmail_password: Optional[str] = None
    auto_check_email: bool = False
    check_interval: int = 60

class SettingsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: Optional[int] = None
    llm_provider: str
    llm_api_key: str
    gmail_server: Optional[str]
    gmail_username: Optional[str]
    gmail_password: Optional[str]
    auto_check_email: bool
    check_interval: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class DocumentCreate(BaseModel):
    filename: str
    document_type: str = "financial"

class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    filename: str
    filepath: str
    document_type: str
    analysis_result: Optional[str]
    file_size: int
    processed: bool
    created_at: datetime
    updated_at: datetime

class ChatRequest(BaseModel):
    message: str
    timestamp: Optional[datetime] = None

class ChatResponse(BaseModel):
    response: str

class FinancialEntry(BaseModel):
    category: str
    subcategory: Optional[str]
    amount: float
    date: datetime
    description: str

class FinancialProfileResponse(BaseModel):
    total_assets: float
    total_liabilities: float
    net_worth: float
    monthly_income: float
    monthly_expenses: float
    investment_portfolio: Dict[str, float]
    credit_accounts: List[Dict[str, Any]]
    recent_transactions: List[FinancialEntry]
    last_updated: datetime

class RAGDocumentCreate(BaseModel):
    filename: str

class RAGDocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    filename: str
    filepath: str
    content: Optional[str]
    chunk_count: int
    processed: bool
    created_at: datetime