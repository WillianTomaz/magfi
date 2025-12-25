from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ApiResponseSchema
from app.services.data_fetcher import DataFetcher
from app.services.prediction_service import PredictionService
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/predict", tags=["predict"])


@router.get("", response_model=ApiResponseSchema)
async def get_market_prediction(db: Session = Depends(get_db)):
    try:
        assets = await DataFetcher.fetch_assets()
        news = await DataFetcher.fetch_news_analysis()
        
        predictions = []
        
        for asset in assets[:5]:
            ticker = asset.get("ticker_symbol")
            current_price = asset.get("current_price", 0)
            
            sentiment_impacts = [
                n for n in news 
                if n.get("ticker", "").upper() == ticker.upper()
            ]
            
            if sentiment_impacts:
                avg_sentiment = sentiment_impacts[0].get("sentiment", "neutral")
                avg_impact = sum(n.get("impact_score", 0) for n in sentiment_impacts) / len(sentiment_impacts)
                
                sentiment_pred = PredictionService.predict_sentiment_impact(avg_sentiment, avg_impact)
                predicted_price = current_price * (1 + sentiment_pred["predicted_change_percent"] / 100)
                
                prediction_data = {
                    "asset_ticker": ticker,
                    "prediction_type": "sentiment_based",
                    "predicted_price": predicted_price,
                    "confidence_score": sentiment_pred["confidence"],
                    "prediction_date": datetime.utcnow(),
                    "horizon_days": 7,
                    "analysis_summary": f"Prediction based on {len(sentiment_impacts)} recent news items with {avg_sentiment} sentiment"
                }
                
                PredictionService.save_prediction(db, prediction_data)
                
                predictions.append({
                    "ticker": ticker,
                    "current_price": current_price,
                    "predicted_price": round(predicted_price, 2),
                    "confidence": round(sentiment_pred["confidence"], 2),
                    "direction": "bullish" if sentiment_pred["direction"] > 0 else ("bearish" if sentiment_pred["direction"] < 0 else "neutral"),
                })
        
        return {
            "success": True,
            "data": predictions,
            "message": f"Generated predictions for {len(predictions)} assets"
        }
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{ticker}", response_model=ApiResponseSchema)
async def get_asset_prediction(ticker: str, db: Session = Depends(get_db)):
    try:
        asset = await DataFetcher.fetch_asset(ticker)
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        
        news = await DataFetcher.fetch_news_analysis()
        sentiment_impacts = [n for n in news if n.get("ticker", "").upper() == ticker.upper()]
        
        if sentiment_impacts:
            avg_sentiment = sentiment_impacts[0].get("sentiment", "neutral")
            avg_impact = sum(n.get("impact_score", 0) for n in sentiment_impacts) / len(sentiment_impacts)
            
            sentiment_pred = PredictionService.predict_sentiment_impact(avg_sentiment, avg_impact)
            current_price = asset.get("current_price", 0)
            predicted_price = current_price * (1 + sentiment_pred["predicted_change_percent"] / 100)
            
            return {
                "success": True,
                "data": {
                    "ticker": ticker,
                    "current_price": current_price,
                    "predicted_price": round(predicted_price, 2),
                    "confidence": round(sentiment_pred["confidence"], 2),
                    "direction": "bullish" if sentiment_pred["direction"] > 0 else ("bearish" if sentiment_pred["direction"] < 0 else "neutral"),
                    "analysis_based_on_news_items": len(sentiment_impacts),
                },
                "message": "Prediction generated successfully"
            }
        else:
            return {
                "success": True,
                "data": {
                    "ticker": ticker,
                    "current_price": asset.get("current_price", 0),
                    "message": "No recent news available for prediction"
                },
                "message": "Insufficient data for accurate prediction"
            }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction error for {ticker}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
