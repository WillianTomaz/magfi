from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import CurrencySchema, ApiResponseSchema
from app.services.currency_service import CurrencyService

router = APIRouter(prefix="/market", tags=["currencies"])


@router.post("/currency", response_model=ApiResponseSchema)
def create_currency(currency_data: dict, db: Session = Depends(get_db)):
    try:
        name = currency_data.get("name")
        if not name:
            raise HTTPException(status_code=400, detail="Currency code is required")
        
        schema = CurrencySchema(
            currency_code=name,
            base_currency=currency_data.get("base_currency", "BRL"),
            current_price=currency_data.get("current_price", 0),
            target_price=currency_data.get("target_price"),
            drop_alert_enabled=currency_data.get("drop_alert", False),
        )
        
        currency = CurrencyService.create_currency(db, schema)
        
        return {
            "success": True,
            "data": {
                "id": str(currency.id),
                "currency_code": currency.currency_code,
            },
            "message": "Currency created successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/currency", response_model=ApiResponseSchema)
def get_currency(currency_code: str = Query(...), db: Session = Depends(get_db)):
    try:
        currency = CurrencyService.get_currency_by_code(db, currency_code)
        if not currency:
            raise HTTPException(status_code=404, detail="Currency not found")
        
        return {
            "success": True,
            "data": {
                "id": str(currency.id),
                "currency_code": currency.currency_code,
                "currency_name": currency.currency_name,
                "base_currency": currency.base_currency,
                "current_price": float(currency.current_price),
                "target_price": float(currency.target_price) if currency.target_price else None,
                "drop_alert_enabled": currency.drop_alert_enabled,
                "time_to_buy": currency.time_to_buy,
            },
            "message": "Currency retrieved successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/currencies", response_model=ApiResponseSchema)
def get_all_currencies(db: Session = Depends(get_db)):
    try:
        currencies = CurrencyService.get_all_currencies(db)
        data = [
            {
                "id": str(c.id),
                "currency_code": c.currency_code,
                "currency_name": c.currency_name,
                "base_currency": c.base_currency,
                "current_price": float(c.current_price),
                "target_price": float(c.target_price) if c.target_price else None,
                "drop_alert_enabled": c.drop_alert_enabled,
                "time_to_buy": c.time_to_buy,
            }
            for c in currencies
        ]
        
        return {
            "success": True,
            "data": data,
            "message": "Currencies retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/currency", response_model=ApiResponseSchema)
def update_currency(currency_code: str = Query(...), currency_data: dict = None, db: Session = Depends(get_db)):
    try:
        if not currency_data:
            raise HTTPException(status_code=400, detail="Currency data is required")
        
        schema = CurrencySchema(
            currency_code=currency_code,
            base_currency=currency_data.get("base_currency", "BRL"),
            current_price=currency_data.get("current_price", 0),
            target_price=currency_data.get("target_price"),
            drop_alert_enabled=currency_data.get("drop_alert"),
        )
        
        currency = CurrencyService.update_currency(db, currency_code, schema)
        if not currency:
            raise HTTPException(status_code=404, detail="Currency not found")
        
        return {
            "success": True,
            "data": {"currency_code": currency.currency_code},
            "message": "Currency updated successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/currency", response_model=ApiResponseSchema)
def delete_currency(currency_code: str = Query(...), db: Session = Depends(get_db)):
    try:
        result = CurrencyService.delete_currency(db, currency_code)
        if not result:
            raise HTTPException(status_code=404, detail="Currency not found")
        
        return {
            "success": True,
            "data": None,
            "message": "Currency deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
