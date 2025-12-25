from sqlalchemy.orm import Session
from app.models import NewsRaw, NewsAnalysis
from app.schemas import NewsRawSchema, NewsAnalysisSchema
from uuid import UUID
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class NewsService:
    @staticmethod
    def save_raw_news(db: Session, news_data: dict):
        news = NewsRaw(
            feed_source=news_data.get("feed_source"),
            title=news_data.get("title"),
            content=news_data.get("content"),
            link=news_data.get("link"),
            published_date=news_data.get("published_date"),
            raw_data=news_data.get("raw_data"),
        )
        db.add(news)
        db.commit()
        db.refresh(news)
        return news

    @staticmethod
    def save_analysis(db: Session, analysis_data: dict):
        analysis = NewsAnalysis(
            asset_ticker=analysis_data.get("asset_ticker"),
            news_title=analysis_data.get("news_title"),
            news_content=analysis_data.get("news_content"),
            sentiment=analysis_data.get("sentiment"),
            impact_score=analysis_data.get("impact_score", 0),
            ai_analysis=analysis_data.get("ai_analysis"),
            source_url=analysis_data.get("source_url"),
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        return analysis

    @staticmethod
    def get_unprocessed_news(db: Session):
        return db.query(NewsRaw).filter(NewsRaw.is_processed == False).all()

    @staticmethod
    def mark_as_processed(db: Session, news_id: UUID):
        news = db.query(NewsRaw).filter(NewsRaw.id == news_id).first()
        if news:
            news.is_processed = True
            db.commit()

    @staticmethod
    def get_raw_news(db: Session, limit: int = 100):
        return db.query(NewsRaw).order_by(NewsRaw.created_at.desc()).limit(limit).all()

    @staticmethod
    def get_analyzed_news(db: Session, limit: int = 100):
        return db.query(NewsAnalysis).order_by(NewsAnalysis.created_at.desc()).limit(limit).all()
