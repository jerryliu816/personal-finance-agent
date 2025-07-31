# Personal Finance Agent

An AI-powered personal finance analysis application for Windows that processes financial documents, builds your financial profile, and provides intelligent insights through chat interactions.

## Features

### 🏦 Document Analysis
- **PDF Processing**: Upload credit card statements, bank statements, investment reports, and tax documents
- **AI-Powered Extraction**: Automatically categorize transactions and extract financial data
- **Multi-Format Support**: Handles various financial document formats with intelligent parsing
- **MCP Integration**: Uses Model Context Protocol for robust PDF processing

### 💬 AI Chat Assistant
- **Contextual Responses**: Ask questions about your finances with full context from your documents
- **LLM Support**: Compatible with OpenAI GPT-4 and Anthropic Claude
- **Personal Insights**: Get personalized financial advice based on your actual data
- **Chat History**: Persistent conversation history for ongoing financial planning

### 📊 Financial Dashboard
- **Net Worth Tracking**: Visual representation of assets vs liabilities
- **Investment Portfolio**: Pie charts and detailed breakdowns of your investments
- **Transaction Analysis**: Recent transactions with categorization and insights
- **Monthly Trends**: Track income, expenses, and savings over time

### ⚙️ Advanced Features
- **System Tray Integration**: Runs quietly in the background with easy access
- **Email Integration**: Automatic processing of financial documents from email (planned)
- **RAG System**: Upload reference documents for enhanced AI responses (planned)
- **Secure Storage**: Encrypted local storage of all financial data and credentials

## Installation

### Requirements
- Windows 10 or 11 (64-bit)
- Internet connection for AI processing

### Easy Installation
1. Download the latest installer from the [Releases](https://github.com/yourusername/personal-finance-agent/releases) page
2. Run `PersonalFinanceAgent-Setup-1.0.0.exe`
3. Follow the installation wizard
4. Launch from Start Menu or Desktop shortcut

### Development Setup

#### Prerequisites
- Python 3.9 or higher
- Node.js 18 or higher
- Git

#### Installation Steps
```bash
# Clone the repository
git clone https://github.com/yourusername/personal-finance-agent.git
cd personal-finance-agent

# Install Python dependencies
pip install -r requirements.txt

# Install and build frontend
cd src/ui/frontend
npm install
npm run build
cd ../../..

# Run the application
python -m src.tray.tray_app
```

## Configuration

### LLM Setup
1. Open the application and click the system tray icon
2. Select "Settings" from the menu
3. Choose your preferred LLM provider:
   - **OpenAI**: Get an API key from [OpenAI Platform](https://platform.openai.com/)
   - **Anthropic**: Get an API key from [Anthropic Console](https://console.anthropic.com/)
4. Enter your API key and save settings

### Email Integration (Optional)
Configure automatic document processing from Gmail:
1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password for the application
3. Enter your Gmail credentials in Settings
4. Enable automatic email checking

## Usage

### Getting Started
1. **Configure API Key**: Set up your LLM provider API key in Settings
2. **Upload Documents**: Use the Document Analysis page to upload your first PDF
3. **Review Analysis**: Check the AI-generated analysis and extracted data
4. **Chat with Assistant**: Ask questions about your finances in the Chat interface

### Document Types Supported
- **Credit Card Statements**: Automatic transaction categorization and balance tracking
- **Bank Statements**: Checking and savings account analysis
- **Investment Reports**: Portfolio tracking and performance analysis
- **Tax Documents**: Income and deduction categorization
- **Insurance Policies**: Coverage and premium tracking
- **Loan Statements**: Balance and payment tracking

### Chat Examples
Try asking questions like:
- "What's my current net worth?"
- "How much did I spend on dining out last month?"
- "What are my biggest expenses?"
- "Should I increase my investment contributions?"
- "How is my spending trending compared to my income?"

## Security & Privacy

### Data Protection
- **Local Storage**: All data is stored locally on your device
- **Encryption**: API keys and sensitive data are encrypted using Windows DPAPI
- **No Cloud Storage**: Financial data never leaves your device except for AI processing
- **Minimal Data Sharing**: Only document text is sent to LLM providers for analysis

### API Usage
- **OpenAI**: Document text sent for analysis, no storage by OpenAI
- **Anthropic**: Document text sent for analysis, subject to Anthropic's privacy policy
- **MCP Servers**: All processing happens locally

## Architecture

### Components
- **FastAPI Backend**: REST API for data management and AI integration
- **React Frontend**: Modern web-based user interface
- **System Tray App**: Windows desktop integration
- **SQLite Database**: Local data storage
- **MCP Servers**: PDF processing and stock data integration
- **ChromaDB**: Vector storage for RAG functionality (planned)

### Technology Stack
- **Backend**: Python, FastAPI, SQLAlchemy, Pydantic
- **Frontend**: React, TypeScript, Material-UI, Vite
- **Desktop**: pystray, Pillow, uvicorn
- **AI**: OpenAI API, Anthropic API, sentence-transformers
- **Database**: SQLite, ChromaDB
- **Packaging**: PyInstaller, Inno Setup

## Development

### Project Structure
```
personal-finance-agent/
├── src/
│   ├── core/                 # Core business logic
│   ├── mcp/                  # MCP server implementations
│   ├── ui/                   # User interface
│   │   ├── backend/          # FastAPI backend
│   │   └── frontend/         # React frontend
│   ├── tray/                 # System tray application
│   └── rag/                  # RAG system components
├── config/                   # Configuration files
├── data/                     # Local database and files
├── installer/                # Windows installer scripts
└── requirements.txt          # Python dependencies
```

### Building from Source

#### Development Mode
```bash
# Backend
uvicorn src.ui.backend.main:app --host 127.0.0.1 --port 8000 --reload

# Frontend (in another terminal)
cd src/ui/frontend
npm run dev

# System Tray
python -m src.tray.tray_app
```

#### Production Build
```bash
# Build everything
python installer/build_installer.py

# Create installer (requires Inno Setup on Windows)
iscc installer/PersonalFinanceAgent.iss
```

## Roadmap

### Phase 1 ✅ (Current)
- Core document processing and analysis
- Basic financial dashboard
- Chat interface with financial context
- System tray integration

### Phase 2 🔄 (In Progress)
- RAG system for reference documents
- Enhanced investment tracking
- Spending trend analysis
- Budget planning tools

### Phase 3 📋 (Planned)
- Automatic email processing
- Advanced financial reporting
- Goal tracking and recommendations
- Multi-currency support

### Phase 4 📋 (Future)
- Mobile companion app
- Cloud sync (optional)
- Advanced AI financial planning
- Integration with financial institutions

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

### Getting Help
- 📖 [Documentation](https://github.com/yourusername/personal-finance-agent/wiki)
- 🐛 [Issue Tracker](https://github.com/yourusername/personal-finance-agent/issues)
- 💬 [Discussions](https://github.com/yourusername/personal-finance-agent/discussions)

### Common Issues
- **API Key Not Working**: Ensure you have sufficient credits and the correct key format
- **Documents Not Processing**: Check that PDFs are not password-protected or corrupted
- **Application Won't Start**: Verify Windows Defender hasn't quarantined the executable

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **OpenAI** and **Anthropic** for providing powerful language models
- **FastAPI** team for the excellent web framework
- **React** and **Material-UI** communities for frontend components
- **ChromaDB** team for vector database capabilities
- **Model Context Protocol** for standardized AI tool integration

---

**Disclaimer**: This application is for personal use only. Always verify AI-generated financial analysis and consult with qualified financial advisors for important financial decisions.