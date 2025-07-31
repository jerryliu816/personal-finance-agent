# Configuration Guide

Detailed guide to configuring Personal Finance Agent for optimal performance.

## 🎯 Overview

Personal Finance Agent can be configured through:
- **Web Interface**: Settings page (recommended for most users)
- **Configuration Files**: Advanced users and developers
- **Environment Variables**: System administrators and automated deployments

## 🌐 Web Interface Configuration

### Accessing Settings
1. Right-click the system tray icon
2. Select **Settings**
3. Or navigate to `http://localhost:8000/settings` in your browser

### AI Language Model Settings

#### Provider Selection
```
LLM Provider: [OpenAI ▼]
Options: OpenAI, Anthropic
```

**OpenAI Configuration**:
- **Model Used**: GPT-4
- **Best For**: General users, fast responses, cost-effective
- **API Key Format**: `sk-...` (starts with sk-)
- **Pricing**: Pay-per-use, typically $0.01-0.05 per document

**Anthropic Configuration**:
- **Model Used**: Claude-3-Sonnet
- **Best For**: Complex analysis, detailed responses
- **API Key Format**: `sk-ant-...` (starts with sk-ant-)
- **Pricing**: Pay-per-use, typically $0.02-0.08 per document

#### API Key Configuration
```
API Key: [●●●●●●●●●●●●●●●●●●●●] 
Helper Text: Your API key for the selected LLM provider
```

**Security Features**:
- Keys are masked in the interface
- Encrypted storage using Windows DPAPI
- Never logged or transmitted except to API provider

### Email Integration Settings

#### Gmail IMAP Configuration
```
Gmail Server: [imap.gmail.com]
Username: [your-email@gmail.com]
Password: [●●●●●●●●●●●●] (App Password)
```

**Setup Requirements**:
1. **2-Factor Authentication**: Must be enabled on Gmail account
2. **App Password**: Generate specific password for this application
3. **IMAP Access**: Must be enabled in Gmail settings

#### Automatic Processing Settings
```
☐ Automatically check email for financial documents
Check Interval: [60] minutes
```

**Options**:
- **Interval Range**: 1-1440 minutes (1 minute to 24 hours)
- **Recommended**: 60-240 minutes for most users
- **Impact**: More frequent checks use more system resources

### Advanced Settings

#### Processing Options
```
Document Processing:
☑ Enable automatic categorization
☑ Extract investment data
☑ Process tax documents
☐ Enable experimental features
```

#### Storage Settings
```
Data Location: C:\Users\[User]\AppData\Roaming\Personal Finance Agent
Database: SQLite (local storage only)
Backup Frequency: [Daily ▼]
```

## 📁 Configuration Files

### Settings File Location
```
%APPDATA%\Personal Finance Agent\config\settings.json
```

### File Structure
```json
{
  "llm_provider": "openai",
  "llm_api_key": "encrypted_key_data",
  "gmail_server": "imap.gmail.com",
  "gmail_username": "user@gmail.com",
  "gmail_password": "encrypted_password_data",
  "auto_check_email": false,
  "check_interval": 60,
  "processing_options": {
    "auto_categorize": true,
    "extract_investments": true,
    "process_tax_docs": true,
    "experimental_features": false
  },
  "ui_preferences": {
    "theme": "light",
    "currency": "USD",
    "date_format": "MM/DD/YYYY"
  }
}
```

### Manual Configuration

⚠️ **Warning**: Manual file editing is for advanced users only. Always backup settings before editing.

#### Editing Settings
1. **Stop the application** first
2. **Backup** the settings file
3. **Edit** with a text editor
4. **Validate** JSON syntax
5. **Restart** the application

#### Common Manual Configurations

**Change Data Directory**:
```json
{
  "data_directory": "D:\\MyFinances\\PersonalFinanceAgent"
}
```

**Custom Processing Settings**:
```json
{
  "processing_options": {
    "auto_categorize": true,
    "confidence_threshold": 0.8,
    "max_document_size": 52428800,
    "supported_formats": ["pdf"]
  }
}
```

## 🔧 Environment Variables

For system administrators, advanced users, or containerized deployments.

### Available Variables

#### Core Settings
```bash
PFA_DATA_DIR=C:\ProgramData\PersonalFinanceAgent
PFA_CONFIG_DIR=C:\ProgramData\PersonalFinanceAgent\config
PFA_LOG_LEVEL=INFO
PFA_PORT=8000
```

#### API Configuration
```bash
PFA_LLM_PROVIDER=openai
PFA_OPENAI_API_KEY=sk-your-key-here
PFA_ANTHROPIC_API_KEY=sk-ant-your-key-here
```

#### Email Settings
```bash
PFA_GMAIL_SERVER=imap.gmail.com
PFA_GMAIL_USERNAME=your-email@gmail.com
PFA_GMAIL_PASSWORD=your-app-password
PFA_AUTO_CHECK_EMAIL=false
PFA_CHECK_INTERVAL=60
```

### Setting Environment Variables

#### Windows Command Prompt
```cmd
set PFA_LLM_PROVIDER=openai
set PFA_OPENAI_API_KEY=sk-your-key-here
PersonalFinanceAgent.exe
```

#### Windows PowerShell
```powershell
$env:PFA_LLM_PROVIDER="openai"
$env:PFA_OPENAI_API_KEY="sk-your-key-here"
.\PersonalFinanceAgent.exe
```

#### System Environment Variables
1. **Open**: Control Panel → System → Advanced System Settings
2. **Click**: Environment Variables
3. **Add**: New system or user variables
4. **Restart**: Application to pick up changes

## 🗃️ Database Configuration

### SQLite Settings

#### Default Configuration
```
Database File: %APPDATA%\Personal Finance Agent\data\finance_agent.db
Engine: SQLite 3.x
Connection Pool: 5 connections
Timeout: 30 seconds
```

#### Advanced Database Settings
```json
{
  "database": {
    "url": "sqlite:///data/finance_agent.db",
    "pool_size": 5,
    "max_overflow": 10,
    "pool_timeout": 30,
    "pool_recycle": 3600,
    "echo": false
  }
}
```

### Backup Configuration
```json
{
  "backup": {
    "enabled": true,
    "frequency": "daily",
    "retention_days": 30,
    "location": "data/backups",
    "compress": true
  }
}
```

## 🎨 UI Customization

### Theme Settings
```json
{
  "ui_preferences": {
    "theme": "light",
    "primary_color": "#2e7d32",
    "secondary_color": "#1976d2",
    "font_family": "Roboto",
    "font_size": "14px"
  }
}
```

### Display Options
```json
{
  "display": {
    "currency": "USD",
    "currency_symbol": "$",
    "date_format": "MM/DD/YYYY",
    "time_format": "12h",
    "number_format": "en-US",
    "chart_animations": true,
    "table_page_size": 25
  }
}
```

## 🔐 Security Configuration

### API Key Encryption

#### Encryption Method
- **Windows**: DPAPI (Data Protection API)
- **Scope**: Current user only
- **Strength**: AES-256 equivalent

#### Key Storage
```
Encrypted Keys: %APPDATA%\Personal Finance Agent\config\.keys
Format: Base64 encoded encrypted data
Access: Current Windows user only
```

### Network Security
```json
{
  "network": {
    "allowed_origins": ["http://localhost:3000", "http://127.0.0.1:8000"],
    "ssl_enabled": false,
    "ssl_cert_path": "",
    "ssl_key_path": "",
    "cors_enabled": true,
    "trusted_proxies": []
  }
}
```

## 📊 Performance Configuration

### Processing Settings
```json
{
  "performance": {
    "max_concurrent_documents": 3,
    "document_processing_timeout": 300,
    "chunk_size": 1000,
    "overlap_size": 100,
    "max_document_size": 52428800,
    "cache_size": 100
  }
}
```

### Memory Management
```json
{
  "memory": {
    "max_memory_usage": "1GB",
    "cleanup_interval": 3600,
    "cache_ttl": 7200,
    "gc_threshold": 0.8
  }
}
```

## 🔧 Troubleshooting Configuration Issues

### Common Problems

#### Settings Not Saving
**Symptoms**: Changes don't persist after restart  
**Solutions**:
1. Check file permissions on config directory
2. Ensure application isn't running as different user
3. Verify disk space availability

#### API Keys Not Working
**Symptoms**: Authentication errors with AI providers  
**Solutions**:
1. Verify key format (OpenAI: sk-..., Anthropic: sk-ant-...)
2. Check key permissions on provider platform
3. Re-enter key in settings interface

#### Email Integration Failing
**Symptoms**: No automatic document processing  
**Solutions**:
1. Verify Gmail app password (not regular password)
2. Check IMAP is enabled in Gmail settings
3. Test credentials manually

### Configuration Validation

#### Settings Validation Tool
Run from command line:
```bash
PersonalFinanceAgent.exe --validate-config
```

#### Manual Validation
Check configuration file syntax:
```bash
python -m json.tool config/settings.json
```

### Reset Configuration

#### Reset to Defaults
1. **Stop application**
2. **Backup** current settings (optional)
3. **Delete** `%APPDATA%\Personal Finance Agent\config\settings.json`
4. **Restart** application
5. **Reconfigure** through settings interface

#### Selective Reset
```json
{
  "reset_sections": ["llm_config", "email_config", "ui_preferences"]
}
```

---

**Need help with configuration?** See our [Troubleshooting Guide](../troubleshooting/common-issues.md) or [create an issue](https://github.com/yourusername/personal-finance-agent/issues).