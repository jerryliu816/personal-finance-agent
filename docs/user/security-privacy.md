# Security & Privacy Guide

Understanding how Personal Finance Agent protects your financial data and privacy.

## 🔒 Security Overview

Personal Finance Agent is designed with **privacy-first principles**:
- **Local Storage**: All financial data stays on your device
- **Encrypted Credentials**: API keys and passwords are encrypted
- **Minimal Data Sharing**: Only document text is sent for AI analysis
- **No Cloud Storage**: No external databases or cloud storage used
- **Open Source**: Code is available for security review

## 🏠 Local Data Storage

### What Stays Local
- **Financial Documents**: Original PDFs stored on your computer
- **Extracted Data**: All transactions, accounts, and analysis results
- **Chat History**: All conversations with the AI assistant
- **Settings**: All configuration and preferences
- **Database**: Complete SQLite database on your local drive

### Storage Locations
```
%APPDATA%\Personal Finance Agent\
├── data\
│   ├── finance_agent.db          # Main database (encrypted)
│   ├── uploads\                  # Original PDF documents
│   └── chromadb\                 # Vector database for RAG
├── config\
│   ├── settings.json             # User settings
│   └── .keys                     # Encrypted API keys
└── logs\                         # Application logs
```

### Access Control
- **File Permissions**: Restricted to current Windows user
- **No Network Access**: Local files not accessible remotely
- **User Data Protection**: Follows Windows user account security

## 🔐 Encryption & Key Management

### API Key Security

#### Encryption Method
- **Technology**: Windows DPAPI (Data Protection API)
- **Strength**: AES-256 equivalent encryption
- **Scope**: Encrypted for current user and machine only
- **Access**: Cannot be decrypted by other users or on other machines

#### Key Storage Process
1. **Entry**: API key entered in settings interface
2. **Encryption**: Immediately encrypted using DPAPI
3. **Storage**: Stored as encrypted blob in `.keys` file
4. **Usage**: Decrypted in memory only when needed for API calls
5. **Transmission**: Only sent to configured AI provider

#### Key Security Features
- **No Plaintext Storage**: Keys never stored in readable format
- **Memory Protection**: Cleared from memory after use
- **No Logging**: API keys never appear in log files
- **Automatic Rotation**: Easy to change keys without data loss

### Database Encryption

#### SQLite Security
- **File Encryption**: Database file encrypted at rest
- **Connection Security**: Encrypted connections to database
- **Backup Protection**: Backup files also encrypted
- **Access Control**: Database only accessible by application

## 🌐 Network Security

### AI Provider Communication

#### What Gets Sent
- **Document Text**: Only the extracted text content from PDFs
- **Chat Messages**: Your questions and conversation context
- **No Metadata**: No filenames, personal info, or system details

#### What Doesn't Get Sent
- **Original PDFs**: Files never leave your computer
- **Personal Information**: Names, addresses, SSNs filtered out
- **File Metadata**: Creation dates, paths, system info
- **Complete Database**: Only relevant context shared

#### Network Protocols
- **HTTPS Only**: All API communication encrypted in transit
- **Certificate Validation**: Proper SSL certificate checking
- **No Data Persistence**: AI providers don't store your data long-term

### Local Network Security

#### Web Interface Security
- **Localhost Only**: Web interface only accessible from your computer
- **Port Binding**: Bound to 127.0.0.1 (local only)
- **No Remote Access**: Cannot be accessed from other devices
- **Session Management**: Secure session handling

#### Firewall Configuration
- **Outbound Only**: Only outbound connections to AI providers
- **No Inbound**: No incoming network connections accepted
- **Port Usage**: Only uses standard HTTPS port (443) for API calls

## 🤖 AI Provider Privacy

### OpenAI Privacy

#### Data Usage Policy
- **Analysis Only**: Data used only for processing your request
- **No Training**: Your data not used to train AI models
- **30-Day Retention**: Data deleted after 30 days (per OpenAI policy)
- **No Sharing**: Data not shared with third parties

#### What OpenAI Receives
- **Document Text**: Extracted text for financial analysis
- **Chat Context**: Previous conversation for continuity
- **Analysis Requests**: Instructions for data processing

#### What OpenAI Doesn't Receive
- **Original Files**: PDF files remain on your computer
- **Personal Identifiers**: Names, SSNs, account numbers filtered
- **System Information**: No device or system details shared

### Anthropic Privacy

#### Data Usage Policy
- **Processing Only**: Data used solely for generating responses
- **No Model Training**: Personal data not used for AI training
- **Limited Retention**: Data not stored long-term
- **Privacy Focus**: Strong commitment to user privacy

#### Privacy Controls
- **Data Minimization**: Only necessary data sent
- **Automatic Filtering**: Sensitive information filtered out
- **Secure Processing**: End-to-end encryption for all communications

## 🛡️ Data Protection Features

### Automatic Data Filtering

#### Sensitive Information Removal
Before sending to AI providers, the application automatically removes:
- **Social Security Numbers**: Patterns like XXX-XX-XXXX
- **Account Numbers**: Long numeric sequences
- **Phone Numbers**: Phone number patterns
- **Email Addresses**: Personal email addresses
- **Home Addresses**: Street addresses and ZIP codes

#### Smart Redaction
```
Original: "John Smith, SSN: 123-45-6789, Account: 1234567890"
Filtered: "[NAME], SSN: [REDACTED], Account: [REDACTED]"
```

### Backup Security

#### Automatic Backups
- **Encrypted Backups**: All backups encrypted with same security
- **Local Storage**: Backups stored locally, never uploaded
- **Retention Policy**: Old backups automatically cleaned up
- **Integrity Checks**: Backup integrity verified

#### Manual Export Security
- **Encrypted Exports**: Data exports encrypted by default
- **Password Protection**: Option to password-protect exports
- **Secure Deletion**: Original data securely deleted after export

## 🚨 Security Best Practices

### For Users

#### API Key Management
- **Keep Keys Secure**: Don't share API keys with others
- **Monitor Usage**: Regularly check API usage on provider platforms
- **Rotate Keys**: Change keys periodically for security
- **Revoke Compromised Keys**: Immediately revoke if compromised

#### Document Security
- **Verify Sources**: Only upload legitimate financial documents
- **Check Content**: Review documents before uploading
- **Secure Network**: Use secure networks when uploading
- **Regular Review**: Periodically review uploaded documents

#### System Security
- **Keep Updated**: Install Windows updates regularly
- **Antivirus**: Use reputable antivirus software
- **Strong Passwords**: Use strong Windows account passwords
- **User Account Control**: Keep UAC enabled

### For Administrators

#### System Hardening
- **File Permissions**: Ensure proper file permissions
- **Network Security**: Configure firewall rules appropriately
- **Access Control**: Limit user access to application directories
- **Monitoring**: Monitor for unusual file access patterns

#### Enterprise Deployment
- **Group Policy**: Use Group Policy for configuration management
- **Centralized Logging**: Collect logs for security monitoring
- **Network Isolation**: Consider network segmentation
- **Compliance**: Ensure compliance with organizational policies

## 📊 Privacy Impact Assessment

### Data Collection
- **Financial Documents**: Necessary for core functionality
- **Chat History**: Enables conversation continuity
- **Usage Analytics**: None collected
- **Crash Reports**: Optional, user-controlled

### Data Processing
- **Purpose**: Financial analysis and insights only
- **Retention**: Indefinite local storage, user controls deletion
- **Sharing**: Only with configured AI providers for processing
- **Third Parties**: No sharing except AI providers

### User Rights
- **Access**: Full access to all your data
- **Modification**: Can edit or delete any data
- **Portability**: Can export data in standard formats
- **Deletion**: Can delete all data at any time

## 🔍 Security Auditing

### Self-Assessment Tools

#### Configuration Review
```bash
PersonalFinanceAgent.exe --security-check
```

#### Data Audit
- Review uploaded documents list
- Check API key configuration
- Verify encryption status
- Audit chat history

### Security Monitoring

#### Log Analysis
Application logs can help identify:
- Unusual access patterns
- Failed authentication attempts
- Network connection issues
- File permission problems

#### Regular Reviews
- **Monthly**: Review uploaded documents and chat history
- **Quarterly**: Update API keys and review settings
- **Annually**: Full security configuration review

## 🚨 Incident Response

### If You Suspect a Security Issue

#### Immediate Steps
1. **Stop the Application**: Close Personal Finance Agent
2. **Disconnect Network**: Disconnect from internet temporarily
3. **Change API Keys**: Rotate all API keys immediately
4. **Review Logs**: Check application logs for suspicious activity

#### Reporting Security Issues
- **GitHub Issues**: Create private security issue
- **Email**: Contact maintainers directly
- **Include**: Detailed description, logs, system information

### Data Breach Response

#### If Data is Compromised
1. **Assess Impact**: Determine what data was affected
2. **Contain Breach**: Stop further unauthorized access
3. **Notify Providers**: Alert AI providers if keys compromised
4. **Change Credentials**: Update all API keys and passwords
5. **Monitor Accounts**: Watch financial accounts for unusual activity

## ✅ Security Checklist

### Initial Setup
- [ ] Configure strong API keys
- [ ] Verify encryption is working
- [ ] Test data filtering
- [ ] Review privacy settings
- [ ] Set up automatic backups

### Regular Maintenance
- [ ] Update application regularly
- [ ] Rotate API keys quarterly
- [ ] Review uploaded documents monthly
- [ ] Check log files for issues
- [ ] Verify backup integrity

### Security Monitoring
- [ ] Monitor API usage on provider platforms
- [ ] Review chat history for sensitive data
- [ ] Check file permissions periodically
- [ ] Audit network connections
- [ ] Test data export/import functions

---

**Security Concerns?** Report security issues to [security@yourproject.com](mailto:security@yourproject.com) or create a private issue on GitHub.