from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json

from ..ui.backend.models import FinancialProfile, Document

class FinanceProfileManager:
    def __init__(self, db: Session):
        self.db = db
    
    def add_financial_entry(self, category: str, subcategory: str, amount: float, 
                           date: datetime, description: str, source_document_id: int,
                           metadata: Optional[Dict[str, Any]] = None) -> FinancialProfile:
        """
        Add a new financial entry to the profile
        """
        entry = FinancialProfile(
            category=category,
            subcategory=subcategory,
            amount=amount,
            date=date,
            description=description,
            source_document_id=source_document_id,
            metadata=json.dumps(metadata) if metadata else None
        )
        
        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)
        
        return entry
    
    def process_document_analysis(self, document_id: int, analysis: Dict[str, Any]):
        """
        Process AI analysis results and create financial profile entries
        """
        if not analysis.get("success", False) or "ai_analysis" not in analysis:
            return
        
        ai_analysis = analysis["ai_analysis"]
        
        # Process transactions
        if "transactions" in ai_analysis:
            for txn in ai_analysis["transactions"]:
                try:
                    date = datetime.fromisoformat(txn["date"]) if txn.get("date") else datetime.now()
                    
                    self.add_financial_entry(
                        category=self._map_category(txn.get("category", "other")),
                        subcategory=txn.get("type", "unknown"),
                        amount=float(txn.get("amount", 0)),
                        date=date,
                        description=txn.get("description", ""),
                        source_document_id=document_id,
                        metadata={"transaction_type": txn.get("type"), "original_category": txn.get("category")}
                    )
                except Exception as e:
                    print(f"Error processing transaction: {e}")
        
        # Process investments
        if "investments" in ai_analysis:
            for inv in ai_analysis["investments"]:
                try:
                    self.add_financial_entry(
                        category="investments",
                        subcategory=inv.get("type", "unknown"),
                        amount=float(inv.get("value", 0)),
                        date=datetime.now(),
                        description=f"{inv.get('symbol')} - {inv.get('shares', 0)} shares",
                        source_document_id=document_id,
                        metadata={"symbol": inv.get("symbol"), "shares": inv.get("shares"), "price": inv.get("price")}
                    )
                except Exception as e:
                    print(f"Error processing investment: {e}")
    
    def get_profile_summary(self) -> Dict[str, Any]:
        """
        Generate comprehensive financial profile summary
        """
        # Calculate totals by category
        income_total = self.db.query(func.sum(FinancialProfile.amount)).filter(
            FinancialProfile.category == "income",
            FinancialProfile.amount > 0
        ).scalar() or 0.0
        
        expense_total = abs(self.db.query(func.sum(FinancialProfile.amount)).filter(
            FinancialProfile.category.in_(["expenses", "food", "gas", "shopping", "entertainment"]),
            FinancialProfile.amount < 0
        ).scalar() or 0.0)
        
        asset_total = self.db.query(func.sum(FinancialProfile.amount)).filter(
            FinancialProfile.category.in_(["assets", "investments"]),
            FinancialProfile.amount > 0
        ).scalar() or 0.0
        
        liability_total = abs(self.db.query(func.sum(FinancialProfile.amount)).filter(
            FinancialProfile.category == "liabilities",
            FinancialProfile.amount < 0
        ).scalar() or 0.0)
        
        # Get investment portfolio
        investment_portfolio = {}
        investments = self.db.query(FinancialProfile).filter(
            FinancialProfile.category == "investments"
        ).all()
        
        for inv in investments:
            if inv.metadata:
                try:
                    metadata = json.loads(inv.metadata)
                    symbol = metadata.get("symbol")
                    if symbol:
                        investment_portfolio[symbol] = investment_portfolio.get(symbol, 0) + inv.amount
                except:
                    pass
        
        # Get recent transactions
        recent_transactions = self.db.query(FinancialProfile).order_by(
            desc(FinancialProfile.date)
        ).limit(20).all()
        
        recent_txns = []
        for txn in recent_transactions:
            recent_txns.append({
                "date": txn.date.isoformat() if txn.date else None,
                "description": txn.description,
                "amount": txn.amount,
                "category": txn.category,
                "subcategory": txn.subcategory
            })
        
        # Calculate monthly averages (last 3 months)
        three_months_ago = datetime.now() - timedelta(days=90)
        
        monthly_income = self.db.query(func.sum(FinancialProfile.amount)).filter(
            FinancialProfile.category == "income",
            FinancialProfile.date >= three_months_ago,
            FinancialProfile.amount > 0
        ).scalar() or 0.0
        monthly_income = monthly_income / 3  # Average over 3 months
        
        monthly_expenses = abs(self.db.query(func.sum(FinancialProfile.amount)).filter(
            FinancialProfile.category.in_(["expenses", "food", "gas", "shopping", "entertainment"]),
            FinancialProfile.date >= three_months_ago,
            FinancialProfile.amount < 0
        ).scalar() or 0.0)
        monthly_expenses = monthly_expenses / 3  # Average over 3 months
        
        return {
            "total_assets": asset_total,
            "total_liabilities": liability_total,
            "net_worth": asset_total - liability_total,
            "monthly_income": monthly_income,
            "monthly_expenses": monthly_expenses,
            "investment_portfolio": investment_portfolio,
            "credit_accounts": self._get_credit_accounts(),
            "recent_transactions": recent_txns,
            "last_updated": datetime.now().isoformat()
        }
    
    def get_chat_context(self) -> Dict[str, Any]:
        """
        Get financial context for chat interactions
        """
        summary = self.get_profile_summary()
        
        # Simplified context for chat
        return {
            "net_worth": summary["net_worth"],
            "monthly_income": summary["monthly_income"],
            "monthly_expenses": summary["monthly_expenses"],
            "investment_portfolio": summary["investment_portfolio"],
            "recent_transactions": summary["recent_transactions"][:5]  # Last 5 transactions
        }
    
    def _map_category(self, original_category: str) -> str:
        """
        Map AI-detected categories to our standard categories
        """
        category_mapping = {
            "food": "expenses",
            "gas": "expenses", 
            "shopping": "expenses",
            "entertainment": "expenses",
            "income": "income",
            "salary": "income",
            "investment": "investments",
            "stock": "investments",
            "bond": "investments",
            "credit": "liabilities",
            "loan": "liabilities",
            "mortgage": "liabilities"
        }
        
        return category_mapping.get(original_category.lower(), "other")
    
    def _get_credit_accounts(self) -> List[Dict[str, Any]]:
        """
        Get credit account information
        """
        credit_accounts = []
        
        # This would be populated from credit card statements
        # For now, return empty list - would be filled by document analysis
        
        return credit_accounts
    
    def get_spending_trends(self, days: int = 30) -> Dict[str, Any]:
        """
        Analyze spending trends over specified period
        """
        start_date = datetime.now() - timedelta(days=days)
        
        expenses = self.db.query(FinancialProfile).filter(
            FinancialProfile.date >= start_date,
            FinancialProfile.amount < 0
        ).all()
        
        category_totals = {}
        daily_spending = {}
        
        for expense in expenses:
            # Category totals
            category = expense.category
            category_totals[category] = category_totals.get(category, 0) + abs(expense.amount)
            
            # Daily spending
            day = expense.date.date().isoformat() if expense.date else "unknown"
            daily_spending[day] = daily_spending.get(day, 0) + abs(expense.amount)
        
        return {
            "period_days": days,
            "category_totals": category_totals,
            "daily_spending": daily_spending,
            "total_spending": sum(category_totals.values()),
            "average_daily_spending": sum(daily_spending.values()) / max(len(daily_spending), 1)
        }