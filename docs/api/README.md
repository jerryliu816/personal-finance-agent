# API Documentation

Complete REST API reference for Personal Finance Agent backend services.

## 🔗 Base URL

```
http://localhost:8000
```

## 📋 API Overview

The Personal Finance Agent API provides endpoints for:
- **Health & Status**: Application health monitoring
- **Settings Management**: User configuration and preferences
- **Document Processing**: Financial document upload and analysis
- **Financial Profile**: Aggregated financial data and insights
- **Chat Interface**: AI-powered financial assistant
- **RAG Documents**: Reference document management (planned)

## 🔐 Authentication

Currently, the API uses **localhost-only access** for security. No authentication tokens are required as the application is designed for single-user desktop use.

**Security Model**:
- API only accessible from `localhost` (127.0.0.1)
- No external network access allowed
- CORS configured for frontend-only access

## 📊 Response Format

### Success Response
```json
{
  "data": {
    // Response data
  },
  "status": "success",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### Error Response
```json
{
  "error": {
    "message": "Error description",
    "code": "ERROR_CODE",
    "details": {}
  },
  "status": "error",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### HTTP Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `404` - Not Found
- `422` - Unprocessable Entity
- `500` - Internal Server Error

## 🏥 Health & Status

### Health Check
Check API server status and connectivity.

```http
GET /health
```

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00Z",
  "version": "1.0.0",
  "uptime": 3600
}
```

## ⚙️ Settings Management

### Get Settings
Retrieve current application settings.

```http
GET /api/settings
```

**Response**:
```json
{
  "id": 1,
  "llm_provider": "openai",
  "llm_api_key": "sk-***masked***",
  "gmail_server": "imap.gmail.com",
  "gmail_username": "user@gmail.com",
  "gmail_password": "***masked***",
  "auto_check_email": false,
  "check_interval": 60,
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

### Update Settings
Update application configuration.

```http
POST /api/settings
Content-Type: application/json
```

**Request Body**:
```json
{
  "llm_provider": "openai",
  "llm_api_key": "sk-your-api-key-here",
  "gmail_server": "imap.gmail.com",
  "gmail_username": "user@gmail.com",
  "gmail_password": "app-password",
  "auto_check_email": true,
  "check_interval": 120
}
```

**Response**:
```json
{
  "id": 1,
  "llm_provider": "openai",
  "llm_api_key": "sk-***masked***",
  "gmail_server": "imap.gmail.com",
  "gmail_username": "user@gmail.com",
  "gmail_password": "***masked***",
  "auto_check_email": true,
  "check_interval": 120,
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T13:00:00Z"
}
```

## 📄 Document Management

### Upload Document
Upload and analyze a financial document.

```http
POST /api/documents/upload
Content-Type: multipart/form-data
```

**Form Parameters**:
- `file` (required): PDF file to upload
- `document_type` (optional): Document type hint ("financial", "credit_card", "bank_statement", etc.)

**Example**:
```bash
curl -X POST "http://localhost:8000/api/documents/upload" \
  -F "file=@statement.pdf" \
  -F "document_type=credit_card"
```

**Response**:
```json
{
  "id": 1,
  "filename": "statement.pdf",
  "filepath": "/data/uploads/statement.pdf",
  "document_type": "credit_card",
  "analysis_result": "{\"document_type\":\"credit_card\",\"transactions\":[...]}",
  "file_size": 1048576,
  "processed": true,
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:05:00Z"
}
```

### Get Documents
Retrieve list of uploaded documents.

```http
GET /api/documents
```

**Response**:
```json
[
  {
    "id": 1,
    "filename": "statement.pdf",
    "filepath": "/data/uploads/statement.pdf",
    "document_type": "credit_card",
    "analysis_result": "{...}",
    "file_size": 1048576,
    "processed": true,
    "created_at": "2024-01-01T12:00:00Z",
    "updated_at": "2024-01-01T12:05:00Z"
  }
]
```

### Delete Document
Remove a document and its analysis.

```http
DELETE /api/documents/{document_id}
```

**Parameters**:
- `document_id` (path): ID of document to delete

**Response**:
```json
{
  "message": "Document deleted successfully"
}
```

**Error Responses**:
```json
// Document not found
{
  "error": {
    "message": "Document not found",
    "code": "DOCUMENT_NOT_FOUND"
  },
  "status": "error"
}
```

## 💰 Financial Profile

### Get Financial Profile
Retrieve aggregated financial profile and summary.

```http
GET /api/profile
```

**Response**:
```json
{
  "total_assets": 50000.00,
  "total_liabilities": 15000.00,
  "net_worth": 35000.00,
  "monthly_income": 5000.00,
  "monthly_expenses": 3500.00,
  "investment_portfolio": {
    "AAPL": 5000.00,
    "MSFT": 3000.00,
    "SPY": 10000.00
  },
  "credit_accounts": [
    {
      "name": "Chase Sapphire",
      "balance": 1500.00,
      "limit": 10000.00,
      "rate": 18.99
    }
  ],
  "recent_transactions": [
    {
      "date": "2024-01-01",
      "description": "Grocery Store",
      "amount": -85.50,
      "category": "food",
      "subcategory": "groceries"
    }
  ],
  "last_updated": "2024-01-01T12:00:00Z"
}
```

## 💬 Chat Interface

### Send Chat Message
Send a message to the AI financial assistant.

```http
POST /api/chat
Content-Type: application/json
```

**Request Body**:
```json
{
  "message": "What's my current net worth?",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

**Response**:
```json
{
  "response": "Based on your financial profile, your current net worth is $35,000. This is calculated from your total assets of $50,000 minus your total liabilities of $15,000. Your net worth has increased by 12% over the past quarter, primarily due to investment gains in your portfolio."
}
```

### Get Chat History
Retrieve recent chat conversation history.

```http
GET /api/chat/history
```

**Query Parameters**:
- `limit` (optional): Number of messages to return (default: 50)

**Response**:
```json
[
  {
    "message": "What's my current net worth?",
    "response": "Based on your財政profile...",
    "timestamp": "2024-01-01T12:00:00Z"
  },
  {
    "message": "How much did I spend on dining last month?",
    "response": "According to your transaction data...",
    "timestamp": "2024-01-01T11:30:00Z"
  }
]
```

## 📚 RAG Documents (Planned)

### Upload RAG Document
Upload reference documents for enhanced AI context.

```http
POST /api/rag/upload
Content-Type: multipart/form-data
```

**Form Parameters**:
- `file` (required): Document file (PDF, TXT, DOC, DOCX)

**Response**:
```json
{
  "id": 1,
  "filename": "financial_guide.pdf",
  "filepath": "/data/rag/financial_guide.pdf",
  "content": "Extracted text content...",
  "chunk_count": 25,
  "processed": true,
  "created_at": "2024-01-01T12:00:00Z"
}
```

### Get RAG Documents
List uploaded RAG documents.

```http
GET /api/rag/documents
```

**Response**:
```json
[
  {
    "id": 1,
    "filename": "financial_guide.pdf",
    "filepath": "/data/rag/financial_guide.pdf",
    "chunk_count": 25,
    "processed": true,
    "created_at": "2024-01-01T12:00:00Z"
  }
]
```

### Delete RAG Document
Remove a RAG document and its embeddings.

```http
DELETE /api/rag/documents/{document_id}
```

## 🔍 Error Handling

### Common Error Codes

#### Document Processing Errors
```json
{
  "error": {
    "message": "Unsupported file format",
    "code": "UNSUPPORTED_FORMAT",
    "details": {
      "supported_formats": ["pdf"],
      "provided_format": "docx"
    }
  }
}
```

#### Configuration Errors
```json
{
  "error": {
    "message": "LLM API key not configured",
    "code": "API_KEY_MISSING",
    "details": {
      "provider": "openai",
      "configuration_url": "/settings"
    }
  }
}
```

#### Processing Errors
```json
{
  "error": {
    "message": "Document analysis failed",
    "code": "ANALYSIS_FAILED",
    "details": {
      "document_id": 123,
      "error_type": "ai_processing_error",
      "retry_possible": true
    }
  }
}
```

### Error Response Structure
```typescript
interface APIError {
  error: {
    message: string          // Human-readable error message
    code: string            // Machine-readable error code
    details?: any           // Additional error context
  }
  status: "error"
  timestamp: string         // ISO 8601 timestamp
}
```

## 📊 Data Models

### Document Model
```typescript
interface Document {
  id: number
  filename: string
  filepath: string
  document_type: string
  analysis_result?: string  // JSON string of analysis results
  file_size: number
  processed: boolean
  created_at: string       // ISO 8601 timestamp
  updated_at: string       // ISO 8601 timestamp
}
```

### Financial Profile Model
```typescript
interface FinancialProfile {
  total_assets: number
  total_liabilities: number
  net_worth: number
  monthly_income: number
  monthly_expenses: number
  investment_portfolio: Record<string, number>
  credit_accounts: CreditAccount[]
  recent_transactions: Transaction[]
  last_updated: string     // ISO 8601 timestamp
}

interface Transaction {
  date: string            // YYYY-MM-DD format
  description: string
  amount: number         // Negative for expenses, positive for income
  category: string
  subcategory: string
}

interface CreditAccount {
  name: string
  balance: number
  limit: number
  rate: number          // Annual percentage rate
}
```

### Settings Model
```typescript
interface Settings {
  id?: number
  llm_provider: "openai" | "anthropic"
  llm_api_key: string
  gmail_server?: string
  gmail_username?: string
  gmail_password?: string
  auto_check_email: boolean
  check_interval: number  // Minutes
  created_at?: string
  updated_at?: string
}
```

## 🔧 Advanced Usage

### Batch Operations
For processing multiple documents, upload them sequentially rather than in parallel to avoid overwhelming the AI service:

```javascript
async function uploadDocuments(files) {
  const results = []
  
  for (const file of files) {
    try {
      const result = await uploadDocument(file)
      results.push(result)
      
      // Wait between uploads to respect rate limits
      await new Promise(resolve => setTimeout(resolve, 1000))
    } catch (error) {
      console.error(`Failed to upload ${file.name}:`, error)
      results.push({ error, filename: file.name })
    }
  }
  
  return results
}
```

### Polling for Processing Status
For long-running document analysis, poll the document status:

```javascript
async function waitForProcessing(documentId, maxAttempts = 30) {
  for (let i = 0; i < maxAttempts; i++) {
    const doc = await getDocument(documentId)
    
    if (doc.processed) {
      return doc
    }
    
    // Wait 2 seconds before next check
    await new Promise(resolve => setTimeout(resolve, 2000))
  }
  
  throw new Error('Document processing timeout')
}
```

### Error Retry Logic
Implement exponential backoff for transient errors:

```javascript
async function uploadWithRetry(file, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await uploadDocument(file)
    } catch (error) {
      if (attempt === maxRetries) throw error
      
      // Exponential backoff: 1s, 2s, 4s
      const delay = Math.pow(2, attempt - 1) * 1000
      await new Promise(resolve => setTimeout(resolve, delay))
    }
  }
}
```

## 📈 Rate Limits

### Current Limits
- **Document Upload**: 10 files per minute
- **Chat Messages**: 30 messages per minute
- **API Requests**: 1000 requests per hour

### Rate Limit Headers
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1641024000
```

Rate limits are applied per API endpoint and reset on a rolling window basis.

## 🔄 Webhooks (Planned)

Future versions will support webhooks for real-time notifications:

```http
POST /api/webhooks
Content-Type: application/json

{
  "url": "https://your-app.com/webhook",
  "events": ["document.processed", "analysis.completed"],
  "secret": "webhook-secret"
}
```

---

**Interactive API Documentation**: Visit `http://localhost:8000/docs` when the application is running for Swagger UI documentation with live API testing capabilities.