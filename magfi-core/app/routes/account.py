from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import AccountSchema, ApiResponseSchema
from app.services.account_service import AccountService

router = APIRouter(prefix="/market", tags=["accounts"])


@router.post("/account", response_model=ApiResponseSchema)
def create_account(account_data: dict, db: Session = Depends(get_db)):
    try:
        schema = AccountSchema(
            account_name=account_data.get("account_name"),
            is_investment_account=account_data.get("is_investment_account", False),
            is_payroll_account=account_data.get("is_payroll_account", False),
            total_invested=account_data.get("total_invested"),
            monthly_salary=account_data.get("monthly_salary"),
            checking_account_balance=account_data.get("checking_account_balance"),
            default_currency=account_data.get("default_currency", "BRL"),
        )
        
        account = AccountService.create_account(db, schema)
        
        return {
            "success": True,
            "data": {"id": str(account.id), "account_name": account.account_name},
            "message": "Account created successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/accounts", response_model=ApiResponseSchema)
def get_all_accounts(db: Session = Depends(get_db)):
    try:
        accounts = AccountService.get_all_accounts(db)
        data = [
            {
                "id": str(a.id),
                "account_name": a.account_name,
                "is_investment_account": a.is_investment_account,
                "is_payroll_account": a.is_payroll_account,
                "total_invested": float(a.total_invested) if a.total_invested else None,
                "default_currency": a.default_currency,
            }
            for a in accounts
        ]
        
        return {
            "success": True,
            "data": data,
            "message": "Accounts retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dividend-gains", response_model=ApiResponseSchema)
def get_dividend_gains(db: Session = Depends(get_db)):
    try:
        dividends = AccountService.get_dividend_gains(db)
        
        return {
            "success": True,
            "data": dividends,
            "message": "Dividend gains retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
