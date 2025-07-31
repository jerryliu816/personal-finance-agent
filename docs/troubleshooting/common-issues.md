# Common Issues & Troubleshooting

Comprehensive guide to diagnosing and resolving common problems with Personal Finance Agent.

## 🚨 Quick Troubleshooting Checklist

Before diving into specific issues, try these quick fixes:

- [ ] **Restart the application** - Close system tray app and restart
- [ ] **Check API key** - Verify your LLM provider API key is valid
- [ ] **Update Windows** - Ensure Windows is up to date
- [ ] **Check internet connection** - Required for AI processing
- [ ] **Free disk space** - Ensure adequate storage space
- [ ] **Antivirus check** - Verify app isn't being blocked

## 🔧 Installation Issues

### Application Won't Install

#### Windows SmartScreen Warning
**Symptoms**: "Windows protected your PC" message appears  
**Cause**: Unsigned executable triggering SmartScreen  

**Solution**:
1. Click **More info**
2. Click **Run anyway**
3. This is safe - warning appears because app lacks code signing certificate

#### Installer Fails with Permission Error
**Symptoms**: "Access denied" or permission errors during installation  
**Cause**: Insufficient user permissions  

**Solution**:
1. Right-click installer
2. Select **Run as administrator**
3. Complete installation with elevated privileges

#### Antivirus Software Blocking Installation
**Symptoms**: Installation fails silently or files are deleted  
**Cause**: Antivirus false positive  

**Solution**:
1. Temporarily disable real-time protection
2. Add installation directory to antivirus exclusions
3. Install the application
4. Re-enable antivirus protection

**Common Antivirus Issues**:
- **Windows Defender**: Add `%ProgramFiles%\Personal Finance Agent` to exclusions
- **Norton/McAfee**: Whitelist `PersonalFinanceAgent.exe`
- **Kaspersky**: Add to trusted applications

### Installation Directory Issues

#### Program Files Access Denied
**Symptoms**: Cannot write to Program Files directory  
**Cause**: User account restrictions  

**Solution**:
1. Install to user directory instead: `%LOCALAPPDATA%\Personal Finance Agent`
2. Or run installer as administrator

#### Corrupted Installation
**Symptoms**: Missing files or incomplete installation  
**Cause**: Interrupted installation process  

**Solution**:
1. Uninstall completely
2. Delete remaining files in installation directory
3. Clear temporary files: `%TEMP%`
4. Reinstall fresh

## 🚀 Application Startup Issues

### System Tray Icon Not Appearing

#### Service Not Starting
**Symptoms**: No system tray icon visible  
**Cause**: Backend server failed to start  

**Diagnosis**:
```bash
# Check if process is running
tasklist | findstr PersonalFinanceAgent

# Check port usage
netstat -ano | findstr :8000
```

**Solutions**:
1. **Port Conflict**: Another application using port 8000
   ```bash
   # Find process using port 8000
   netstat -ano | findstr :8000
   # Kill conflicting process
   taskkill /PID <PID> /F
   ```

2. **Missing Dependencies**: 
   - Install Microsoft Visual C++ Redistributable
   - Update .NET Framework if required

3. **Firewall Blocking**:
   - Allow `PersonalFinanceAgent.exe` through Windows Firewall
   - Check corporate firewall settings

#### System Tray Area Hidden
**Symptoms**: Application running but icon not visible  
**Cause**: Windows hiding system tray icons  

**Solution**:
1. Click up arrow (^) in system tray
2. Right-click empty space → **Taskbar settings**
3. Select **Turn system icons on or off**
4. Find Personal Finance Agent and set to **On**

### Web Interface Not Loading

#### Browser Connection Refused
**Symptoms**: "This site can't be reached" error  
**Cause**: Backend server not running or port blocked  

**Diagnosis**:
```bash
# Test local connection
curl http://localhost:8000/health

# Check server logs
type "%APPDATA%\Personal Finance Agent\logs\application.log"
```

**Solutions**:
1. **Server Not Started**: Restart application
2. **Wrong Port**: Check if server started on different port
3. **Firewall**: Allow localhost connections
4. **Browser Cache**: Clear browser cache and cookies

#### Page Loads But Features Don't Work
**Symptoms**: Interface loads but buttons/forms don't respond  
**Cause**: JavaScript errors or API connection issues  

**Diagnosis**:
1. Open browser Developer Tools (F12)
2. Check Console tab for errors
3. Check Network tab for failed requests

**Solutions**:
1. **JavaScript Disabled**: Enable JavaScript in browser
2. **CORS Issues**: Restart application to reset CORS settings
3. **Browser Compatibility**: Use Chrome, Firefox, or Edge

## 🔑 API Configuration Issues

### OpenAI API Problems

#### Invalid API Key
**Symptoms**: "Authentication failed" errors  
**Cause**: Incorrect or expired API key  

**Solutions**:
1. **Verify Key Format**: Must start with `sk-`
2. **Check OpenAI Dashboard**: Verify key exists and has credits
3. **Regenerate Key**: Create new API key if needed
4. **Clear Cache**: Delete and re-enter key in settings

#### Rate Limit Exceeded
**Symptoms**: "Rate limit exceeded" errors  
**Cause**: Too many API requests  

**Solutions**:
1. **Wait**: Rate limits reset automatically
2. **Upgrade Plan**: Increase rate limits on OpenAI dashboard
3. **Reduce Usage**: Process documents one at a time

#### Insufficient Credits
**Symptoms**: "Insufficient quota" errors  
**Cause**: No remaining API credits  

**Solutions**:
1. **Add Credits**: Top up OpenAI account
2. **Check Usage**: Review usage on OpenAI dashboard
3. **Monitor Spending**: Set up usage alerts

### Anthropic API Problems

#### Authentication Issues
**Symptoms**: API key errors with Anthropic  
**Cause**: Invalid API key format or permissions  

**Solutions**:
1. **Key Format**: Must start with `sk-ant-`
2. **Beta Access**: Ensure you have Claude API access
3. **Organization**: Check if key belongs to correct organization

#### Model Access Issues
**Symptoms**: "Model not available" errors  
**Cause**: Model access restrictions  

**Solutions**:
1. **Request Access**: Apply for Claude-3 access
2. **Check Status**: Verify access in Anthropic Console
3. **Switch Models**: Try different model if available

## 📄 Document Processing Issues

### PDF Upload Failures

#### File Format Not Supported
**Symptoms**: "Only PDF files are supported" error  
**Cause**: Uploading non-PDF files  

**Solutions**:
1. **Convert to PDF**: Use online converters or print to PDF
2. **Check Extension**: Ensure file has `.pdf` extension
3. **File Corruption**: Try re-downloading or re-creating PDF

#### Password-Protected PDFs
**Symptoms**: "Cannot extract text" errors  
**Cause**: PDF requires password to open  

**Solutions**:
1. **Remove Password**: Use PDF editor to remove password
2. **Save as New PDF**: Print to PDF to create unprotected copy
3. **Use Alternative**: Scan or screenshot if content is public

#### Large File Issues
**Symptoms**: Upload times out or fails  
**Cause**: File size exceeds limits  

**Solutions**:
1. **Split Document**: Divide into smaller sections
2. **Compress PDF**: Use PDF compression tools
3. **Optimize Images**: Reduce image quality in PDF

### Text Extraction Problems

#### Poor OCR Results
**Symptoms**: Garbled or missing text in analysis  
**Cause**: Low-quality scanned documents  

**Solutions**:
1. **Higher Quality Scan**: Rescan at higher DPI (300+ recommended)
2. **Clean Image**: Remove noise, adjust contrast
3. **Re-type Content**: For critical documents, manually re-create

#### Missing Tables or Formatting
**Symptoms**: Table data not extracted properly  
**Cause**: Complex document layout  

**Solutions**:
1. **Manual Review**: Check analysis results and add missing data
2. **Split Tables**: Extract tables as separate images
3. **Alternative Format**: Convert to simpler layout if possible

### AI Analysis Issues

#### Poor Categorization
**Symptoms**: Transactions categorized incorrectly  
**Cause**: Ambiguous transaction descriptions  

**Solutions**:
1. **Review Results**: Check analysis for accuracy
2. **Provide Context**: Add document type hint during upload
3. **Manual Correction**: Edit categories in database if needed

#### Incomplete Extraction
**Symptoms**: Missing transactions or data  
**Cause**: Complex document format or poor text extraction  

**Solutions**:
1. **Try Different Provider**: Switch between OpenAI and Anthropic
2. **Improve PDF Quality**: Ensure text is clearly readable
3. **Manual Entry**: Add missing transactions manually

## 💬 Chat Interface Issues

### Chat Not Responding

#### No Response from AI
**Symptoms**: Messages sent but no reply received  
**Cause**: API configuration or connectivity issues  

**Diagnosis**:
1. Check API key is configured
2. Verify internet connection
3. Check API provider status pages

**Solutions**:
1. **Reconfigure API**: Re-enter API key in settings
2. **Switch Provider**: Try different LLM provider
3. **Check Credits**: Ensure API account has sufficient credits

#### Slow Response Times
**Symptoms**: Long delays before chat responses  
**Cause**: API latency or complex queries  

**Solutions**:
1. **Simplify Questions**: Ask more direct questions
2. **Check Connection**: Ensure stable internet connection
3. **Provider Status**: Check if API provider has service issues

### Context Issues

#### Responses Lack Financial Context
**Symptoms**: Generic responses without personal financial data  
**Cause**: No processed documents or context retrieval failure  

**Solutions**:
1. **Upload Documents**: Ensure financial documents are uploaded and processed
2. **Wait for Processing**: Allow time for document analysis to complete
3. **Check Profile**: Verify financial profile contains data

#### Outdated Information
**Symptoms**: Chat references old financial data  
**Cause**: Database not updated with recent documents  

**Solutions**:
1. **Refresh Data**: Upload recent financial documents
2. **Restart Application**: Refresh in-memory caches
3. **Manual Update**: Check if recent uploads were processed

## ⚙️ Settings and Configuration Issues

### Settings Not Saving

#### Configuration File Permissions
**Symptoms**: Changes don't persist after restart  
**Cause**: No write permissions to config directory  

**Solutions**:
1. **Check Permissions**: Ensure user can write to `%APPDATA%\Personal Finance Agent`
2. **Run as Administrator**: Temporary solution for permission issues
3. **Move Config**: Use different config directory with write access

#### Corrupted Settings File
**Symptoms**: Application crashes on startup or settings reset  
**Cause**: Invalid JSON in settings file  

**Solutions**:
1. **Reset Settings**: Delete `%APPDATA%\Personal Finance Agent\config\settings.json`
2. **Backup Restore**: Restore from backup if available
3. **Manual Edit**: Fix JSON syntax errors in text editor

### Email Integration Issues

#### Gmail Connection Failed
**Symptoms**: "Authentication failed" for Gmail  
**Cause**: Incorrect credentials or security settings  

**Solutions**:
1. **App Password**: Use Gmail app password, not regular password
2. **2FA Required**: Enable 2-factor authentication on Gmail
3. **IMAP Enabled**: Ensure IMAP is enabled in Gmail settings
4. **Correct Server**: Use `imap.gmail.com` as server

#### No Emails Being Processed
**Symptoms**: Automatic email checking not working  
**Cause**: Email integration not configured properly  

**Solutions**:
1. **Enable Feature**: Check "Auto check email" in settings
2. **Check Interval**: Ensure check interval is reasonable (15+ minutes)
3. **Test Connection**: Manually verify email credentials work
4. **Check Filters**: Ensure emails aren't being filtered out

## 🗄️ Database Issues

### Database Corruption

#### SQLite Database Locked
**Symptoms**: "Database is locked" errors  
**Cause**: Multiple processes accessing database or crash during write  

**Solutions**:
1. **Close Application**: Ensure no other instances running
2. **Restart Computer**: Clear any locked file handles
3. **Database Recovery**: Use SQLite tools to repair database
4. **Restore Backup**: Use automatic backup if available

#### Data Inconsistency
**Symptoms**: Missing or incorrect financial data  
**Cause**: Database corruption or failed transactions  

**Solutions**:
1. **Integrity Check**: Run SQLite integrity check
   ```bash
   sqlite3 data/finance_agent.db "PRAGMA integrity_check;"
   ```
2. **Vacuum Database**: Clean up database file
   ```bash
   sqlite3 data/finance_agent.db "VACUUM;"
   ```
3. **Restore Backup**: Use recent backup if corruption is severe

### Performance Issues

#### Slow Database Queries
**Symptoms**: Application feels sluggish, long loading times  
**Cause**: Large database or missing indexes  

**Solutions**:
1. **Reindex Database**: Rebuild database indexes
   ```bash
   sqlite3 data/finance_agent.db "REINDEX;"
   ```
2. **Analyze Statistics**: Update query planner statistics
   ```bash
   sqlite3 data/finance_agent.db "ANALYZE;"
   ```
3. **Archive Old Data**: Move old transactions to separate database

## 🌐 Network and Connectivity Issues

### Firewall and Antivirus

#### Windows Firewall Blocking
**Symptoms**: Cannot access web interface or API calls fail  
**Cause**: Windows Firewall blocking application  

**Solutions**:
1. **Allow Through Firewall**:
   - Windows Settings → Update & Security → Windows Security
   - Firewall & network protection → Allow an app through firewall
   - Add `PersonalFinanceAgent.exe`

2. **Create Firewall Rule**:
   ```bash
   netsh advfirewall firewall add rule name="Personal Finance Agent" dir=in action=allow program="C:\Program Files\Personal Finance Agent\PersonalFinanceAgent.exe"
   ```

#### Corporate Network Restrictions
**Symptoms**: API calls fail in corporate environment  
**Cause**: Network policies blocking external API access  

**Solutions**:
1. **Proxy Configuration**: Configure proxy settings if required
2. **VPN**: Use personal VPN if allowed
3. **Mobile Hotspot**: Use mobile connection for AI processing
4. **Contact IT**: Request whitelist for API endpoints

### DNS and Connectivity

#### Cannot Reach API Endpoints
**Symptoms**: "Name resolution failed" or similar DNS errors  
**Cause**: DNS issues or network connectivity problems  

**Solutions**:
1. **Test DNS**: Try `nslookup api.openai.com`
2. **Change DNS**: Use public DNS (8.8.8.8, 1.1.1.1)
3. **Check Connectivity**: Test with `ping google.com`
4. **Restart Network**: Reset network adapters

## 🔧 Advanced Troubleshooting

### Log Analysis

#### Accessing Log Files
```bash
# Application logs
type "%APPDATA%\Personal Finance Agent\logs\application.log"

# Error logs
type "%APPDATA%\Personal Finance Agent\logs\error.log"

# System event logs
eventvwr.msc
```

#### Common Log Patterns

**API Errors**:
```
ERROR: OpenAI API call failed: 401 Unauthorized
ERROR: Invalid API key format
ERROR: Rate limit exceeded
```

**Database Errors**:
```
ERROR: SQLite database locked
ERROR: Table doesn't exist
ERROR: Foreign key constraint failed
```

**Network Errors**:
```
ERROR: Connection timeout
ERROR: SSL certificate verification failed
ERROR: Name resolution failed
```

### Diagnostic Tools

#### System Information Collection
```bash
# System info
systeminfo

# Running processes
tasklist | findstr PersonalFinanceAgent

# Network connections
netstat -ano | findstr :8000

# Event logs
wevtutil qe Application /c:10 /f:text /q:"*[System[Provider[@Name='Personal Finance Agent']]]"
```

#### Database Diagnostics
```bash
# Connect to database
sqlite3 "%APPDATA%\Personal Finance Agent\data\finance_agent.db"

# Check tables
.tables

# Check integrity
PRAGMA integrity_check;

# Show indexes
.indexes

# Exit
.quit
```

### Clean Reinstallation

#### Complete Removal
```bash
# 1. Uninstall application
# Control Panel → Programs → Uninstall Personal Finance Agent

# 2. Remove user data
rmdir /s "%APPDATA%\Personal Finance Agent"

# 3. Remove registry entries
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "PersonalFinanceAgent" /f

# 4. Clear temporary files
del /q "%TEMP%\PersonalFinanceAgent*"
```

#### Fresh Installation
```bash
# 1. Download latest installer
# 2. Run as administrator
# 3. Choose clean installation directory
# 4. Reconfigure all settings
```

## 📞 Getting Additional Help

### Before Contacting Support

Collect the following information:
- **Windows Version**: `winver` command output
- **Application Version**: Check in About dialog
- **Error Messages**: Exact text of any error messages
- **Log Files**: Recent entries from application logs
- **Steps to Reproduce**: What you were doing when issue occurred

### Where to Get Help

1. **Documentation**: Check other sections of this documentation
2. **GitHub Issues**: Search existing issues or create new one
3. **Discussions**: Use GitHub Discussions for questions
4. **Community**: Join community forums or Discord

### Reporting Bugs

Include in bug reports:
- **Environment**: Windows version, application version
- **Steps to Reproduce**: Detailed steps to recreate issue
- **Expected Behavior**: What should have happened
- **Actual Behavior**: What actually happened
- **Screenshots**: Visual evidence if helpful
- **Log Files**: Relevant log entries
- **Workarounds**: Any temporary solutions you found

---

**Still Having Issues?** Create a [GitHub issue](https://github.com/yourusername/personal-finance-agent/issues) with detailed information about your problem.