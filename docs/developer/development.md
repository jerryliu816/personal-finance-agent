# Development Guide

Comprehensive guide for developing and contributing to Personal Finance Agent.

## 🎯 Development Workflow

### Git Workflow

#### Branch Strategy
```bash
# Main branches
main                    # Production-ready code
develop                 # Integration branch for features

# Feature branches
feature/pdf-processing  # New feature development
bugfix/database-lock   # Bug fixes
hotfix/security-patch  # Critical production fixes
release/v1.1.0         # Release preparation
```

#### Branch Naming Conventions
```bash
feature/description-of-feature
bugfix/description-of-bug
hotfix/critical-security-fix
docs/update-api-documentation
test/add-integration-tests
refactor/improve-database-layer
```

#### Commit Message Format
Follow [Conventional Commits](https://www.conventionalcommits.org/):

```bash
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or modifying tests
- `chore`: Maintenance tasks

**Examples**:
```bash
feat(document): add support for tax document processing
fix(database): resolve connection timeout issues
docs(api): update REST API documentation
test(chat): add unit tests for chat functionality
refactor(llm): improve error handling in LLM client
```

### Development Process

#### 1. Planning Phase
```bash
# Create or assign GitHub issue
# Design solution approach
# Review with maintainers if needed
# Create feature branch

git checkout develop
git pull origin develop
git checkout -b feature/new-document-type
```

#### 2. Development Phase
```bash
# Make incremental commits
git add .
git commit -m "feat(document): add initial PDF parsing logic"

# Push regularly to backup work
git push origin feature/new-document-type

# Keep branch updated with develop
git rebase develop
```

#### 3. Testing Phase
```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/unit/
pytest tests/integration/

# Check test coverage
pytest --cov=src --cov-report=html

# Run linting
flake8 src/
black --check src/
mypy src/
```

#### 4. Review Phase
```bash
# Create pull request
# Request code review
# Address feedback
# Update documentation if needed
```

#### 5. Integration Phase
```bash
# Merge to develop
# Update changelog
# Tag release if needed
```

## 📝 Coding Standards

### Python Code Style

#### PEP 8 Compliance
```python
# Use Black formatter (max line length: 88)
# Import organization
import os
import sys
from pathlib import Path

import fastapi
import sqlalchemy
from pydantic import BaseModel

from src.core.document_processor import DocumentProcessor
```

#### Type Hints
```python
from typing import Dict, List, Optional, Union
from datetime import datetime

def process_document(
    file_path: str,
    document_type: str = "financial"
) -> Dict[str, Any]:
    """Process a financial document and return analysis results."""
    pass

class DocumentResponse(BaseModel):
    id: int
    filename: str
    processed: bool
    created_at: datetime
    analysis_result: Optional[Dict[str, Any]] = None
```

#### Error Handling
```python
# Use specific exception types
class DocumentProcessingError(Exception):
    """Raised when document processing fails."""
    def __init__(self, message: str, error_code: str = None):
        super().__init__(message)
        self.error_code = error_code

# Proper exception handling
try:
    result = process_document(file_path)
except DocumentProcessingError as e:
    logger.error(f"Document processing failed: {e}")
    raise HTTPException(status_code=422, detail=str(e))
except Exception as e:
    logger.exception("Unexpected error during document processing")
    raise HTTPException(status_code=500, detail="Internal server error")
```

#### Logging
```python
import logging

logger = logging.getLogger(__name__)

def process_document(file_path: str) -> Dict[str, Any]:
    logger.info(f"Starting document processing for {file_path}")
    
    try:
        # Processing logic
        result = analyze_document(file_path)
        logger.info(f"Document processed successfully: {len(result.get('transactions', []))} transactions found")
        return result
    except Exception as e:
        logger.error(f"Document processing failed: {e}")
        raise
```

#### Async/Await Patterns
```python
import asyncio
from typing import List

async def process_multiple_documents(file_paths: List[str]) -> List[Dict[str, Any]]:
    """Process multiple documents concurrently."""
    tasks = [process_document_async(path) for path in file_paths]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    successful_results = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            logger.error(f"Failed to process {file_paths[i]}: {result}")
        else:
            successful_results.append(result)
    
    return successful_results
```

### TypeScript/React Code Style

#### Component Structure
```typescript
// Functional components with TypeScript
import React, { useState, useEffect } from 'react'
import { Button, Alert, CircularProgress } from '@mui/material'

interface DocumentUploadProps {
  onUploadComplete: (document: Document) => void
  maxFileSize?: number
}

export default function DocumentUpload({
  onUploadComplete,
  maxFileSize = 50 * 1024 * 1024 // 50MB default
}: DocumentUploadProps) {
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleUpload = async (file: File) => {
    try {
      setUploading(true)
      setError(null)
      
      if (file.size > maxFileSize) {
        throw new Error(`File size exceeds ${maxFileSize / 1024 / 1024}MB limit`)
      }
      
      const document = await uploadDocument(file)
      onUploadComplete(document)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed')
    } finally {
      setUploading(false)
    }
  }

  return (
    <div>
      {error && <Alert severity="error">{error}</Alert>}
      <Button disabled={uploading}>
        {uploading ? <CircularProgress size={20} /> : 'Upload Document'}
      </Button>
    </div>
  )
}
```

#### API Service Layer
```typescript
// services/api.ts
import axios, { AxiosResponse } from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

// Request interceptor for auth
api.interceptors.request.use((config) => {
  // Add auth headers if needed
  return config
})

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle authentication errors
    }
    return Promise.reject(error)
  }
)

export const documentsApi = {
  uploadDocument: async (file: File): Promise<Document> => {
    const formData = new FormData()
    formData.append('file', file)
    
    const response: AxiosResponse<Document> = await api.post(
      '/documents/upload',
      formData,
      {
        headers: { 'Content-Type': 'multipart/form-data' },
      }
    )
    
    return response.data
  },

  getDocuments: async (): Promise<Document[]> => {
    const response = await api.get<Document[]>('/documents')
    return response.data
  },
}
```

## 🧪 Testing Guidelines

### Test Structure

#### Unit Tests
```python
# tests/unit/test_document_processor.py
import pytest
from unittest.mock import Mock, patch
from src.core.document_processor import DocumentProcessor
from src.core.llm_client import LLMClient

class TestDocumentProcessor:
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.processor = DocumentProcessor()
        self.sample_pdf_path = "tests/fixtures/sample_statement.pdf"

    def test_classify_document_type_credit_card(self):
        """Test credit card document classification."""
        text = "CREDIT CARD STATEMENT\nStatement Balance: $1,234.56\nMinimum Payment Due: $25.00"
        result = self.processor._classify_document_type(text)
        assert result == "credit_card"

    def test_classify_document_type_bank_statement(self):
        """Test bank statement document classification."""
        text = "CHECKING ACCOUNT STATEMENT\nOpening Balance: $5,000.00\nClosing Balance: $4,750.00"
        result = self.processor._classify_document_type(text)
        assert result == "bank_statement"

    @patch('src.core.document_processor.DocumentProcessor._extract_text_via_mcp')
    async def test_process_document_success(self, mock_extract_text):
        """Test successful document processing."""
        # Mock text extraction
        mock_extract_text.return_value = "Sample financial document text"
        
        # Mock LLM client
        mock_llm = Mock(spec=LLMClient)
        mock_llm.analyze_financial_document.return_value = {
            "document_type": "credit_card",
            "transactions": [
                {"date": "2024-01-01", "amount": -50.0, "description": "Restaurant"}
            ]
        }
        
        result = await self.processor.process_document(
            self.sample_pdf_path,
            llm_client=mock_llm
        )
        
        assert result["success"] is True
        assert result["document_type"] == "credit_card"
        assert "ai_analysis" in result

    def test_process_document_file_not_found(self):
        """Test handling of non-existent files."""
        result = asyncio.run(
            self.processor.process_document("nonexistent.pdf")
        )
        assert result["success"] is False
        assert "File not found" in result["error"]
```

#### Integration Tests
```python
# tests/integration/test_api_endpoints.py
import pytest
from fastapi.testclient import TestClient
from src.ui.backend.main import app

class TestDocumentEndpoints:
    def setup_method(self):
        """Set up test client and test data."""
        self.client = TestClient(app)
        self.test_pdf_content = b"Mock PDF content"

    def test_upload_document_success(self):
        """Test successful document upload."""
        files = {"file": ("test.pdf", self.test_pdf_content, "application/pdf")}
        response = self.client.post("/api/documents/upload", files=files)
        
        assert response.status_code == 200
        data = response.json()
        assert data["filename"] == "test.pdf"
        assert data["processed"] is True

    def test_upload_document_invalid_format(self):
        """Test upload with invalid file format."""
        files = {"file": ("test.txt", b"Text content", "text/plain")}
        response = self.client.post("/api/documents/upload", files=files)
        
        assert response.status_code == 400
        assert "Only PDF files are supported" in response.json()["detail"]

    def test_get_documents_empty(self):
        """Test getting documents when none exist."""
        response = self.client.get("/api/documents")
        
        assert response.status_code == 200
        assert response.json() == []
```

#### Frontend Tests
```typescript
// src/ui/frontend/src/__tests__/DocumentUpload.test.tsx
import React from 'react'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import '@testing-library/jest-dom'
import { rest } from 'msw'
import { setupServer } from 'msw/node'
import DocumentUpload from '../components/DocumentUpload'

// Mock API server
const server = setupServer(
  rest.post('/api/documents/upload', (req, res, ctx) => {
    return res(
      ctx.json({
        id: 1,
        filename: 'test.pdf',
        processed: true,
        created_at: '2024-01-01T00:00:00Z'
      })
    )
  })
)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

describe('DocumentUpload', () => {
  test('renders upload button', () => {
    render(<DocumentUpload onUploadComplete={jest.fn()} />)
    expect(screen.getByText('Upload Document')).toBeInTheDocument()
  })

  test('handles successful upload', async () => {
    const onUploadComplete = jest.fn()
    render(<DocumentUpload onUploadComplete={onUploadComplete} />)
    
    const file = new File(['pdf content'], 'test.pdf', { type: 'application/pdf' })
    const input = screen.getByRole('button')
    
    fireEvent.click(input)
    // Simulate file selection and upload...
    
    await waitFor(() => {
      expect(onUploadComplete).toHaveBeenCalledWith(
        expect.objectContaining({ filename: 'test.pdf' })
      )
    })
  })
})
```

### Test Data Management

#### Fixtures
```python
# tests/conftest.py
import pytest
import tempfile
from pathlib import Path
from src.ui.backend.database import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture
def test_db():
    """Create temporary test database."""
    engine = create_engine("sqlite:///test.db", echo=False)
    Base.metadata.create_all(engine)
    
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    yield TestingSessionLocal()
    
    # Cleanup
    Path("test.db").unlink(missing_ok=True)

@pytest.fixture
def sample_pdf():
    """Create sample PDF file for testing."""
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
        f.write(b'Mock PDF content')
        f.flush()
        yield f.name
    Path(f.name).unlink(missing_ok=True)

@pytest.fixture
def mock_llm_response():
    """Mock LLM analysis response."""
    return {
        "document_type": "credit_card",
        "transactions": [
            {
                "date": "2024-01-01",
                "amount": -50.0,
                "description": "Restaurant Purchase",
                "category": "dining"
            }
        ],
        "summary": {
            "total_credits": 0.0,
            "total_debits": -50.0,
            "net_change": -50.0
        }
    }
```

## 🔧 Development Tools

### Code Quality Tools

#### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
        language_version: python3.9

  - repo: https://github.com/pycqa/flake8
    rev: 4.0.1
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.950
    hooks:
      - id: mypy
        additional_dependencies: [types-all]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.2.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
```

#### Configuration Files

**`.flake8`**:
```ini
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = 
    venv/,
    .git/,
    __pycache__/,
    build/,
    dist/
```

**`pyproject.toml`**:
```toml
[tool.black]
line-length = 88
target-version = ['py39']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

### IDE Configuration

#### VS Code Extensions
```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.black-formatter",
    "ms-python.flake8",
    "ms-python.mypy-type-checker",
    "ms-vscode.vscode-typescript-next",
    "bradlc.vscode-tailwindcss",
    "esbenp.prettier-vscode"
  ]
}
```

#### Debug Configurations
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "src.ui.backend.main:app",
        "--reload",
        "--port",
        "8000"
      ],
      "console": "integratedTerminal",
      "envFile": "${workspaceFolder}/.env"
    },
    {
      "name": "Python: Tests",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": ["-v"],
      "console": "integratedTerminal"
    }
  ]
}
```

## 📚 Documentation Standards

### Code Documentation

#### Docstring Format
```python
def analyze_financial_document(self, text_content: str, document_type: str = "financial") -> Dict[str, Any]:
    """
    Analyze a financial document using AI and extract structured data.
    
    Args:
        text_content (str): The extracted text content from the document
        document_type (str, optional): Type of document being analyzed. 
                                     Defaults to "financial".
    
    Returns:
        Dict[str, Any]: Analysis results containing:
            - document_type: Detected document type
            - transactions: List of extracted transactions
            - summary: Financial summary data
            - insights: AI-generated insights
    
    Raises:
        APIConfigurationError: If API key is not configured
        DocumentProcessingError: If analysis fails
    
    Example:
        >>> client = LLMClient("openai", "sk-...")
        >>> result = await client.analyze_financial_document(text, "credit_card")
        >>> print(result["document_type"])
        'credit_card'
    """
```

#### API Documentation
```python
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

class DocumentUploadResponse(BaseModel):
    """Response model for document upload endpoint."""
    id: int
    filename: str
    document_type: str
    processed: bool
    file_size: int
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "filename": "statement_2024_01.pdf",
                "document_type": "credit_card",
                "processed": True,
                "file_size": 1048576
            }
        }

@router.post("/documents/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    document_type: str = "financial",
    db: Session = Depends(get_db)
) -> DocumentUploadResponse:
    """
    Upload and analyze a financial document.
    
    - **file**: PDF file to upload (required)
    - **document_type**: Type of document (optional, defaults to "financial")
    
    Returns the uploaded document with analysis results.
    
    Raises:
        - **400**: Invalid file format or size
        - **422**: Document processing failed
        - **500**: Internal server error
    """
```

## 🚀 Performance Guidelines

### Database Optimization

#### Query Optimization
```python
# Good: Use specific queries with proper indexing
def get_recent_transactions(db: Session, limit: int = 10) -> List[FinancialProfile]:
    return db.query(FinancialProfile)\
        .order_by(FinancialProfile.date.desc())\
        .limit(limit)\
        .all()

# Better: Add index for frequently queried columns
# In models.py:
class FinancialProfile(Base):
    __tablename__ = "financial_profiles"
    
    date = Column(DateTime, index=True)  # Add index for date queries
    category = Column(String(100), index=True)  # Add index for category filtering
```

#### Connection Management
```python
# Use connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600
)
```

### Frontend Performance

#### Code Splitting
```typescript
// Lazy load pages for better initial load time
import { lazy, Suspense } from 'react'

const Dashboard = lazy(() => import('./pages/Dashboard'))
const Documents = lazy(() => import('./pages/Documents'))
const Chat = lazy(() => import('./pages/Chat'))

function App() {
  return (
    <Suspense fallback={<CircularProgress />}>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/documents" element={<Documents />} />
        <Route path="/chat" element={<Chat />} />
      </Routes>
    </Suspense>
  )
}
```

#### Memoization
```typescript
// Use React.memo for expensive components
import React, { memo, useMemo } from 'react'

interface ExpensiveChartProps {
  data: TransactionData[]
  timeRange: string
}

const ExpensiveChart = memo(({ data, timeRange }: ExpensiveChartProps) => {
  const processedData = useMemo(() => {
    return data.filter(/* expensive filtering logic */)
  }, [data, timeRange])

  return <Chart data={processedData} />
})
```

## 🔍 Debugging Guidelines

### Python Debugging

#### Logging Strategy
```python
import logging
import traceback

logger = logging.getLogger(__name__)

def process_document_with_debugging(file_path: str) -> Dict[str, Any]:
    logger.info(f"Processing document: {file_path}")
    
    try:
        # Add timing information
        start_time = time.time()
        result = process_document(file_path)
        processing_time = time.time() - start_time
        
        logger.info(f"Document processed in {processing_time:.2f} seconds")
        logger.debug(f"Processing result: {result}")
        
        return result
        
    except Exception as e:
        logger.error(f"Document processing failed: {e}")
        logger.debug(f"Full traceback: {traceback.format_exc()}")
        raise
```

#### Error Context
```python
class DocumentProcessingError(Exception):
    """Enhanced exception with context information."""
    
    def __init__(self, message: str, file_path: str = None, error_code: str = None):
        super().__init__(message)
        self.file_path = file_path
        self.error_code = error_code
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "message": str(self),
            "file_path": self.file_path,
            "error_code": self.error_code,
            "timestamp": self.timestamp.isoformat()
        }
```

### Frontend Debugging

#### Error Boundaries
```typescript
import React, { Component, ReactNode } from 'react'

interface ErrorBoundaryState {
  hasError: boolean
  error: Error | null
  errorInfo: any
}

class ErrorBoundary extends Component<{ children: ReactNode }, ErrorBoundaryState> {
  constructor(props: { children: ReactNode }) {
    super(props)
    this.state = { hasError: false, error: null, errorInfo: null }
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error, errorInfo: null }
  }

  componentDidCatch(error: Error, errorInfo: any) {
    console.error('Error caught by boundary:', error, errorInfo)
    this.setState({ error, errorInfo })
  }

  render() {
    if (this.state.hasError) {
      return (
        <div>
          <h2>Something went wrong.</h2>
          <details style={{ whiteSpace: 'pre-wrap' }}>
            {this.state.error && this.state.error.toString()}
            <br />
            {this.state.errorInfo.componentStack}
          </details>
        </div>
      )
    }

    return this.props.children
  }
}
```

---

**Next**: See [Testing Guide](testing.md) for comprehensive testing strategies or [Contributing Guidelines](contributing.md) for the contribution process.