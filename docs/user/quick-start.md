# Quick Start Guide

Get up and running with Personal Finance Agent in under 10 minutes!

## 🎯 What You'll Accomplish

By the end of this guide, you'll have:
- ✅ Installed Personal Finance Agent
- ✅ Configured your AI provider
- ✅ Uploaded your first financial document
- ✅ Asked your first question to the AI assistant

## 📋 Prerequisites

- **Windows 10 or 11** (64-bit)
- **Internet connection** for AI processing
- **API Key** from OpenAI or Anthropic (we'll help you get this)

## 🚀 Step 1: Installation

### Option A: Easy Installer (Recommended)
1. Download the latest installer from [Releases](https://github.com/yourusername/personal-finance-agent/releases)
2. Run `PersonalFinanceAgent-Setup-1.0.0.exe`
3. Follow the installation wizard
4. Launch from Start Menu or Desktop shortcut

### Option B: Development Setup
```bash
git clone https://github.com/yourusername/personal-finance-agent.git
cd personal-finance-agent
pip install -r requirements.txt
cd src/ui/frontend && npm install && npm run build && cd ../../..
python -m src.tray.tray_app
```

## 🔑 Step 2: Get Your AI API Key

You'll need an API key from either OpenAI or Anthropic:

### OpenAI (Recommended for beginners)
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Go to **API Keys** section
4. Click **Create new secret key**
5. Copy the key (starts with `sk-...`)
6. **Cost**: ~$0.01-0.05 per document analysis

### Anthropic (Advanced users)
1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Sign up or log in
3. Go to **API Keys**
4. Create a new key
5. Copy the key (starts with `sk-ant-...`)

> 💡 **Tip**: Start with OpenAI if you're unsure. You can always switch later.

## ⚙️ Step 3: Configure the Application

1. **Find the System Tray**: Look for the green dollar sign icon in your system tray (bottom-right corner)
2. **Right-click** the icon and select **Settings**
3. **Configure AI Provider**:
   - Select your provider (OpenAI or Anthropic)
   - Paste your API key
   - Click **Save Settings**

![Settings Screenshot](../images/settings-page.png)

## 📄 Step 4: Upload Your First Document

1. From the tray menu, click **Document Analysis**
2. **Drag and drop** a PDF financial document or click **Choose File**
3. **Wait for processing** (usually 30-60 seconds)
4. **Review the results** - you'll see extracted transactions, categories, and insights

### Supported Document Types
- 💳 **Credit Card Statements** - Automatic transaction categorization
- 🏦 **Bank Statements** - Income and expense tracking
- 📊 **Investment Reports** - Portfolio analysis
- 📋 **Tax Documents** - Income and deduction categorization

> 📝 **Note**: Only PDF files are currently supported. Make sure your PDFs are not password-protected.

## 💬 Step 5: Chat with Your AI Assistant

1. Click **Chat Assistant** from the tray menu
2. **Ask a question** about your finances, such as:
   - "What's my current net worth?"
   - "How much did I spend on dining last month?"
   - "What are my biggest expenses?"
   - "Should I increase my investment contributions?"

The AI will provide personalized responses based on your actual financial data!

## 🎉 You're All Set!

Congratulations! You now have a fully functional AI-powered personal finance assistant.

## 🔄 Next Steps

### Explore More Features
- **📊 Dashboard**: View your financial overview with charts and graphs
- **📁 Multiple Documents**: Upload more documents to build a complete financial profile
- **💬 Advanced Questions**: Ask complex financial planning questions
- **⚙️ Email Integration**: Set up automatic document processing (optional)

### Common First Questions to Try
```
"Show me my spending breakdown by category"
"What's my average monthly income?"
"How much am I saving each month?"
"Which investments are performing best?"
"What percentage of my income goes to housing?"
```

## ❓ Need Help?

- **🐛 Something not working?** Check our [Troubleshooting Guide](../troubleshooting/common-issues.md)
- **❓ Have questions?** See our [FAQ](../troubleshooting/faq.md)
- **💡 Want to learn more?** Read the complete [User Manual](user-manual.md)

## 🔒 Security Reminder

- Your financial data stays on your device
- API keys are encrypted and stored locally
- Only document text is sent to AI providers for analysis
- No financial data is stored in the cloud

---

**Estimated completion time**: 5-10 minutes  
**Difficulty**: Beginner  
**Next**: [User Manual](user-manual.md) for advanced features