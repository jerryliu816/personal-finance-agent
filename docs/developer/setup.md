# Developer Setup Guide

Complete guide to setting up a development environment for Personal Finance Agent.

## 🎯 Prerequisites

### Required Software

#### Python 3.9+
```bash
# Check current version
python --version

# Download from: https://www.python.org/downloads/
# Ensure "Add Python to PATH" is checked during installation
```

#### Node.js 18+
```bash
# Check current version
node --version
npm --version

# Download from: https://nodejs.org/
# Use LTS version (18.x or 20.x recommended)
```

#### Git
```bash
# Check current version
git --version

# Download from: https://git-scm.com/
# Use default settings during installation
```

#### Code Editor (Recommended)
- **VS Code**: With Python and TypeScript extensions
- **PyCharm**: Professional or Community edition
- **Alternative**: Any editor with Python and JavaScript support

## 📁 Repository Setup

### Clone Repository
```bash
# Clone the repository
git clone https://github.com/yourusername/personal-finance-agent.git
cd personal-finance-agent

# Check repository structure
ls -la
```

Expected structure:
```
personal-finance-agent/
├── src/                    # Source code
├── docs/                   # Documentation
├── installer/              # Build scripts
├── requirements.txt        # Python dependencies
├── pyproject.toml         # Project configuration
└── README.md              # Project overview
```

## 🐍 Python Environment Setup

### Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Verify activation (should show venv path)
which python
```

### Install Dependencies
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep fastapi
pip list | grep pystray
```

### Common Python Setup Issues

#### Permission Errors
```bash
# If you get permission errors, try:
pip install --user -r requirements.txt
```

#### Missing Visual C++ Build Tools (Windows)
```bash
# If you get compiler errors, install Visual Studio Build Tools:
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

#### SQLite Issues
```bash
# If SQLite errors occur:
pip install --upgrade sqlite3
```

## 🌐 Frontend Setup

### Navigate to Frontend Directory
```bash
cd src/ui/frontend
```

### Install Node Dependencies
```bash
# Install dependencies
npm install

# Verify installation
npm list --depth=0
```

### Frontend Development Scripts
```bash
# Development server (with hot reload)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Type checking
npm run type-check
```

### Common Frontend Setup Issues

#### Node Version Conflicts
```bash
# If you have version conflicts:
# Install Node Version Manager (NVM)
# Windows: https://github.com/coreybutler/nvm-windows
# Use recommended Node version
nvm install 18.18.0
nvm use 18.18.0
```

#### Package Installation Failures
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

## 🗄️ Database Setup

### Initialize Database
```bash
# Return to project root
cd ../../..

# Initialize the database
python -c "from src.ui.backend.database import init_db; init_db()"

# Verify database creation
ls data/finance_agent.db
```

### Database Tools (Optional)
```bash
# Install SQLite browser for database inspection
# Download from: https://sqlitebrowser.org/

# Or use command line:
sqlite3 data/finance_agent.db
.tables
.quit
```

## 🔧 IDE Configuration

### VS Code Setup

#### Recommended Extensions
```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.black-formatter",
    "ms-python.flake8",
    "ms-vscode.vscode-typescript-next",
    "bradlc.vscode-tailwindcss",
    "ms-vscode.vscode-json"
  ]
}
```

#### Workspace Settings (`.vscode/settings.json`)
```json
{
  "python.defaultInterpreterPath": "./venv/Scripts/python.exe",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length", "88"],
  "typescript.preferences.importModuleSpecifier": "relative",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  }
}
```

#### Launch Configurations (`.vscode/launch.json`)
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI Backend",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "src.ui.backend.main:app",
        "--reload",
        "--host",
        "127.0.0.1",
        "--port",
        "8000"
      ],
      "console": "integratedTerminal"
    },
    {
      "name": "Python: System Tray App",
      "type": "python",
      "request": "launch",
      "module": "src.tray.tray_app",
      "console": "integratedTerminal"
    }
  ]
}
```

### PyCharm Setup

#### Project Configuration
1. **Open Project**: File → Open → Select project directory
2. **Python Interpreter**: Settings → Project → Python Interpreter → Add → Existing environment → Select `venv/Scripts/python.exe`
3. **Code Style**: Settings → Editor → Code Style → Python → Set line length to 88

#### Run Configurations
1. **FastAPI Backend**:
   - Script path: `venv/Scripts/uvicorn.exe`
   - Parameters: `src.ui.backend.main:app --reload --host 127.0.0.1 --port 8000`

2. **System Tray App**:
   - Script path: `src/tray/tray_app.py`

## 🧪 Testing Setup

### Install Test Dependencies
```bash
# Test dependencies are included in requirements.txt
pip install pytest pytest-asyncio pytest-cov httpx
```

### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_document_processor.py

# Run with verbose output
pytest -v
```

### Create Test Directory Structure
```bash
mkdir -p tests/{unit,integration,fixtures}
touch tests/__init__.py
touch tests/conftest.py
```

## 🏃‍♂️ Running the Application

### Development Mode

#### Option 1: Separate Components
```bash
# Terminal 1: Backend API
cd personal-finance-agent
venv\Scripts\activate
uvicorn src.ui.backend.main:app --reload --host 127.0.0.1 --port 8000

# Terminal 2: Frontend (in another terminal)
cd src/ui/frontend
npm run dev

# Terminal 3: System Tray App (in another terminal)
cd personal-finance-agent
venv\Scripts\activate
python -m src.tray.tray_app
```

#### Option 2: Integrated Mode
```bash
# Build frontend first
cd src/ui/frontend
npm run build
cd ../../..

# Run system tray app (includes backend)
python -m src.tray.tray_app
```

### Access Points
- **Main Application**: Right-click system tray icon → Open Finance Agent
- **Direct Browser Access**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Settings**: Right-click tray → Settings

### Environment Variables (Optional)
```bash
# Create .env file in project root
PFA_DEBUG=true
PFA_LOG_LEVEL=DEBUG
PFA_PORT=8000
PFA_DATA_DIR=./data
```

## 🛠️ Development Tools

### Code Quality Tools

#### Black (Code Formatting)
```bash
# Format all Python code
black src/

# Check formatting without making changes
black --check src/
```

#### Flake8 (Linting)
```bash
# Lint Python code
flake8 src/

# With configuration file (.flake8)
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = venv/
```

#### mypy (Type Checking)
```bash
# Type check Python code
mypy src/
```

#### ESLint (Frontend Linting)
```bash
cd src/ui/frontend
npm run lint
npm run lint:fix
```

### Debugging Tools

#### Python Debugging
```python
# Add to code for debugging
import pdb; pdb.set_trace()

# Or use VS Code debugger with breakpoints
```

#### Frontend Debugging
```bash
# Chrome DevTools
# React Developer Tools extension
# VS Code debugger for browser
```

### Database Tools

#### SQLite Commands
```bash
# Open database
sqlite3 data/finance_agent.db

# Common commands
.tables                 # List tables
.schema table_name     # Show table schema
SELECT * FROM settings; # Query data
.quit                  # Exit
```

## 🔄 Git Workflow

### Branch Strategy
```bash
# Main branch for stable releases
git checkout main

# Feature development
git checkout -b feature/document-analysis-improvements
git commit -am "Add improved PDF parsing"
git push origin feature/document-analysis-improvements

# Create PR on GitHub
```

### Commit Messages
Follow conventional commits:
```bash
git commit -m "feat: add support for investment documents"
git commit -m "fix: resolve PDF parsing error for large files"
git commit -m "docs: update API documentation"
git commit -m "test: add unit tests for document processor"
```

## 🚀 Building and Packaging

### Frontend Build
```bash
cd src/ui/frontend
npm run build
cd ../../..
```

### Python Package Build
```bash
# Build wheel
python -m build

# Install locally
pip install -e .
```

### Windows Executable
```bash
# Full build process
python installer/build_installer.py
```

## 📋 Development Checklist

### Initial Setup
- [ ] Python 3.9+ installed
- [ ] Node.js 18+ installed
- [ ] Git configured
- [ ] Repository cloned
- [ ] Virtual environment created and activated
- [ ] Python dependencies installed
- [ ] Frontend dependencies installed
- [ ] Database initialized
- [ ] IDE configured

### Daily Development
- [ ] Virtual environment activated
- [ ] Latest code pulled from main
- [ ] Tests passing
- [ ] Code formatted and linted
- [ ] Documentation updated (if needed)

### Before Committing
- [ ] All tests pass
- [ ] Code formatted with Black
- [ ] No linting errors
- [ ] Type checking passes
- [ ] Documentation updated
- [ ] Commit message follows conventions

## ❓ Troubleshooting

### Common Issues

#### Virtual Environment Issues
```bash
# If venv activation fails:
python -m venv --clear venv
venv\Scripts\activate
pip install -r requirements.txt
```

#### Import Errors
```bash
# If Python can't find modules:
# Add project root to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
# Windows:
set PYTHONPATH=%PYTHONPATH%;%CD%
```

#### Database Errors
```bash
# If database is locked:
rm data/finance_agent.db
python -c "from src.ui.backend.database import init_db; init_db()"
```

#### Port Already in Use
```bash
# Find process using port 8000
netstat -ano | findstr :8000
# Kill process by PID
taskkill /PID <PID> /F
```

### Getting Help

- **Documentation**: Check the docs/ directory
- **Issues**: Search existing GitHub issues
- **Discussions**: Start a GitHub discussion
- **Code Review**: Create a draft PR for feedback

---

**Ready to contribute?** See our [Contributing Guidelines](contributing.md) for development workflow and coding standards.