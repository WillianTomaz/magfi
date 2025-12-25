from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import AssetSchema, AssetResponseSchema, ApiResponseSchema
from app.services.asset_service import AssetService

router = APIRouter(prefix="/market", tags=["assets"])


@router.post("/asset", response_model=ApiResponseSchema)
def create_asset(asset_data: dict, db: Session = Depends(get_db)):
    try:
        name = asset_data.get("name")
        if not name:
            raise HTTPException(status_code=400, detail="Asset name is required")
        
        schema = AssetSchema(
            ticker_symbol=name,
            currency_code=asset_data.get("currency_code", "BRL"),
            current_price=asset_data.get("current_price", 0),
            target_price=asset_data.get("target_price"),
            drop_alert_enabled=asset_data.get("drop_alert", False),
            target_gap_percentage=asset_data.get("target_gap_percentage"),
            sector=asset_data.get("sector"),
            pl_ratio=asset_data.get("pl_ratio"),
            pvpa_ratio=asset_data.get("pvpa_ratio"),
        )
        
        asset = AssetService.create_asset(db, schema, asset_data.get("name"))
        
        return {
            "success": True,
            "data": {
                "id": str(asset.id),
                "ticker_symbol": asset.ticker_symbol,
                "asset_name": asset.asset_name,
            },
            "message": "Asset created successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/asset", response_model=ApiResponseSchema)
def get_asset(ticker_symbol: str = Query(...), db: Session = Depends(get_db)):
    try:
        asset = AssetService.get_asset_by_ticker(db, ticker_symbol)
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        
        return {
            "success": True,
            "data": {
                "id": str(asset.id),
                "ticker_symbol": asset.ticker_symbol,
                "asset_name": asset.asset_name,
                "currency_code": asset.currency_code,
                "current_price": float(asset.current_price),
                "target_price": float(asset.target_price) if asset.target_price else None,
                "drop_alert_enabled": asset.drop_alert_enabled,
                "time_to_buy": asset.time_to_buy,
                "sector": asset.sector,
                "pl_ratio": asset.pl_ratio,
                "pvpa_ratio": asset.pvpa_ratio,
            },
            "message": "Asset retrieved successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/assets", response_model=ApiResponseSchema)
def get_all_assets(db: Session = Depends(get_db)):
    try:
        assets = AssetService.get_all_assets(db)
        data = [
            {
                "id": str(a.id),
                "ticker_symbol": a.ticker_symbol,
                "asset_name": a.asset_name,
                "currency_code": a.currency_code,
                "current_price": float(a.current_price),
                "target_price": float(a.target_price) if a.target_price else None,
                "drop_alert_enabled": a.drop_alert_enabled,
                "time_to_buy": a.time_to_buy,
            }
            for a in assets
        ]
        
        return {
            "success": True,
            "data": data,
            "message": "Assets retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/asset", response_model=ApiResponseSchema)
def update_asset(ticker_symbol: str = Query(...), asset_data: dict = None, db: Session = Depends(get_db)):
    try:
        if not asset_data:
            raise HTTPException(status_code=400, detail="Asset data is required")
        
        schema = AssetSchema(
            ticker_symbol=ticker_symbol,
            currency_code=asset_data.get("currency_code"),
            current_price=asset_data.get("current_price", 0),
            target_price=asset_data.get("target_price"),
            drop_alert_enabled=asset_data.get("drop_alert"),
            target_gap_percentage=asset_data.get("target_gap_percentage"),
        )
        
        asset = AssetService.update_asset(db, ticker_symbol, schema)
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        
        return {
            "success": True,
            "data": {"ticker_symbol": asset.ticker_symbol},
            "message": "Asset updated successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/asset", response_model=ApiResponseSchema)
def delete_asset(ticker_symbol: str = Query(...), db: Session = Depends(get_db)):
    try:
        result = AssetService.delete_asset(db, ticker_symbol)
        if not result:
            raise HTTPException(status_code=404, detail="Asset not found")
        
        return {
            "success": True,
            "data": None,
            "message": "Asset deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
