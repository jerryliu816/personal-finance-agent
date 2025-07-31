# User Manual

Complete guide to using Personal Finance Agent's features.

## 📖 Table of Contents

- [Getting Started](#getting-started)
- [Dashboard Overview](#dashboard-overview)
- [Document Analysis](#document-analysis)
- [Chat Assistant](#chat-assistant)
- [Settings Configuration](#settings-configuration)
- [RAG Documents](#rag-documents)
- [Data Management](#data-management)
- [Tips and Best Practices](#tips-and-best-practices)

## 🚀 Getting Started

### System Tray Interface

Personal Finance Agent runs as a system tray application. Look for the green dollar sign icon in your system tray (bottom-right corner of your screen).

**Right-click the icon** to access:
- 🏠 **Open Finance Agent** - Main dashboard
- ⚙️ **Settings** - Configuration page
- 📄 **Document Analysis** - Upload and analyze documents
- 💬 **Chat Interface** - AI assistant
- 📚 **RAG Documents** - Reference document management
- ❌ **Quit** - Exit the application

### First Time Setup

1. **Configure API Key**: Essential for AI processing
2. **Upload Documents**: Build your financial profile
3. **Explore Dashboard**: View your financial overview
4. **Chat with Assistant**: Ask questions about your finances

## 📊 Dashboard Overview

The dashboard provides a comprehensive view of your financial health.

### Key Metrics Cards

#### Net Worth
- **Calculation**: Total Assets - Total Liabilities
- **Color Coding**: 
  - 🟢 Green: Positive net worth
  - 🔴 Red: Negative net worth
- **Updates**: Automatically recalculated when new documents are processed

#### Monthly Income
- **Source**: Income transactions from uploaded documents
- **Calculation**: Average over the last 3 months
- **Includes**: Salary, bonuses, investment income, other income sources

#### Monthly Expenses
- **Source**: Expense transactions from uploaded documents
- **Calculation**: Average over the last 3 months
- **Categories**: Housing, food, transportation, entertainment, etc.

#### Monthly Savings
- **Calculation**: Monthly Income - Monthly Expenses
- **Insight**: Shows your financial trajectory

### Visual Charts

#### Assets vs Liabilities Bar Chart
- **Purpose**: Visual comparison of what you own vs what you owe
- **Categories**:
  - **Assets**: Cash, investments, property, etc.
  - **Liabilities**: Credit card debt, loans, mortgages, etc.

#### Investment Portfolio Pie Chart
- **Purpose**: Breakdown of your investment holdings
- **Data Source**: Investment account statements
- **Features**: 
  - Hover for exact values
  - Color-coded by asset type
  - Percentage and dollar amounts

### Recent Transactions

- **Display**: Last 10 transactions across all accounts
- **Information**: Date, description, amount, category
- **Features**:
  - Color coding (green for income, red for expenses)
  - Category chips for easy identification
  - Sorted by date (newest first)

## 📄 Document Analysis

Transform your financial documents into structured data and insights.

### Supported Document Types

#### Credit Card Statements
- **Auto-detects**: Card type, statement period, balance information
- **Extracts**: Individual transactions with dates, amounts, merchants
- **Categorizes**: Dining, gas, shopping, travel, etc.
- **Insights**: Spending patterns, largest expenses, category breakdowns

#### Bank Statements
- **Supports**: Checking and savings accounts
- **Extracts**: Deposits, withdrawals, transfers, fees
- **Tracks**: Account balances, cash flow patterns
- **Identifies**: Income sources, recurring payments

#### Investment Reports
- **Processes**: Brokerage statements, 401(k) reports, IRA statements
- **Extracts**: Holdings, transactions, performance data
- **Tracks**: Portfolio allocation, gains/losses, dividend income
- **Analyzes**: Asset allocation, risk distribution

#### Tax Documents
- **Handles**: W-2s, 1099s, tax returns
- **Extracts**: Income sources, deductions, tax payments
- **Categorizes**: Different types of income and expenses
- **Useful for**: Annual financial planning, tax preparation

### Upload Process

#### Step 1: Access Document Analysis
- Click the tray icon → **Document Analysis**
- Or open the main application and navigate to the Documents tab

#### Step 2: Upload Document
- **Drag and drop** PDF files into the upload area
- Or click **Choose File** to browse
- **File Requirements**:
  - PDF format only
  - Not password-protected
  - Reasonable file size (under 50MB)

#### Step 3: Processing
- **AI Analysis**: Document is processed using your configured LLM
- **Time**: Usually 30-60 seconds depending on document complexity
- **Progress**: Loading indicator shows processing status

#### Step 4: Review Results
- **Analysis Summary**: Overview of extracted data
- **Transaction List**: Individual transactions with categories
- **Insights**: AI-generated observations about spending patterns
- **Raw Data**: Full JSON analysis available for review

### Document Management

#### Document List
- **View**: All uploaded documents with metadata
- **Information**: Filename, size, upload date, processing status
- **Actions**: View analysis, delete document

#### Document Status
- **Processing**: Document is being analyzed
- **Processed**: Analysis complete, data extracted
- **Error**: Issue with processing (check document format)

#### Viewing Analysis Results
- Click the **view icon** next to any document
- See detailed JSON analysis including:
  - Extracted transactions
  - Account information
  - Summary statistics
  - AI insights and observations

## 💬 Chat Assistant

Your personal AI financial advisor with full access to your financial profile.

### Getting Started with Chat

#### First Questions to Try
```
"What's my current financial situation?"
"How much did I spend last month?"
"What are my biggest expenses?"
"Show me my investment portfolio breakdown"
"How is my spending trending?"
```

#### Types of Questions You Can Ask

**Financial Overview**
- Net worth, assets, liabilities
- Income and expense summaries
- Monthly financial trends

**Spending Analysis**
- Category breakdowns
- Largest expenses
- Spending patterns over time
- Comparisons between months

**Investment Insights**
- Portfolio allocation
- Performance analysis
- Investment recommendations

**Financial Planning**
- Budget recommendations
- Savings goals
- Debt payoff strategies

### Chat Features

#### Context Awareness
- The AI has access to your complete financial profile
- Responses include specific numbers from your actual data
- Can reference recent transactions and trends

#### Conversation History
- All chat conversations are saved locally
- Access previous conversations and advice
- Build on previous discussions for deeper insights

#### Smart Responses
- Personalized advice based on your financial situation
- References specific transactions and patterns
- Provides actionable recommendations

### Advanced Chat Usage

#### Detailed Analysis Requests
```
"Break down my dining expenses by restaurant for the last 6 months"
"Compare my current spending to the previous quarter"
"What percentage of my income goes to each expense category?"
```

#### Financial Planning Questions
```
"Based on my spending, how much should I budget for groceries?"
"If I want to save $10,000 this year, how much should I save monthly?"
"Should I pay off credit card debt or invest in my 401k first?"
```

#### Investment Analysis
```
"How is my portfolio diversified across asset classes?"
"Which of my investments has the best return?"
"Am I taking too much risk with my current allocation?"
```

## ⚙️ Settings Configuration

Customize Personal Finance Agent to work with your preferred services and settings.

### AI Language Model Configuration

#### Choosing a Provider

**OpenAI (Recommended for beginners)**
- **Model**: GPT-4
- **Pros**: Excellent general financial knowledge, faster responses
- **Cons**: Requires OpenAI account and credits
- **Cost**: ~$0.01-0.05 per document analysis

**Anthropic (Advanced users)**
- **Model**: Claude-3-Sonnet
- **Pros**: Strong analytical capabilities, good with complex documents
- **Cons**: More expensive, newer service
- **Cost**: ~$0.02-0.08 per document analysis

#### API Key Setup

1. **Get API Key**:
   - OpenAI: [platform.openai.com](https://platform.openai.com/) → API Keys
   - Anthropic: [console.anthropic.com](https://console.anthropic.com/) → API Keys

2. **Configure in Settings**:
   - Select your provider from dropdown
   - Paste API key in the text field
   - Click **Save Settings**

3. **Test Configuration**:
   - Upload a test document to verify everything works
   - Check for any error messages

### Email Integration (Optional)

Automatically process financial documents from your email.

#### Gmail Configuration

**Prerequisites**:
- Gmail account with 2-factor authentication enabled
- App password generated for the application

**Setup Steps**:
1. **Enable 2FA**: Go to Google Account settings → Security → 2-Step Verification
2. **Generate App Password**: Security → App passwords → Select app → Generate
3. **Configure Settings**:
   - Gmail Server: `imap.gmail.com`
   - Username: Your Gmail address
   - Password: Use the generated app password (not your regular password)
   - Check Interval: How often to check for new emails (default: 60 minutes)

#### Automatic Processing
- **Email Filtering**: Looks for PDF attachments in emails
- **Document Types**: Credit card statements, bank statements, investment reports
- **Processing**: Automatically analyzes and adds to your financial profile
- **Notifications**: System tray notifications for processed documents

### Security Settings

#### Data Storage
- **Location**: All data stored locally on your computer
- **Encryption**: API keys encrypted using Windows DPAPI
- **Privacy**: No cloud storage, data doesn't leave your device except for AI processing

#### API Security
- **Key Storage**: Encrypted and stored securely
- **Usage**: Only sent to configured LLM provider
- **Monitoring**: No usage tracking or data collection

## 📚 RAG Documents (Coming Soon)

Upload reference documents to enhance AI responses with additional context.

### Planned Features

#### Document Types
- Financial planning guides
- Investment research reports
- Tax documentation
- Personal financial notes

#### Processing
- **Chunking**: Documents split into searchable sections
- **Embedding**: Vector representations for semantic search
- **Retrieval**: Relevant sections automatically included in AI context

#### Enhanced Chat
- AI responses will include relevant information from your reference documents
- Citations showing which documents were referenced
- More comprehensive and personalized advice

## 📈 Data Management

### Data Export

#### Financial Profile Export
- Export your complete financial profile as JSON
- Includes all transactions, categories, and analysis results
- Useful for backup or migration to other tools

#### Transaction Export
- Export transactions as CSV for use in Excel or other tools
- Filter by date range, category, or account
- Includes all extracted transaction data

### Data Backup

#### Automatic Backup
- Application automatically backs up your database
- Backups stored in `%APPDATA%\Personal Finance Agent\backups\`
- Configurable backup frequency

#### Manual Backup
- Copy the entire data directory for complete backup
- Location: `%APPDATA%\Personal Finance Agent\data\`
- Includes database, uploaded documents, and settings

### Data Privacy

#### Local Storage Only
- All financial data stored locally on your computer
- No cloud storage or external databases
- Complete control over your financial information

#### AI Processing
- Only document text sent to AI providers for analysis
- No permanent storage by AI providers
- Processed data returns to your local system only

## 💡 Tips and Best Practices

### Document Management

#### Best Practices
- **Regular Uploads**: Upload statements monthly for accurate tracking
- **Consistent Naming**: Use consistent filenames for easy identification
- **Complete Coverage**: Include all account types for comprehensive analysis

#### Organization Tips
- Upload statements in chronological order
- Keep original documents in addition to uploading to the app
- Review AI analysis for accuracy and make mental notes of any patterns

### Getting Better AI Responses

#### Specific Questions
❌ "How are my finances?"  
✅ "What was my spending breakdown by category last month?"

#### Context-Rich Queries
❌ "Should I invest more?"  
✅ "Based on my current savings rate and expenses, should I increase my 401k contribution?"

#### Follow-up Questions
- Build on previous responses for deeper analysis
- Ask for specific recommendations based on your data
- Request explanations for AI recommendations

### Financial Analysis

#### Regular Review
- Check dashboard weekly for spending awareness
- Monthly deep-dive analysis using chat assistant
- Quarterly financial planning discussions with AI

#### Goal Setting
- Use AI to help set realistic financial goals
- Track progress toward goals using regular uploads
- Adjust strategies based on AI recommendations

### Security Best Practices

#### API Key Management
- Keep API keys secure and don't share them
- Monitor API usage on provider platforms
- Rotate keys periodically for security

#### Document Security
- Don't upload documents with sensitive information beyond financial data
- Regularly review uploaded documents list
- Use secure networks when uploading documents

---

**Need more help?** Check our [FAQ](../troubleshooting/faq.md) or [Troubleshooting Guide](../troubleshooting/common-issues.md).