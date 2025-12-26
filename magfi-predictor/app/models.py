from sqlalchemy import Column, String, DateTime, UUID, Float, Text
import uuid
from datetime import datetime
from app.database import Base


class Prediction(Base):
    __tablename__ = "fct_prediction"
    __table_args__ = {"schema": "app_magfi"}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id = Column(UUID(as_uuid=True), nullable=True)
    prediction_type = Column(String(50), nullable=False)
    predicted_price = Column(Float, nullable=True)
    confidence_score = Column(Float, nullable=False)
    prediction_date = Column(DateTime, nullable=False)
    analysis_summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
