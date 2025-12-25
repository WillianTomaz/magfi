from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID


class NewsRawSchema(BaseModel):
    feed_source: str
    title: str
    content: str
    link: Optional[str] = None
    published_date: Optional[datetime] = None


class NewsAnalysisSchema(BaseModel):
    asset_ticker: Optional[str] = None
    news_title: str
    news_content: str
    sentiment: str
    impact_score: float
    ai_analysis: Optional[str] = None
    source_url: Optional[str] = None


class HealthResponseSchema(BaseModel):
    status: str
    app_name: str
    environment: str


class ApiResponseSchema(BaseModel):
    success: bool
    data: Optional[dict] = None
    message: str
    error: Optional[str] = None
