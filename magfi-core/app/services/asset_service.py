from sqlalchemy.orm import Session
from app.models import Asset, AssetPriceHistory
from app.schemas import AssetSchema
from uuid import UUID
from datetime import datetime
from decimal import Decimal


class AssetService:
    @staticmethod
    def create_asset(db: Session, asset_data: AssetSchema, asset_name: str = None):
        asset = Asset(
            ticker_symbol=asset_data.ticker_symbol.upper(),
            asset_name=asset_name or asset_data.ticker_symbol,
            currency_code=asset_data.currency_code or "BRL",
            current_price=Decimal(str(asset_data.current_price)),
            target_price=Decimal(str(asset_data.target_price)) if asset_data.target_price else None,
            drop_alert_enabled=asset_data.drop_alert_enabled,
            target_gap_percentage=asset_data.target_gap_percentage,
            sector=asset_data.sector,
            pl_ratio=asset_data.pl_ratio,
            pvpa_ratio=asset_data.pvpa_ratio,
        )
        db.add(asset)
        db.commit()
        db.refresh(asset)
        return asset

    @staticmethod
    def get_asset_by_ticker(db: Session, ticker_symbol: str):
        return db.query(Asset).filter(Asset.ticker_symbol == ticker_symbol.upper()).first()

    @staticmethod
    def get_all_assets(db: Session, active_only: bool = True):
        query = db.query(Asset)
        if active_only:
            query = query.filter(Asset.is_active == True)
        return query.all()

    @staticmethod
    def update_asset(db: Session, ticker_symbol: str, asset_data: AssetSchema):
        asset = AssetService.get_asset_by_ticker(db, ticker_symbol)
        if not asset:
            return None
        
        if asset_data.current_price:
            asset.current_price = Decimal(str(asset_data.current_price))
        if asset_data.target_price:
            asset.target_price = Decimal(str(asset_data.target_price))
        if asset_data.drop_alert_enabled is not None:
            asset.drop_alert_enabled = asset_data.drop_alert_enabled
        if asset_data.target_gap_percentage:
            asset.target_gap_percentage = asset_data.target_gap_percentage
        if asset_data.sector:
            asset.sector = asset_data.sector
        if asset_data.pl_ratio:
            asset.pl_ratio = asset_data.pl_ratio
        if asset_data.pvpa_ratio:
            asset.pvpa_ratio = asset_data.pvpa_ratio
        
        asset.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(asset)
        return asset

    @staticmethod
    def delete_asset(db: Session, ticker_symbol: str):
        asset = AssetService.get_asset_by_ticker(db, ticker_symbol)
        if not asset:
            return False
        asset.is_active = False
        asset.updated_at = datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def get_drop_alert_assets(db: Session):
        assets = db.query(Asset).filter(
            Asset.drop_alert_enabled == True,
            Asset.target_price.isnot(None),
            Asset.is_active == True
        ).all()
        
        result = []
        for asset in assets:
            current = float(asset.current_price)
            target = float(asset.target_price)
            time_to_buy = current <= target
            
            if time_to_buy:
                gap = ((target - current) / current * 100) if current > 0 else 0
                result.append({
                    "id": str(asset.id),
                    "ticker_symbol": asset.ticker_symbol,
                    "asset_name": asset.asset_name,
                    "current_price": current,
                    "target_price": target,
                    "time_to_buy": True,
                    "gap_percentage": round(gap, 2)
                })
        
        return result

    @staticmethod
    def record_price_history(db: Session, asset_id: UUID, price: Decimal):
        history = AssetPriceHistory(
            asset_id=asset_id,
            price=price,
            recorded_at=datetime.utcnow()
        )
        db.add(history)
        db.commit()
