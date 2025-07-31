import openai
import anthropic
from typing import Dict, Any, Optional, List
import json

class LLMClient:
    def __init__(self, provider: str, api_key: str):
        self.provider = provider.lower()
        self.api_key = api_key
        
        if self.provider == "openai":
            self.client = openai.OpenAI(api_key=api_key)
        elif self.provider == "anthropic":
            self.client = anthropic.Anthropic(api_key=api_key)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    async def analyze_financial_document(self, text_content: str, document_type: str = "financial") -> Dict[str, Any]:
        prompt = self._get_financial_analysis_prompt(text_content, document_type)
        
        try:
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a financial document analysis expert. Analyze documents and extract structured financial information."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.1
                )
                content = response.choices[0].message.content
            
            elif self.provider == "anthropic":
                response = self.client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=4000,
                    temperature=0.1,
                    system="You are a financial document analysis expert. Analyze documents and extract structured financial information.",
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                content = response.content[0].text
            
            # Parse the JSON response
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # If JSON parsing fails, return raw content
                return {"raw_analysis": content, "parsing_error": True}
                
        except Exception as e:
            return {"error": str(e), "success": False}

    async def chat_with_context(self, message: str, financial_context: Dict[str, Any]) -> str:
        context_prompt = self._format_financial_context(financial_context)
        full_prompt = f"""
Financial Context:
{context_prompt}

User Question: {message}

Please provide a helpful response based on the financial context provided. Be specific and reference actual numbers from the user's financial profile when relevant.
"""
        
        try:
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a personal finance advisor with access to the user's financial profile. Provide helpful, specific advice based on their actual financial data."},
                        {"role": "user", "content": full_prompt}
                    ],
                    temperature=0.3
                )
                return response.choices[0].message.content
            
            elif self.provider == "anthropic":
                response = self.client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=2000,
                    temperature=0.3,
                    system="You are a personal finance advisor with access to the user's financial profile. Provide helpful, specific advice based on their actual financial data.",
                    messages=[
                        {"role": "user", "content": full_prompt}
                    ]
                )
                return response.content[0].text
                
        except Exception as e:
            return f"I apologize, but I encountered an error processing your request: {str(e)}"

    def _get_financial_analysis_prompt(self, text_content: str, document_type: str) -> str:
        return f"""
Analyze the following {document_type} document and extract structured financial information.

Document Content:
{text_content}

Please extract and return a JSON object with the following structure:
{{
    "document_type": "credit_card|bank_statement|investment|tax_document|other",
    "date_range": {{
        "start_date": "YYYY-MM-DD",
        "end_date": "YYYY-MM-DD"
    }},
    "account_info": {{
        "account_number": "masked account number",
        "institution": "bank/credit card company name",
        "account_type": "checking|savings|credit|investment|other"
    }},
    "transactions": [
        {{
            "date": "YYYY-MM-DD",
            "description": "transaction description",
            "amount": -123.45,
            "category": "food|gas|shopping|entertainment|income|other",
            "type": "debit|credit"
        }}
    ],
    "summary": {{
        "total_debits": -1234.56,
        "total_credits": 5678.90,
        "net_change": 4444.34,
        "starting_balance": 1000.00,
        "ending_balance": 5444.34
    }},
    "investments": [
        {{
            "symbol": "AAPL",
            "shares": 10.5,
            "price": 150.00,
            "value": 1575.00,
            "type": "stock|bond|mutual_fund|etf"
        }}
    ],
    "key_insights": [
        "Notable patterns or important information extracted from the document"
    ]
}}

Ensure all monetary amounts are properly formatted as numbers (positive for credits/income, negative for debits/expenses).
If certain information is not available, use null or empty arrays as appropriate.
"""

    def _format_financial_context(self, context: Dict[str, Any]) -> str:
        formatted = []
        
        if "net_worth" in context:
            formatted.append(f"Net Worth: ${context['net_worth']:,.2f}")
        
        if "monthly_income" in context:
            formatted.append(f"Monthly Income: ${context['monthly_income']:,.2f}")
            
        if "monthly_expenses" in context:
            formatted.append(f"Monthly Expenses: ${context['monthly_expenses']:,.2f}")
        
        if "investment_portfolio" in context and context["investment_portfolio"]:
            formatted.append("Investment Portfolio:")
            for symbol, value in context["investment_portfolio"].items():
                formatted.append(f"  - {symbol}: ${value:,.2f}")
        
        if "recent_transactions" in context and context["recent_transactions"]:
            formatted.append("Recent Transactions:")
            for txn in context["recent_transactions"][:5]:  # Show last 5
                formatted.append(f"  - {txn.get('date', 'N/A')}: {txn.get('description', 'N/A')} ${txn.get('amount', 0):,.2f}")
        
        return "\n".join(formatted)