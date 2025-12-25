# MAGFI Project Structure & File Organization

## 📁 Complete Directory Tree

```
magfi/
│
├── 📄 README.md                    # Main project documentation
├── 📄 QUICKSTART.md                # 5-minute setup guide
├── 📄 ANALYSIS.md                  # Deep financial/architecture analysis
├── 📄 API_REFERENCE.md             # Complete API endpoints documentation
├── 📄 .env.example                 # Environment variables template
├── 📄 .gitignore                   # Git ignore patterns
├── 📄 docker-compose.yml           # Multi-service orchestration
│
├── 📂 magfi-core/                  # MAIN API (Asset/Currency Management)
│   ├── 📄 README.md
│   ├── 📄 requirements.txt
│   ├── 📄 .env.example
│   ├── 📄 .gitignore
│   ├── 📄 Dockerfile
│   ├── 📄 docker-compose.yml
│   │
│   ├── 📂 app/                     # Application code
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI application initialization
│   │   ├── config.py               # Settings management
│   │   ├── database.py             # SQLAlchemy setup
│   │   ├── models.py               # ORM models
│   │   ├── schemas.py              # Pydantic schemas
│   │   │
│   │   ├── 📂 routes/              # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── health.py           # GET /health
│   │   │   ├── config.py           # GET/PUT /config
│   │   │   ├── asset.py            # Asset CRUD + alerts
│   │   │   ├── currency.py         # Currency CRUD
│   │   │   ├── market.py           # Drop alerts + predictions
│   │   │   └── account.py          # Account & dividend tracking
│   │   │
│   │   └── 📂 services/            # Business logic layer
│   │       ├── __init__.py
│   │       ├── config_service.py
│   │       ├── asset_service.py    # Asset logic + alerts
│   │       ├── currency_service.py
│   │       ├── account_service.py
│   │       └── prediction_service.py # Integration with magfi-predictor
│   │
│   └── 📂 ddl/                     # Database schemas
│       ├── 01_config.sql
│       ├── 02_asset.sql
│       ├── 03_currency.sql
│       ├── 04_account.sql
│       └── 05_analytics.sql
│
├── 📂 magfi-ingestor/              # News Collection & AI Analysis
│   ├── 📄 README.md
│   ├── 📄 requirements.txt
│   ├── 📄 .env.example
│   ├── 📄 .gitignore
│   ├── 📄 Dockerfile
│   ├── 📄 docker-compose.yml
│   │
│   ├── 📂 app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   │
│   │   ├── 📂 routes/
│   │   │   ├── __init__.py
│   │   │   ├── health.py
│   │   │   └── ingest.py           # POST /ingest/news + GET news endpoints
│   │   │
│   │   └── 📂 services/
│   │       ├── __init__.py
│   │       ├── rss_collector.py    # RSS feed collection
│   │       ├── news_service.py     # News data persistence
│   │       └── ai_analyzer.py      # OpenAI/Gemini sentiment analysis
│   │
│   └── 📂 ddl/
│       ├── 01_news_raw.sql         # stg_news_raw table
│       └── 02_news_analysis.sql    # fct_news_analysis table
│
└── 📂 magfi-predictor/             # Market Prediction Engine
    ├── 📄 README.md
    ├── 📄 requirements.txt
    ├── 📄 .env.example
    ├── 📄 .gitignore
    ├── 📄 Dockerfile
    ├── 📄 docker-compose.yml
    │
    ├── 📂 app/
    │   ├── __init__.py
    │   ├── main.py
    │   ├── config.py
    │   ├── database.py
    │   ├── models.py
    │   ├── schemas.py
    │   │
    │   ├── 📂 routes/
    │   │   ├── __init__.py
    │   │   ├── health.py
    │   │   └── predict.py          # GET /predict + /predict/{ticker}
    │   │
    │   └── 📂 services/
    │       ├── __init__.py
    │       ├── data_fetcher.py     # Fetch from magfi-core & ingestor
    │       └── prediction_service.py # ML prediction logic
    │
    └── 📂 ddl/
        └── 01_prediction.sql       # fct_prediction table
```

---

## 📊 Service Responsibilities

### magfi-core (Port 8000) - Main API
**Responsibility:** Single source of truth for financial data

**Provides:**
- Asset CRUD operations
- Currency CRUD operations
- Configuration management
- Drop price alerts
- Portfolio/account tracking
- Dividend monitoring
- Integration bridge to other services

**Works independently:** ✅ Yes
**Database Tables:** dim_config, dim_asset, dim_currency, dim_account, fct_*

---

### magfi-ingestor (Port 8001) - News Processing
**Responsibility:** Collect, analyze, and store financial news

**Provides:**
- RSS feed collection from financial sources
- AI-powered sentiment analysis (OpenAI/Gemini)
- Impact scoring for market relevance
- Asset ticker extraction
- Raw news storage → Processed analysis

**Works independently:** ❌ No (optional dependency for magfi-core)
**Database Tables:** stg_news_raw, fct_news_analysis

---

### magfi-predictor (Port 8002) - ML Predictions
**Responsibility:** Generate market predictions from data

**Provides:**
- Asset price predictions
- Confidence scoring
- Sentiment-based forecasts
- Horizon-based predictions (1-week, 1-month, etc.)
- Integration with news analysis data

**Works independently:** ❌ No (optional dependency for magfi-core)
**Database Tables:** fct_prediction

---

## 🗄️ Database Schema Overview

### Dimensional Tables (Slow-Changing)
```
dim_config
├─ id (UUID, PK)
├─ config_name (VARCHAR, UNIQUE)
└─ config_value (TEXT)

dim_asset
├─ id (UUID, PK)
├─ ticker_symbol (VARCHAR, UNIQUE, INDEX)
├─ current_price (NUMERIC)
├─ target_price (NUMERIC)
├─ drop_alert_enabled (BOOLEAN, INDEX)
├─ pl_ratio (FLOAT)
└─ pvpa_ratio (FLOAT)

dim_currency
├─ id (UUID, PK)
├─ currency_code (VARCHAR, UNIQUE, INDEX)
├─ current_price (NUMERIC)
├─ target_price (NUMERIC)
└─ drop_alert_enabled (BOOLEAN, INDEX)

dim_account
├─ id (UUID, PK)
├─ account_name (VARCHAR)
├─ is_investment_account (BOOLEAN)
├─ total_invested (NUMERIC)
└─ default_currency (VARCHAR)
```

### Fact Tables (Fast-Changing)
```
fct_asset_price_history
├─ id (UUID, PK)
├─ asset_id (UUID, FK → dim_asset)
├─ price (NUMERIC)
└─ recorded_at (TIMESTAMP, INDEX)

fct_currency_price_history
├─ id (UUID, PK)
├─ currency_id (UUID, FK → dim_currency)
├─ price (NUMERIC)
└─ recorded_at (TIMESTAMP, INDEX)

fct_portfolio_position
├─ id (UUID, PK)
├─ account_id (UUID, FK → dim_account)
├─ asset_id (UUID, FK → dim_asset)
├─ quantity (NUMERIC)
└─ average_cost (NUMERIC)

fct_dividend
├─ id (UUID, PK)
├─ asset_id (UUID, FK → dim_asset)
├─ dividend_amount (NUMERIC)
├─ ex_dividend_date (TIMESTAMP)
└─ payment_date (TIMESTAMP, INDEX)

fct_news_analysis (magfi-ingestor)
├─ id (UUID, PK)
├─ asset_ticker (VARCHAR, INDEX)
├─ sentiment (VARCHAR)
├─ impact_score (FLOAT)
└─ ai_analysis (TEXT)

fct_prediction (magfi-predictor)
├─ id (UUID, PK)
├─ asset_ticker (VARCHAR, INDEX)
├─ predicted_price (FLOAT)
├─ confidence_score (FLOAT)
└─ prediction_date (TIMESTAMP, INDEX)

stg_news_raw (magfi-ingestor - Staging)
├─ id (UUID, PK)
├─ feed_source (VARCHAR, INDEX)
├─ title (VARCHAR)
├─ content (TEXT)
└─ is_processed (BOOLEAN, INDEX)
```

---

## 🔄 Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      User/Client                             │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP Requests
                         ▼
            ┌────────────────────────────┐
            │    magfi-core:8000         │
            │   (Main API Gateway)       │
            └────────┬───────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
    [Internal]  [Fetch from]  [Call to]
    Operations  magfi-ingestor magfi-predictor
        │            │            │
        │            ├─→ fct_news_analysis
        │            └─→ fct_news_raw
        │
        └─→ dim_config
        └─→ dim_asset
        └─→ dim_currency
        └─→ dim_account
        └─→ fct_*

       magfi-ingestor:8001
       ├─→ RSS Feeds
       ├─→ stg_news_raw (raw data)
       └─→ fct_news_analysis (AI processed)

       magfi-predictor:8002
       ├─→ Fetch from magfi-core
       ├─→ Fetch from magfi-ingestor
       └─→ fct_prediction (ML outputs)

       PostgreSQL (Supabase)
       └─→ All tables above
```

---

## 📝 Key Files to Know

### Configuration
- **`.env.example`** - Template for all environment variables
- **`app/config.py`** - Pydantic settings loader

### Database
- **`ddl/`** - SQL files (CREATE TABLE statements)
- **`app/models.py`** - SQLAlchemy ORM models

### API Routes
- **`routes/health.py`** - Service health checks
- **`routes/asset.py`** - Asset CRUD endpoints
- **`routes/currency.py`** - Currency CRUD endpoints
- **`routes/market.py`** - Alerts and predictions
- **`routes/account.py`** - Portfolio management

### Business Logic
- **`services/asset_service.py`** - Asset operations + drop alert logic
- **`services/currency_service.py`** - Currency operations
- **`services/prediction_service.py`** - Integration with magfi-predictor
- **`services/news_service.py`** - News data management
- **`services/ai_analyzer.py`** - OpenAI/Gemini integration

### Deployment
- **`Dockerfile`** - Docker image definition
- **`docker-compose.yml`** - Multi-service orchestration
- **`requirements.txt`** - Python dependencies

---

## 🚀 Deployment Workflow

### Development
```bash
# Each service in separate terminal
cd magfi-core && uvicorn app.main:app --reload --port 8000
cd magfi-ingestor && uvicorn app.main:app --reload --port 8001
cd magfi-predictor && uvicorn app.main:app --reload --port 8002
```

### Production (Docker)
```bash
# From root directory
docker-compose up --build

# Services automatically start with:
# - PostgreSQL initialization (ddl/* files)
# - All environment variables configured
# - Health checks enabled
# - Logging to stdout
```

### Cloud Deployment (Supabase + Cloud Run)
```bash
# Push to cloud registry
docker build -t gcr.io/project-id/magfi-core ./magfi-core
docker push gcr.io/project-id/magfi-core

# Deploy to Cloud Run
gcloud run deploy magfi-core --image gcr.io/project-id/magfi-core
```

---

## 💾 Environment Variables

Each service has `.env.example` with required variables:

### magfi-core
```
DATABASE_URL=postgresql://...
SUPABASE_URL=...
MAGFI_INGESTOR_URL=http://magfi-ingestor:8001
MAGFI_PREDICTOR_URL=http://magfi-predictor:8002
```

### magfi-ingestor
```
DATABASE_URL=postgresql://...
RSS_FEEDS=url1,url2,url3
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
```

### magfi-predictor
```
DATABASE_URL=postgresql://...
MAGFI_CORE_URL=http://magfi-core:8000
MAGFI_INGESTOR_URL=http://magfi-ingestor:8001
```

---

## 📖 Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Project overview + setup |
| `QUICKSTART.md` | 5-minute getting started guide |
| `ANALYSIS.md` | Deep financial/architecture analysis |
| `API_REFERENCE.md` | Complete endpoint documentation |
| `magfi-core/README.md` | Core service details |
| `magfi-ingestor/README.md` | Ingestor service details |
| `magfi-predictor/README.md` | Predictor service details |

---

## 🎯 Quick Reference

### Start Services
```bash
docker-compose up --build                    # All services
cd magfi-core && docker-compose up --build   # Single service
```

### Check Health
```bash
curl http://localhost:8000/health            # Core
curl http://localhost:8001/health            # Ingestor
curl http://localhost:8002/health            # Predictor
```

### Create Test Data
```bash
curl -X POST http://localhost:8000/market/asset \
  -H "Content-Type: application/json" \
  -d '{"name":"AAPL","current_price":273.67,"drop_alert":true}'
```

### View API Docs
```
http://localhost:8000/docs                   # Core Swagger
http://localhost:8001/docs                   # Ingestor Swagger
http://localhost:8002/docs                   # Predictor Swagger
```

### Database Connection
```bash
psql -U magfi_user -d magfi_db -h localhost
```

---

## 🔒 Security Notes

- ✅ Never commit `.env` files (use `.env.example`)
- ✅ Use strong passwords in production
- ✅ Enable HTTPS in production deployment
- ✅ Restrict CORS origins in production
- ✅ Validate all user inputs (Pydantic handles this)
- ✅ Use environment variables for secrets (not hardcoded)
- ✅ Implement JWT authentication (optional enhancement)

---

## 📈 Scalability Considerations

- **Database**: Use Supabase managed PostgreSQL
- **Async I/O**: All services use async/await
- **Indexing**: Strategic indices on filtered columns
- **Pagination**: Implement on list endpoints
- **Caching**: Redis for hot data (future enhancement)
- **Load Balancing**: Deploy multiple instances behind load balancer
- **Monitoring**: Set up CloudWatch/Stackdriver alerts

---

## 🤝 Contributing Guidelines

1. **Code Style**: Follow PEP 8 (Black formatter)
2. **Type Hints**: All functions must have type hints
3. **Comments**: Only when necessary, keep concise
4. **Tests**: Write tests for new features
5. **Commits**: Clear, atomic commits
6. **Branches**: feature/*, bugfix/*, docs/* naming

---

## 📞 Support & Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com
- **SQLAlchemy**: https://docs.sqlalchemy.org
- **PostgreSQL**: https://www.postgresql.org/docs
- **Supabase**: https://supabase.com/docs
- **Docker**: https://docs.docker.com

---

**Last Updated:** 2025-12-25
**Version:** 1.0.0
**License:** MIT
