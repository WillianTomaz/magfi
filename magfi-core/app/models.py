from sqlalchemy import Column, String, Float, DateTime, Boolean, Integer, UUID, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
import uuid
from datetime import datetime
from app.database import Base


class Config(Base):
    __tablename__ = "dim_config"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    config_name = Column(String(255), unique=True, nullable=False, index=True)
    config_value = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Asset(Base):
    __tablename__ = "dim_asset"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticker_symbol = Column(String(20), unique=True, nullable=False, index=True)
    asset_name = Column(String(255), nullable=False)
    currency_code = Column(String(3), nullable=False)
    current_price = Column(Numeric(15, 4), nullable=False)
    target_price = Column(Numeric(15, 4), nullable=True)
    drop_alert_enabled = Column(Boolean, default=False)
    target_gap_percentage = Column(Float, nullable=True)
    time_to_buy = Column(Boolean, default=False)
    sector = Column(String(100), nullable=True)
    pl_ratio = Column(Float, nullable=True)
    pvpa_ratio = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    price_history = relationship("AssetPriceHistory", back_populates="asset", cascade="all, delete-orphan")


class AssetPriceHistory(Base):
    __tablename__ = "fct_asset_price_history"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("dim_asset.id"), nullable=False)
    price = Column(Numeric(15, 4), nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow)
    
    asset = relationship("Asset", back_populates="price_history")


class Currency(Base):
    __tablename__ = "dim_currency"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    currency_code = Column(String(3), unique=True, nullable=False, index=True)
    currency_name = Column(String(100), nullable=False)
    base_currency = Column(String(3), nullable=False, default="BRL")
    current_price = Column(Numeric(15, 4), nullable=False)
    target_price = Column(Numeric(15, 4), nullable=True)
    drop_alert_enabled = Column(Boolean, default=False)
    time_to_buy = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    price_history = relationship("CurrencyPriceHistory", back_populates="currency", cascade="all, delete-orphan")


class CurrencyPriceHistory(Base):
    __tablename__ = "fct_currency_price_history"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    currency_id = Column(UUID(as_uuid=True), ForeignKey("dim_currency.id"), nullable=False)
    price = Column(Numeric(15, 4), nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow)
    
    currency = relationship("Currency", back_populates="price_history")


class Account(Base):
    __tablename__ = "dim_account"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_name = Column(String(255), nullable=False)
    is_investment_account = Column(Boolean, default=False)
    is_payroll_account = Column(Boolean, default=False)
    total_invested = Column(Numeric(15, 4), nullable=True)
    monthly_salary = Column(Numeric(15, 4), nullable=True)
    checking_account_balance = Column(Numeric(15, 4), nullable=True)
    default_currency = Column(String(3), nullable=False, default="BRL")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    portfolio = relationship("PortfolioPosition", back_populates="account", cascade="all, delete-orphan")


class PortfolioPosition(Base):
    __tablename__ = "fct_portfolio_position"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True), ForeignKey("dim_account.id"), nullable=False)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("dim_asset.id"), nullable=False)
    quantity = Column(Numeric(20, 8), nullable=False)
    average_cost = Column(Numeric(15, 4), nullable=False)
    acquisition_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    account = relationship("Account", back_populates="portfolio")


class Dividend(Base):
    __tablename__ = "fct_dividend"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("dim_asset.id"), nullable=False)
    dividend_amount = Column(Numeric(15, 4), nullable=False)
    dividend_type = Column(String(50), nullable=False)
    ex_dividend_date = Column(DateTime, nullable=False)
    payment_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class NewsAnalysis(Base):
    __tablename__ = "fct_news_analysis"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("dim_asset.id"), nullable=True)
    news_title = Column(String, nullable=False)
    news_content = Column(String, nullable=False)
    sentiment = Column(String(20), nullable=False)
    impact_score = Column(Float, nullable=False)
    ai_analysis = Column(String, nullable=True)
    source_url = Column(String, nullable=True)
    analyzed_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)


class Prediction(Base):
    __tablename__ = "fct_prediction"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("dim_asset.id"), nullable=True)
    prediction_type = Column(String(50), nullable=False)
    predicted_price = Column(Numeric(15, 4), nullable=True)
    confidence_score = Column(Float, nullable=False)
    prediction_date = Column(DateTime, nullable=False)
    analysis_summary = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
