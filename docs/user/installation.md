# Installation Guide

Complete installation instructions for Personal Finance Agent on Windows.

## 🎯 System Requirements

### Minimum Requirements
- **Operating System**: Windows 10 (version 1909 or later)
- **Architecture**: 64-bit (x64)
- **RAM**: 4 GB
- **Storage**: 500 MB free space
- **Internet**: Required for AI processing

### Recommended Requirements
- **Operating System**: Windows 11
- **RAM**: 8 GB or more
- **Storage**: 2 GB free space (for documents and data)
- **Internet**: Broadband connection for faster AI responses

## 🚀 Installation Methods

### Method 1: Windows Installer (Recommended)

This is the easiest way to install Personal Finance Agent.

#### Step 1: Download the Installer
1. Visit the [Releases page](https://github.com/yourusername/personal-finance-agent/releases)
2. Download the latest `PersonalFinanceAgent-Setup-1.0.0.exe`
3. **Verify the download** (optional but recommended):
   - Check the file size matches the release notes
   - Verify SHA256 hash if provided

#### Step 2: Run the Installer
1. **Right-click** the downloaded file and select **Run as administrator**
2. If Windows Defender shows a warning:
   - Click **More info**
   - Click **Run anyway**
   - This happens because the app isn't yet signed with a code signing certificate

#### Step 3: Installation Wizard
1. **Welcome Screen**: Click **Next**
2. **License Agreement**: Read and accept the MIT license
3. **Installation Directory**: 
   - Default: `C:\Program Files\Personal Finance Agent`
   - Click **Browse** to change location
4. **Additional Tasks**:
   - ✅ Create desktop shortcut (recommended)
   - ✅ Add to Start Menu
   - ⬜ Start automatically with Windows (optional)
5. **Install**: Click **Install** and wait for completion
6. **Finish**: Click **Launch Personal Finance Agent**

#### Step 4: First Launch
The application will:
1. Create data directories in `%APPDATA%\Personal Finance Agent`
2. Start the system tray service
3. Open your default browser to the settings page

### Method 2: Development Installation

For developers or advanced users who want to run from source.

#### Prerequisites
- **Python 3.9+**: Download from [python.org](https://www.python.org/downloads/)
- **Node.js 18+**: Download from [nodejs.org](https://nodejs.org/)
- **Git**: Download from [git-scm.com](https://git-scm.com/)

#### Installation Steps
```bash
# 1. Clone the repository
git clone https://github.com/yourusername/personal-finance-agent.git
cd personal-finance-agent

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Build frontend
cd src\ui\frontend
npm install
npm run build
cd ..\..\..

# 5. Initialize database
python -c "from src.ui.backend.database import init_db; init_db()"

# 6. Run the application
python -m src.tray.tray_app
```

## 🔧 Post-Installation Setup

### 1. Verify Installation
After installation, you should see:
- 💚 Green dollar sign icon in the system tray
- 📁 Data directory at `%APPDATA%\Personal Finance Agent`
- 🚀 Application accessible via tray menu

### 2. Configure Firewall (if needed)
Windows may ask for firewall permissions:
- **Allow** the application to communicate through Windows Defender Firewall
- This is needed for the web interface to work properly

### 3. Set Up API Key
See the [Quick Start Guide](quick-start.md#step-2-get-your-ai-api-key) for detailed instructions.

## 📁 File Locations

### Installed Files
```
C:\Program Files\Personal Finance Agent\
├── PersonalFinanceAgent.exe     # Main executable
├── _internal\                   # Application files
└── unins000.exe                # Uninstaller
```

### User Data
```
%APPDATA%\Personal Finance Agent\
├── data\
│   ├── finance_agent.db        # SQLite database
│   ├── uploads\                # Uploaded documents
│   └── chromadb\              # Vector database
└── config\
    └── settings.json          # User settings
```

## 🔄 Updating the Application

### Automatic Updates (Planned)
Future versions will include automatic update checking.

### Manual Updates
1. Download the new installer
2. Run it - it will update the existing installation
3. Your data and settings will be preserved

### Development Updates
```bash
cd personal-finance-agent
git pull origin main
pip install -r requirements.txt
cd src\ui\frontend && npm install && npm run build
```

## 🗑️ Uninstallation

### Via Control Panel
1. Open **Settings** > **Apps**
2. Search for "Personal Finance Agent"
3. Click **Uninstall**
4. Follow the uninstaller prompts

### Manual Cleanup (if needed)
After uninstallation, you may want to remove user data:
```
%APPDATA%\Personal Finance Agent\  # User data and settings
```

## 🛠️ Troubleshooting Installation

### Common Issues

#### "Windows protected your PC" Warning
**Cause**: Unsigned executable  
**Solution**: 
1. Click **More info**
2. Click **Run anyway**
3. This is safe - the warning appears because we don't have a code signing certificate yet

#### Installation Fails with Permission Error
**Cause**: Insufficient permissions  
**Solution**: 
1. Right-click installer
2. Select **Run as administrator**

#### Application Won't Start
**Causes & Solutions**:
1. **Antivirus blocking**: Add exception for the installation directory
2. **Missing dependencies**: Install Microsoft Visual C++ Redistributable
3. **Port conflict**: Another application using port 8000

#### "Python not found" Error (Development)
**Solution**: 
1. Download Python from [python.org](https://www.python.org/downloads/)
2. During installation, check **Add Python to PATH**
3. Restart command prompt

#### Node.js/npm Errors (Development)
**Solution**:
1. Download Node.js from [nodejs.org](https://nodejs.org/)
2. Use LTS version (18.x or 20.x)
3. Restart command prompt after installation

### Getting Help

If you encounter issues not covered here:

1. **Check logs**: Look in `%APPDATA%\Personal Finance Agent\logs\`
2. **Search issues**: [GitHub Issues](https://github.com/yourusername/personal-finance-agent/issues)
3. **Create new issue**: Include:
   - Windows version
   - Installation method used
   - Error messages
   - Log files (if available)

## 🔒 Security Considerations

### Windows Defender
- The application may be flagged as unknown software
- This is normal for new applications without code signing certificates
- You can safely add an exception

### Network Access
- The application only communicates with:
  - OpenAI/Anthropic APIs for document analysis
  - Localhost for the web interface
- No other network access is required

### Data Storage
- All financial data is stored locally
- No cloud storage or external databases
- API keys are encrypted using Windows DPAPI

---

**Need help?** See our [Troubleshooting Guide](../troubleshooting/common-issues.md) or [create an issue](https://github.com/yourusername/personal-finance-agent/issues).