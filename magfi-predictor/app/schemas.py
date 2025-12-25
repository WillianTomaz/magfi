from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from uuid import UUID


class PredictionSchema(BaseModel):
    asset_ticker: Optional[str] = None
    prediction_type: str
    predicted_price: Optional[float] = None
    confidence_score: float
    prediction_date: datetime
    horizon_days: Optional[int] = None
    analysis_summary: Optional[str] = None


class HealthResponseSchema(BaseModel):
    status: str
    app_name: str
    environment: str


class ApiResponseSchema(BaseModel):
    success: bool
    data: Optional[dict] = None
    message: str
    error: Optional[str] = None
