# Contributing Guidelines

Welcome to Personal Finance Agent! We're excited that you're interested in contributing to this project. This guide will help you get started and ensure your contributions align with our project standards.

## 🎯 How to Contribute

### Types of Contributions

We welcome various types of contributions:

#### 🐛 Bug Reports
- Report issues with clear reproduction steps
- Include system information and error logs
- Search existing issues first to avoid duplicates

#### 🚀 Feature Requests
- Propose new features or enhancements
- Explain the use case and expected behavior
- Consider if it fits the project scope

#### 📝 Code Contributions
- Bug fixes and improvements
- New features and functionality
- Performance optimizations
- Code refactoring

#### 📚 Documentation
- Fix typos and improve clarity
- Add examples and tutorials
- Translate documentation
- Update API documentation

#### 🧪 Testing
- Add test cases for existing functionality
- Improve test coverage
- Write integration tests
- Performance testing

## 🚀 Getting Started

### 1. Fork and Clone
```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/yourusername/personal-finance-agent.git
cd personal-finance-agent

# Add upstream remote
git remote add upstream https://github.com/originalowner/personal-finance-agent.git
```

### 2. Set Up Development Environment
Follow the [Developer Setup Guide](setup.md) to configure your development environment.

### 3. Create a Branch
```bash
# Update your fork
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b bugfix/issue-description
```

### 4. Make Your Changes
- Follow our [coding standards](#coding-standards)
- Write tests for new functionality
- Update documentation as needed
- Commit early and often with clear messages

### 5. Test Your Changes
```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/unit/
pytest tests/integration/

# Check code quality
flake8 src/
black --check src/
mypy src/

# Test frontend
cd src/ui/frontend
npm test
npm run lint
```

### 6. Submit Pull Request
```bash
# Push your branch
git push origin feature/your-feature-name

# Create pull request on GitHub
# Fill out the PR template completely
```

## 📋 Pull Request Process

### Before Submitting

#### Checklist
- [ ] Code follows project style guidelines
- [ ] All tests pass locally
- [ ] New code has appropriate test coverage
- [ ] Documentation updated (if applicable)
- [ ] No merge conflicts with main branch
- [ ] Commit messages follow conventional format
- [ ] Self-review completed

#### Testing Requirements
- **Unit Tests**: All new functions and classes must have unit tests
- **Integration Tests**: API endpoints and workflows need integration tests
- **Coverage**: Maintain or improve test coverage percentage
- **Manual Testing**: Test your changes in the actual application

### Pull Request Template

When creating a PR, fill out this template:

```markdown
## Description
Brief description of changes and motivation.

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Changes Made
- List specific changes
- Include any new dependencies
- Mention files modified

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed
- [ ] All tests pass

## Screenshots (if applicable)
Add screenshots for UI changes.

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No merge conflicts
```

### Review Process

#### What Reviewers Look For
1. **Functionality**: Does the code work as intended?
2. **Code Quality**: Is the code readable, maintainable, and efficient?
3. **Testing**: Are there adequate tests for the changes?
4. **Documentation**: Is documentation updated appropriately?
5. **Security**: Are there any security implications?
6. **Performance**: Will this impact application performance?

#### Review Timeline
- **Initial Review**: Within 2-3 business days
- **Follow-up Reviews**: Within 1-2 business days after updates
- **Merge**: After approval from at least one maintainer

## 📝 Coding Standards

### Python Code Style

#### PEP 8 Compliance
We use Black formatter with 88-character line length:
```python
# Good
def process_financial_document(
    file_path: str, document_type: str = "financial"
) -> Dict[str, Any]:
    """Process a financial document and return analysis results."""
    pass
```

#### Type Hints
Use type hints for all function parameters and return values:
```python
from typing import Dict, List, Optional, Union
from datetime import datetime

def analyze_transactions(
    transactions: List[Dict[str, Any]], 
    start_date: Optional[datetime] = None
) -> Dict[str, Union[int, float]]:
    """Analyze transactions and return summary statistics."""
    pass
```

#### Error Handling
Use specific exception types and proper error handling:
```python
class DocumentProcessingError(Exception):
    """Raised when document processing fails."""
    def __init__(self, message: str, error_code: str = None):
        super().__init__(message)
        self.error_code = error_code

try:
    result = process_document(file_path)
except DocumentProcessingError as e:
    logger.error(f"Processing failed: {e}")
    raise HTTPException(status_code=422, detail=str(e))
```

#### Docstring Format
Use Google-style docstrings:
```python
def calculate_net_worth(assets: float, liabilities: float) -> float:
    """
    Calculate net worth from assets and liabilities.
    
    Args:
        assets (float): Total asset value
        liabilities (float): Total liability value
    
    Returns:
        float: Net worth (assets - liabilities)
    
    Raises:
        ValueError: If assets or liabilities are negative
    
    Example:
        >>> calculate_net_worth(100000, 25000)
        75000.0
    """
    if assets < 0 or liabilities < 0:
        raise ValueError("Assets and liabilities must be non-negative")
    return assets - liabilities
```

### TypeScript/React Code Style

#### Component Structure
```typescript
// Use functional components with TypeScript
import React, { useState, useEffect } from 'react'
import { Button, Typography } from '@mui/material'

interface FinancialSummaryProps {
  netWorth: number
  onRefresh: () => void
}

export default function FinancialSummary({ 
  netWorth, 
  onRefresh 
}: FinancialSummaryProps) {
  const [loading, setLoading] = useState(false)

  const formatCurrency = (amount: number): string => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount)
  }

  return (
    <div>
      <Typography variant="h4">
        Net Worth: {formatCurrency(netWorth)}
      </Typography>
      <Button onClick={onRefresh} disabled={loading}>
        Refresh
      </Button>
    </div>
  )
}
```

#### API Services
```typescript
// services/financialApi.ts
import axios from 'axios'

export interface FinancialProfile {
  netWorth: number
  monthlyIncome: number
  monthlyExpenses: number
}

export const financialApi = {
  getProfile: async (): Promise<FinancialProfile> => {
    const response = await axios.get<FinancialProfile>('/api/profile')
    return response.data
  },

  updateProfile: async (profile: Partial<FinancialProfile>): Promise<void> => {
    await axios.patch('/api/profile', profile)
  }
}
```

### Database Guidelines

#### Schema Changes
```python
# Always use Alembic migrations for schema changes
# Create migration file
alembic revision --autogenerate -m "Add new table for investment tracking"

# Example migration
def upgrade():
    op.create_table(
        'investment_holdings',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('symbol', sa.String(10), nullable=False),
        sa.Column('shares', sa.Numeric(10, 4), nullable=False),
        sa.Column('purchase_date', sa.DateTime, nullable=False),
    )
    op.create_index('ix_investment_holdings_symbol', 'investment_holdings', ['symbol'])
```

#### Query Optimization
```python
# Good: Use indexes and specific queries
def get_recent_transactions(db: Session, limit: int = 10) -> List[Transaction]:
    return db.query(Transaction)\
        .order_by(Transaction.date.desc())\
        .limit(limit)\
        .all()

# Bad: Loading all data then filtering in Python
def get_recent_transactions_bad(db: Session) -> List[Transaction]:
    all_transactions = db.query(Transaction).all()
    return sorted(all_transactions, key=lambda x: x.date, reverse=True)[:10]
```

## 🧪 Testing Guidelines

### Unit Tests

#### Test Structure
```python
# tests/unit/test_document_processor.py
import pytest
from unittest.mock import Mock, patch
from src.core.document_processor import DocumentProcessor

class TestDocumentProcessor:
    def setup_method(self):
        """Set up test fixtures."""
        self.processor = DocumentProcessor()
        self.sample_text = "Sample financial document text"

    def test_classify_document_type_credit_card(self):
        """Test credit card document classification."""
        text = "CREDIT CARD STATEMENT\nBalance: $1,234.56"
        result = self.processor._classify_document_type(text)
        assert result == "credit_card"

    @patch('src.core.document_processor.DocumentProcessor._extract_text_via_mcp')
    async def test_process_document_success(self, mock_extract):
        """Test successful document processing."""
        mock_extract.return_value = self.sample_text
        
        result = await self.processor.process_document("test.pdf")
        
        assert result["success"] is True
        assert "document_type" in result

    def test_process_document_file_not_found(self):
        """Test handling of non-existent files."""
        with pytest.raises(FileNotFoundError):
            asyncio.run(self.processor.process_document("nonexistent.pdf"))
```

#### Test Data
```python
# tests/fixtures/financial_data.py
import pytest

@pytest.fixture
def sample_transactions():
    """Sample transaction data for testing."""
    return [
        {
            "date": "2024-01-15",
            "description": "Grocery Store",
            "amount": -85.50,
            "category": "food"
        },
        {
            "date": "2024-01-16",
            "description": "Salary Deposit",
            "amount": 3000.00,
            "category": "income"
        }
    ]

@pytest.fixture
def mock_financial_profile():
    """Mock financial profile for testing."""
    return {
        "net_worth": 50000.00,
        "monthly_income": 5000.00,
        "monthly_expenses": 3500.00,
        "investment_portfolio": {
            "AAPL": 5000.00,
            "MSFT": 3000.00
        }
    }
```

### Integration Tests

#### API Testing
```python
# tests/integration/test_api.py
import pytest
from fastapi.testclient import TestClient
from src.ui.backend.main import app

class TestDocumentAPI:
    def setup_method(self):
        """Set up test client."""
        self.client = TestClient(app)

    def test_upload_document_success(self):
        """Test successful document upload."""
        with open("tests/fixtures/sample.pdf", "rb") as f:
            files = {"file": ("sample.pdf", f, "application/pdf")}
            response = self.client.post("/api/documents/upload", files=files)
        
        assert response.status_code == 200
        data = response.json()
        assert data["filename"] == "sample.pdf"
        assert data["processed"] is True

    def test_get_financial_profile(self):
        """Test financial profile endpoint."""
        response = self.client.get("/api/profile")
        
        assert response.status_code == 200
        data = response.json()
        assert "net_worth" in data
        assert "monthly_income" in data
```

### Frontend Testing

#### Component Testing
```typescript
// src/__tests__/FinancialSummary.test.tsx
import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import '@testing-library/jest-dom'
import FinancialSummary from '../components/FinancialSummary'

describe('FinancialSummary', () => {
  const mockProps = {
    netWorth: 50000,
    onRefresh: jest.fn()
  }

  test('displays net worth correctly', () => {
    render(<FinancialSummary {...mockProps} />)
    expect(screen.getByText('Net Worth: $50,000.00')).toBeInTheDocument()
  })

  test('calls onRefresh when button clicked', () => {
    render(<FinancialSummary {...mockProps} />)
    fireEvent.click(screen.getByText('Refresh'))
    expect(mockProps.onRefresh).toHaveBeenCalledTimes(1)
  })
})
```

## 📚 Documentation Standards

### Code Documentation

#### README Updates
When adding new features, update relevant README sections:
- Installation requirements
- Usage examples
- Configuration options
- Troubleshooting steps

#### API Documentation
Update OpenAPI schemas for new endpoints:
```python
@router.post("/documents/analyze", response_model=AnalysisResponse)
async def analyze_document(
    document_id: int = Path(..., description="ID of document to analyze"),
    analysis_type: str = Query("full", description="Type of analysis to perform")
) -> AnalysisResponse:
    """
    Perform advanced analysis on a financial document.
    
    This endpoint provides detailed analysis beyond basic processing,
    including trend analysis and category breakdowns.
    
    - **document_id**: ID of previously uploaded document
    - **analysis_type**: "full", "summary", or "trends"
    
    Returns detailed analysis results with insights and recommendations.
    """
```

### User Documentation

#### Examples and Tutorials
When adding features, include user-facing examples:
```markdown
## Using Investment Tracking

To track your investment portfolio:

1. Upload your brokerage statement
2. The system will automatically detect holdings
3. View your portfolio breakdown in the dashboard

### Supported Formats
- Schwab brokerage statements
- Fidelity account summaries  
- Vanguard portfolio reports
```

## 🔒 Security Guidelines

### Code Security

#### Input Validation
```python
from pydantic import BaseModel, Field, validator

class DocumentUpload(BaseModel):
    file_size: int = Field(..., gt=0, le=50_000_000)  # Max 50MB
    document_type: str = Field(..., regex="^[a-zA-Z_]+$")
    
    @validator('document_type')
    def validate_document_type(cls, v):
        allowed_types = ['credit_card', 'bank_statement', 'investment']
        if v not in allowed_types:
            raise ValueError(f'Document type must be one of {allowed_types}')
        return v
```

#### SQL Injection Prevention
```python
# Good: Use parameterized queries
def get_transactions_by_category(db: Session, category: str) -> List[Transaction]:
    return db.query(Transaction)\
        .filter(Transaction.category == category)\
        .all()

# Bad: String concatenation
def get_transactions_bad(db: Session, category: str) -> List[Transaction]:
    query = f"SELECT * FROM transactions WHERE category = '{category}'"
    return db.execute(query).fetchall()
```

#### API Security
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

def validate_api_access(token: str = Depends(security)):
    """Validate API access token."""
    if not is_valid_token(token.credentials):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
```

### Data Privacy

#### PII Handling
```python
import re

def sanitize_financial_data(text: str) -> str:
    """Remove personally identifiable information from text."""
    # Remove SSNs
    text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN_REDACTED]', text)
    
    # Remove account numbers
    text = re.sub(r'\b\d{10,16}\b', '[ACCOUNT_REDACTED]', text)
    
    # Remove phone numbers
    text = re.sub(r'\b\d{3}-\d{3}-\d{4}\b', '[PHONE_REDACTED]', text)
    
    return text
```

## 🐛 Bug Report Guidelines

### Issue Template

When reporting bugs, use this template:

```markdown
**Bug Description**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

**Expected Behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment**
- OS: [e.g. Windows 11]
- Application Version: [e.g. 1.0.0]
- Browser: [e.g. Chrome 120.0]

**Additional Context**
Any other context about the problem.

**Log Files**
Include relevant log entries if available.
```

### Security Issues

For security vulnerabilities:
1. **Don't create public issues**
2. **Email maintainers privately**
3. **Include proof of concept if safe**
4. **Allow time for fix before disclosure**

## 🎯 Feature Request Guidelines

### Feature Template

```markdown
**Feature Description**
Clear description of the proposed feature.

**Problem Statement**
What problem does this solve?

**Proposed Solution**
How would you like this to work?

**Alternative Solutions**
Other approaches you've considered.

**Use Cases**
Specific scenarios where this would be helpful.

**Additional Context**
Screenshots, mockups, or examples.
```

### Feature Evaluation Criteria

We evaluate features based on:
1. **User Value**: How many users would benefit?
2. **Complexity**: Implementation effort required
3. **Maintenance**: Ongoing support needed
4. **Security**: Privacy and security implications
5. **Scope**: Fits project vision and goals

## 📊 Project Governance

### Decision Making

#### Minor Changes
- Bug fixes, documentation updates, small improvements
- Can be merged by any maintainer after review

#### Major Changes
- New features, breaking changes, architecture changes
- Require discussion and consensus among maintainers

#### Controversial Changes
- Use GitHub Discussions for community input
- Consider RFC (Request for Comments) process
- Final decision by project maintainers

### Maintainer Responsibilities

#### Code Review
- Review PRs within 2-3 business days
- Provide constructive feedback
- Ensure quality and security standards

#### Issue Triage
- Label and categorize issues
- Request additional information when needed
- Close duplicates and invalid issues

#### Release Management
- Create release notes
- Tag releases and create distribution packages
- Coordinate security updates

## ❓ Getting Help

### Resources
- **Documentation**: Check existing docs first
- **GitHub Discussions**: Ask questions and share ideas
- **Issues**: Search existing issues before creating new ones
- **Discord/Slack**: Real-time community support (if available)

### Mentoring

New contributors can request mentoring:
- **Good First Issues**: Tagged for newcomers
- **Pair Programming**: Available for complex features
- **Code Reviews**: Detailed feedback for learning
- **Architecture Guidance**: Help with design decisions

## 🏆 Recognition

### Contributors

We recognize contributors through:
- **GitHub Contributors**: Automatic recognition
- **Release Notes**: Major contributors mentioned
- **Hall of Fame**: Special recognition for significant contributions

### Types of Recognition
- **Code Contributions**: Features, bug fixes, improvements
- **Documentation**: Writing, editing, translation
- **Testing**: Bug reports, test writing, QA
- **Community**: Helping others, moderation, events

---

Thank you for contributing to Personal Finance Agent! Your efforts help make financial management more accessible and intelligent for everyone. 🎉