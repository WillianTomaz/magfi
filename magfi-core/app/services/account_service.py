from sqlalchemy.orm import Session
from app.models import Account, PortfolioPosition, Dividend
from app.schemas import AccountSchema
from datetime import datetime
from decimal import Decimal
from sqlalchemy import func


class AccountService:
    @staticmethod
    def create_account(db: Session, account_data: AccountSchema):
        account = Account(
            account_name=account_data.account_name,
            is_investment_account=account_data.is_investment_account,
            is_payroll_account=account_data.is_payroll_account,
            total_invested=Decimal(str(account_data.total_invested)) if account_data.total_invested else None,
            monthly_salary=Decimal(str(account_data.monthly_salary)) if account_data.monthly_salary else None,
            checking_account_balance=Decimal(str(account_data.checking_account_balance)) if account_data.checking_account_balance else None,
            default_currency=account_data.default_currency or "BRL",
        )
        db.add(account)
        db.commit()
        db.refresh(account)
        return account

    @staticmethod
    def get_all_accounts(db: Session, active_only: bool = True):
        query = db.query(Account)
        if active_only:
            query = query.filter(Account.is_active == True)
        return query.all()

    @staticmethod
    def get_account_by_id(db: Session, account_id):
        return db.query(Account).filter(Account.id == account_id, Account.is_active == True).first()

    @staticmethod
    def get_dividend_gains(db: Session, period: str = "year"):
        dividends = db.query(Dividend).all()
        
        result = []
        for dividend in dividends:
            result.append({
                "asset_id": str(dividend.asset_id),
                "dividend_amount": float(dividend.dividend_amount),
                "dividend_type": dividend.dividend_type,
                "ex_dividend_date": dividend.ex_dividend_date.isoformat(),
                "payment_date": dividend.payment_date.isoformat(),
            })
        
        return result
