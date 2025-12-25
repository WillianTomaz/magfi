from sqlalchemy import Column, String, DateTime, Boolean, UUID, ForeignKey, Float, Text
import uuid
from datetime import datetime
from app.database import Base


class NewsRaw(Base):
    __tablename__ = "stg_news_raw"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    feed_source = Column(String(500), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    link = Column(String(500), nullable=True)
    published_date = Column(DateTime, nullable=True)
    raw_data = Column(Text, nullable=True)
    is_processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class NewsAnalysis(Base):
    __tablename__ = "fct_news_analysis"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_ticker = Column(String(20), nullable=True)
    news_title = Column(String, nullable=False)
    news_content = Column(Text, nullable=False)
    sentiment = Column(String(20), nullable=False)
    impact_score = Column(Float, nullable=False)
    ai_analysis = Column(Text, nullable=True)
    source_url = Column(String(500), nullable=True)
    analyzed_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
