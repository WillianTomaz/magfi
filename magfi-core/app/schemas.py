from pydantic import BaseModel, Field
from typing import Optional, List, Union
from datetime import datetime
from uuid import UUID


class ConfigSchema(BaseModel):
    config_name: str
    config_value: Optional[str] = None
    
    class Config:
        from_attributes = True


class ConfigResponseSchema(ConfigSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime


class AssetSchema(BaseModel):
    ticker_symbol: str
    currency_code: Optional[str] = None
    current_price: float
    target_price: Optional[float] = None
    drop_alert_enabled: Optional[bool] = False
    target_gap_percentage: Optional[float] = None
    sector: Optional[str] = None
    pl_ratio: Optional[float] = None
    pvpa_ratio: Optional[float] = None


class AssetCreateSchema(BaseModel):
    name: str
    ticker_symbol: Optional[str] = None
    currency_code: Optional[str] = "BRL"
    current_price: float
    target_price: Optional[float] = None
    drop_alert_enabled: Optional[bool] = False
    target_gap_percentage: Optional[float] = None
    sector: Optional[str] = None
    pl_ratio: Optional[float] = None
    pvpa_ratio: Optional[float] = None


class AssetResponseSchema(BaseModel):
    id: UUID
    ticker_symbol: str
    asset_name: str
    currency_code: str
    current_price: float
    target_price: Optional[float]
    drop_alert_enabled: bool
    target_gap_percentage: Optional[float]
    time_to_buy: bool
    sector: Optional[str]
    pl_ratio: Optional[float]
    pvpa_ratio: Optional[float]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CurrencySchema(BaseModel):
    currency_code: str = Field(..., alias="name")
    base_currency: Optional[str] = "BRL"
    current_price: float
    target_price: Optional[float] = None
    drop_alert_enabled: Optional[bool] = False


class CurrencyResponseSchema(BaseModel):
    id: UUID
    currency_code: str
    currency_name: str
    base_currency: str
    current_price: float
    target_price: Optional[float]
    drop_alert_enabled: bool
    time_to_buy: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DropAlertResponseSchema(BaseModel):
    id: UUID
    name: str
    current_price: float
    target_price: float
    time_to_buy: bool
    gap_percentage: float


class AccountSchema(BaseModel):
    account_name: str
    is_investment_account: Optional[bool] = False
    is_payroll_account: Optional[bool] = False
    total_invested: Optional[float] = None
    monthly_salary: Optional[float] = None
    checking_account_balance: Optional[float] = None
    default_currency: Optional[str] = "BRL"


class AccountResponseSchema(AccountSchema):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DividendSchema(BaseModel):
    asset_id: UUID
    dividend_amount: float
    dividend_type: str
    ex_dividend_date: datetime
    payment_date: datetime


class DividendResponseSchema(DividendSchema):
    id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True


class PredictionResponseSchema(BaseModel):
    id: UUID
    asset_id: Optional[UUID]
    prediction_type: str
    predicted_price: Optional[float]
    confidence_score: float
    prediction_date: datetime
    analysis_summary: Optional[str]
    
    class Config:
        from_attributes = True


class HealthResponseSchema(BaseModel):
    status: str
    app_name: str
    environment: str
    version: str


class ApiResponseSchema(BaseModel):
    success: bool
    data: Optional[Union[dict, List]] = None
    message: str
    error: Optional[str] = None
