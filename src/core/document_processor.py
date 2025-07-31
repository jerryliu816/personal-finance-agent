import asyncio
import json
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

from .llm_client import LLMClient

class DocumentProcessor:
    def __init__(self):
        self.supported_formats = ['.pdf']
        
    async def process_document(self, file_path: str, llm_client: Optional[LLMClient] = None) -> Dict[str, Any]:
        """
        Process a financial document and extract relevant information
        """
        if not Path(file_path).exists():
            return {"error": "File not found", "success": False}
        
        file_extension = Path(file_path).suffix.lower()
        if file_extension not in self.supported_formats:
            return {"error": f"Unsupported file format: {file_extension}", "success": False}
        
        try:
            # Extract text using MCP PDF server
            text_content = await self._extract_text_via_mcp(file_path)
            if not text_content:
                return {"error": "Failed to extract text from PDF", "success": False}
            
            # Determine document type
            document_type = self._classify_document_type(text_content)
            
            result = {
                "file_path": file_path,
                "file_name": Path(file_path).name,
                "document_type": document_type,
                "extracted_text": text_content,
                "processing_timestamp": datetime.now().isoformat(),
                "success": True
            }
            
            # If LLM client is provided, perform AI analysis
            if llm_client:
                try:
                    analysis = await llm_client.analyze_financial_document(text_content, document_type)
                    result["ai_analysis"] = analysis
                except Exception as e:
                    result["ai_analysis_error"] = str(e)
            
            return result
            
        except Exception as e:
            return {
                "error": str(e),
                "success": False,
                "file_path": file_path
            }
    
    async def _extract_text_via_mcp(self, file_path: str) -> Optional[str]:
        """
        Extract text using the MCP PDF processing server
        """
        try:
            # Start MCP server as subprocess
            process = await asyncio.create_subprocess_exec(
                "python", "-m", "src.mcp.pdf_server",
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Prepare MCP request
            request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": "extract_text",
                    "arguments": {
                        "file_path": file_path,
                        "method": "both"
                    }
                }
            }
            
            # Send request
            request_json = json.dumps(request) + "\n"
            stdout, stderr = await process.communicate(request_json.encode())
            
            if process.returncode == 0:
                response = json.loads(stdout.decode())
                if "result" in response and "content" in response["result"]:
                    content = response["result"]["content"][0]["text"]
                    extraction_results = json.loads(content)
                    
                    # Prefer pdfplumber result, fallback to pymupdf
                    if "pdfplumber" in extraction_results:
                        return extraction_results["pdfplumber"]
                    elif "pymupdf" in extraction_results:
                        return extraction_results["pymupdf"]
            
            return None
            
        except Exception as e:
            print(f"MCP extraction error: {e}")
            # Fallback to direct extraction
            return await self._extract_text_direct(file_path)
    
    async def _extract_text_direct(self, file_path: str) -> Optional[str]:
        """
        Fallback text extraction using direct library calls
        """
        try:
            import PyMuPDF as fitz
            
            doc = fitz.open(file_path)
            text = ""
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                text += f"\n--- Page {page_num + 1} ---\n"
                text += page.get_text()
            doc.close()
            
            return text
            
        except ImportError:
            try:
                import pdfplumber
                
                with pdfplumber.open(file_path) as pdf:
                    text = ""
                    for page_num, page in enumerate(pdf.pages):
                        text += f"\n--- Page {page_num + 1} ---\n"
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text
                
                return text
                
            except ImportError:
                return None
        except Exception as e:
            print(f"Direct extraction error: {e}")
            return None
    
    def _classify_document_type(self, text_content: str) -> str:
        """
        Classify document type based on text content patterns
        """
        text_lower = text_content.lower()
        
        # Credit card patterns
        if any(pattern in text_lower for pattern in [
            'credit card', 'statement balance', 'minimum payment', 'payment due',
            'available credit', 'credit limit', 'annual percentage rate'
        ]):
            return "credit_card"
        
        # Bank statement patterns
        if any(pattern in text_lower for pattern in [
            'checking account', 'savings account', 'account balance',
            'deposits', 'withdrawals', 'opening balance', 'closing balance'
        ]):
            return "bank_statement"
        
        # Investment patterns
        if any(pattern in text_lower for pattern in [
            'portfolio', 'securities', 'dividend', 'capital gains',
            'mutual fund', 'stock', 'bond', 'investment account'
        ]):
            return "investment"
        
        # Tax document patterns
        if any(pattern in text_lower for pattern in [
            'form 1040', 'tax return', 'w-2', '1099', 'irs',
            'adjusted gross income', 'taxable income'
        ]):
            return "tax_document"
        
        # Insurance patterns
        if any(pattern in text_lower for pattern in [
            'insurance', 'policy', 'premium', 'deductible',
            'coverage', 'claim'
        ]):
            return "insurance"
        
        # Loan/mortgage patterns
        if any(pattern in text_lower for pattern in [
            'mortgage', 'loan', 'principal', 'interest rate',
            'monthly payment', 'balance remaining'
        ]):
            return "loan"
        
        return "other"
    
    def get_document_insights(self, analysis_result: Dict[str, Any]) -> List[str]:
        """
        Extract key insights from processed document
        """
        insights = []
        
        if not analysis_result.get("success", False):
            return ["Document processing failed"]
        
        ai_analysis = analysis_result.get("ai_analysis", {})
        
        if "summary" in ai_analysis:
            summary = ai_analysis["summary"]
            if "net_change" in summary:
                net_change = summary["net_change"]
                if net_change > 0:
                    insights.append(f"Net increase of ${net_change:,.2f}")
                elif net_change < 0:
                    insights.append(f"Net decrease of ${abs(net_change):,.2f}")
        
        if "transactions" in ai_analysis:
            transaction_count = len(ai_analysis["transactions"])
            insights.append(f"{transaction_count} transactions processed")
            
            # Find largest transactions
            transactions = ai_analysis["transactions"]
            if transactions:
                largest_expense = min(transactions, key=lambda x: x.get("amount", 0))
                largest_income = max(transactions, key=lambda x: x.get("amount", 0))
                
                if largest_expense.get("amount", 0) < -100:
                    insights.append(f"Largest expense: ${abs(largest_expense['amount']):,.2f} - {largest_expense.get('description', 'Unknown')}")
                
                if largest_income.get("amount", 0) > 100:
                    insights.append(f"Largest income: ${largest_income['amount']:,.2f} - {largest_income.get('description', 'Unknown')}")
        
        if "investments" in ai_analysis and ai_analysis["investments"]:
            total_investment_value = sum(inv.get("value", 0) for inv in ai_analysis["investments"])
            insights.append(f"Total investment value: ${total_investment_value:,.2f}")
        
        if "key_insights" in ai_analysis:
            insights.extend(ai_analysis["key_insights"])
        
        return insights if insights else ["Document processed successfully"]