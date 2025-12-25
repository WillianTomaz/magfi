from sqlalchemy.orm import Session
from app.models import Currency, CurrencyPriceHistory
from app.schemas import CurrencySchema
from uuid import UUID
from datetime import datetime
from decimal import Decimal


class CurrencyService:
    @staticmethod
    def create_currency(db: Session, currency_data: CurrencySchema):
        currency = Currency(
            currency_code=currency_data.currency_code.upper(),
            currency_name=currency_data.currency_code,
            base_currency=currency_data.base_currency or "BRL",
            current_price=Decimal(str(currency_data.current_price)),
            target_price=Decimal(str(currency_data.target_price)) if currency_data.target_price else None,
            drop_alert_enabled=currency_data.drop_alert_enabled,
        )
        db.add(currency)
        db.commit()
        db.refresh(currency)
        return currency

    @staticmethod
    def get_currency_by_code(db: Session, currency_code: str):
        return db.query(Currency).filter(Currency.currency_code == currency_code.upper()).first()

    @staticmethod
    def get_all_currencies(db: Session, active_only: bool = True):
        query = db.query(Currency)
        if active_only:
            query = query.filter(Currency.is_active == True)
        return query.all()

    @staticmethod
    def update_currency(db: Session, currency_code: str, currency_data: CurrencySchema):
        currency = CurrencyService.get_currency_by_code(db, currency_code)
        if not currency:
            return None
        
        if currency_data.current_price:
            currency.current_price = Decimal(str(currency_data.current_price))
        if currency_data.target_price:
            currency.target_price = Decimal(str(currency_data.target_price))
        if currency_data.drop_alert_enabled is not None:
            currency.drop_alert_enabled = currency_data.drop_alert_enabled
        
        currency.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(currency)
        return currency

    @staticmethod
    def delete_currency(db: Session, currency_code: str):
        currency = CurrencyService.get_currency_by_code(db, currency_code)
        if not currency:
            return False
        currency.is_active = False
        currency.updated_at = datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def get_drop_alert_currencies(db: Session):
        currencies = db.query(Currency).filter(
            Currency.drop_alert_enabled == True,
            Currency.target_price.isnot(None),
            Currency.is_active == True
        ).all()
        
        result = []
        for currency in currencies:
            current = float(currency.current_price)
            target = float(currency.target_price)
            time_to_buy = current <= target
            
            if time_to_buy:
                gap = ((target - current) / current * 100) if current > 0 else 0
                result.append({
                    "id": str(currency.id),
                    "currency_code": currency.currency_code,
                    "currency_name": currency.currency_name,
                    "current_price": current,
                    "target_price": target,
                    "time_to_buy": True,
                    "gap_percentage": round(gap, 2)
                })
        
        return result

    @staticmethod
    def record_price_history(db: Session, currency_id: UUID, price: Decimal):
        history = CurrencyPriceHistory(
            currency_id=currency_id,
            price=price,
            recorded_at=datetime.utcnow()
        )
        db.add(history)
        db.commit()
