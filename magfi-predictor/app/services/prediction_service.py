from sqlalchemy.orm import Session
from app.models import Prediction
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class PredictionService:
    @staticmethod
    def save_prediction(db: Session, prediction_data: dict):
        prediction = Prediction(
            asset_ticker=prediction_data.get("asset_ticker"),
            prediction_type=prediction_data.get("prediction_type"),
            predicted_price=prediction_data.get("predicted_price"),
            confidence_score=prediction_data.get("confidence_score"),
            prediction_date=prediction_data.get("prediction_date"),
            horizon_days=prediction_data.get("horizon_days"),
            analysis_summary=prediction_data.get("analysis_summary"),
        )
        db.add(prediction)
        db.commit()
        db.refresh(prediction)
        return prediction

    @staticmethod
    def get_predictions(db: Session, hours: int = 24):
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        return db.query(Prediction).filter(Prediction.created_at >= cutoff_time).all()

    @staticmethod
    def get_asset_predictions(db: Session, ticker: str):
        return db.query(Prediction).filter(Prediction.asset_ticker == ticker.upper()).all()

    @staticmethod
    def predict_sentiment_impact(news_sentiment: str, impact_score: float) -> dict:
        sentiment_multiplier = {"positive": 1.0, "negative": -1.0, "neutral": 0.0}
        direction = sentiment_multiplier.get(news_sentiment.lower(), 0.0)
        
        predicted_change = direction * impact_score * 2.0
        confidence = impact_score
        
        return {
            "direction": direction,
            "predicted_change_percent": predicted_change,
            "confidence": confidence
        }
