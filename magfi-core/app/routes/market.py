from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ApiResponseSchema
from app.services.asset_service import AssetService
from app.services.currency_service import CurrencyService
from app.services.prediction_service import PredictionService

router = APIRouter(prefix="/market", tags=["alerts_and_reports"])


@router.get("/drop-alert/assets", response_model=ApiResponseSchema)
def get_drop_alert_assets(db: Session = Depends(get_db)):
    try:
        assets = AssetService.get_drop_alert_assets(db)
        
        return {
            "success": True,
            "data": assets,
            "message": f"Found {len(assets)} assets ready to buy"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/drop-alert/currencies", response_model=ApiResponseSchema)
def get_drop_alert_currencies(db: Session = Depends(get_db)):
    try:
        currencies = CurrencyService.get_drop_alert_currencies(db)
        
        return {
            "success": True,
            "data": currencies,
            "message": f"Found {len(currencies)} currencies ready to buy"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/report/prediction", response_model=ApiResponseSchema)
async def get_market_prediction(db: Session = Depends(get_db)):
    try:
        prediction = await PredictionService.get_market_prediction()
        
        return {
            "success": True,
            "data": prediction,
            "message": "Market prediction report generated"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
