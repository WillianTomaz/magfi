from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ApiResponseSchema
from app.services.rss_collector import RSSCollector
from app.services.news_service import NewsService
from app.services.ai_analyzer import AIAnalyzer
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/ingest", tags=["ingest"])


@router.post("/news", response_model=ApiResponseSchema)
async def ingest_news(db: Session = Depends(get_db)):
    try:
        articles = RSSCollector.collect_feeds()
        
        saved_count = 0
        for article in articles:
            try:
                news = NewsService.save_raw_news(db, article)
                
                analysis = await AIAnalyzer.analyze_sentiment(
                    f"{article.get('title')} {article.get('content')}"
                )
                
                analysis_data = {
                    "asset_ticker": analysis.get("tickers", [None])[0] if analysis.get("tickers") else None,
                    "news_title": article.get("title"),
                    "news_content": article.get("content"),
                    "sentiment": analysis.get("sentiment", "neutral"),
                    "impact_score": analysis.get("impact_score", 0.5),
                    "ai_analysis": analysis.get("analysis"),
                    "source_url": article.get("link"),
                }
                
                NewsService.save_analysis(db, analysis_data)
                NewsService.mark_as_processed(db, news.id)
                saved_count += 1
            except Exception as e:
                logger.error(f"Error processing article: {str(e)}")
                continue
        
        return {
            "success": True,
            "data": {"ingested_count": saved_count},
            "message": f"Successfully ingested {saved_count} news items"
        }
    except Exception as e:
        logger.error(f"Ingestion error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/news/raw", response_model=ApiResponseSchema)
def get_raw_news(limit: int = 100, db: Session = Depends(get_db)):
    try:
        news = NewsService.get_raw_news(db, limit)
        data = [
            {
                "id": str(n.id),
                "title": n.title,
                "source": n.feed_source,
                "created_at": n.created_at.isoformat(),
            }
            for n in news
        ]
        
        return {
            "success": True,
            "data": data,
            "message": "Raw news retrieved"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/news/analyzed", response_model=ApiResponseSchema)
def get_analyzed_news(limit: int = 100, db: Session = Depends(get_db)):
    try:
        news = NewsService.get_analyzed_news(db, limit)
        data = [
            {
                "id": str(n.id),
                "title": n.news_title,
                "sentiment": n.sentiment,
                "impact_score": n.impact_score,
                "ticker": n.asset_ticker,
            }
            for n in news
        ]
        
        return {
            "success": True,
            "data": data,
            "message": "Analyzed news retrieved"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
