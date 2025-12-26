# MAGFI - Complete Documentation Index

## 📚 Documentation Map

### 🚀 Getting Started (Start Here!)

1. **[QUICKSTART.md](./QUICKSTART.md)** ⭐ START HERE

   - 5-minute Docker setup
   - First API calls examples
   - Common workflows
   - Troubleshooting

2. **[README.md](./README.md)**
   - Project overview
   - Architecture diagram
   - Technology stack
   - Development setup

### 🏗️ Architecture & Analysis

3. **[PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md)**

   - Complete directory tree
   - Service responsibilities
   - Database schema overview
   - Data flow diagrams

4. **[ANALYSIS.md](./ANALYSIS.md)**
   - Deep financial analysis
   - JSON structure insights
   - Database design decisions
   - Alert logic implementation
   - Multi-service architecture

### 📖 API Documentation

5. **[API_REFERENCE.md](./API_REFERENCE.md)** (Most Detailed)
   - All endpoints documented
   - Request/response examples
   - Query parameters explained
   - Error handling
   - Testing examples

### 🔧 Service-Specific Documentation

6. **[magfi-core/README.md](./magfi-core/README.md)**

   - Core API features
   - Local setup instructions
   - Docker commands
   - Features list

7. **[magfi-ingestor/README.md](./magfi-ingestor/README.md)**

   - News ingestion details
   - AI analysis features
   - Setup instructions

8. **[magfi-predictor/README.md](./magfi-predictor/README.md)**
   - Prediction engine details
   - ML features
   - Setup instructions

---

## 🎯 Quick Navigation by Use Case

### "I want to start using MAGFI right now"

→ Read: **QUICKSTART.md** (5 min)

### "I need to understand the system architecture"

→ Read: **PROJECT_STRUCTURE.md** (15 min)

### "I want complete API documentation"

→ Read: **API_REFERENCE.md** (detailed reference)

### "I need to understand the financial logic"

→ Read: **ANALYSIS.md** (30 min)

### "I'm deploying to production"

→ Read: **README.md** + check docker-compose.yml

### "I'm developing a feature"

→ Read: **PROJECT_STRUCTURE.md** (find the file) + relevant service README

---

## 📋 Key Concepts

### Three Microservices

| Service             | Port | Purpose                     | Independent? |
| ------------------- | ---- | --------------------------- | ------------ |
| **magfi-core**      | 8100 | Asset/Currency management   | ✅ Yes       |
| **magfi-ingestor**  | 8200 | News collection & sentiment | ❌ Optional  |
| **magfi-predictor** | 8300 | ML market predictions       | ❌ Optional  |

### Database Tables (30 total)

**Core (magfi-core):**

- `dim_config`, `dim_asset`, `dim_currency`, `dim_account`
- `fct_asset_price_history`, `fct_currency_price_history`, `fct_portfolio_position`, `fct_dividend`

**News (magfi-ingestor):**

- `stg_news_raw`, `fct_news_analysis`

**Predictions (magfi-predictor):**

- `fct_prediction`

### Main Endpoints (23 total)

**Asset Management:** POST, GET, PUT, DELETE /market/asset(s)
**Currency Management:** POST, GET, PUT, DELETE /market/currency(ies)
**Alerts:** GET /market/drop-alert/assets, /currencies
**Portfolio:** GET /market/accounts, /dividend-gains, POST /market/account
**Analysis:** GET /market/report/prediction
**News:** POST /ingest/news, GET /ingest/news/{raw,analyzed}
**Predictions:** GET /predict, /predict/{ticker}

---

## �� File References

### Configuration Files

- [`.env.example`](./.env.example) - Environment template (root)
- [`magfi-core/.env.example`](./magfi-core/.env.example) - Core service config
- [`magfi-ingestor/.env.example`](./magfi-ingestor/.env.example) - Ingestor config
- [`magfi-predictor/.env.example`](./magfi-predictor/.env.example) - Predictor config

### Docker Files

- [`docker-compose.yml`](./docker-compose.yml) - Root orchestration
- [`magfi-core/docker-compose.yml`](./magfi-core/docker-compose.yml) - Individual service
- [`magfi-core/Dockerfile`](./magfi-core/Dockerfile) - Image definition

### Database DDL

- [`magfi-core/ddl/`](./magfi-core/ddl/) - 5 SQL schema files
- [`magfi-ingestor/ddl/`](./magfi-ingestor/ddl/) - 2 SQL schema files
- [`magfi-predictor/ddl/`](./magfi-predictor/ddl/) - 1 SQL schema file

### Application Code

#### magfi-core

- Routes: [`asset.py`](./magfi-core/app/routes/asset.py), [`currency.py`](./magfi-core/app/routes/currency.py), [`market.py`](./magfi-core/app/routes/market.py), [`config.py`](./magfi-core/app/routes/config.py), [`account.py`](./magfi-core/app/routes/account.py)
- Services: [`asset_service.py`](./magfi-core/app/services/asset_service.py), [`currency_service.py`](./magfi-core/app/services/currency_service.py), etc.

#### magfi-ingestor

- Routes: [`ingest.py`](./magfi-ingestor/app/routes/ingest.py)
- Services: [`rss_collector.py`](./magfi-ingestor/app/services/rss_collector.py), [`ai_analyzer.py`](./magfi-ingestor/app/services/ai_analyzer.py)

#### magfi-predictor

- Routes: [`predict.py`](./magfi-predictor/app/routes/predict.py)
- Services: [`data_fetcher.py`](./magfi-predictor/app/services/data_fetcher.py), [`prediction_service.py`](./magfi-predictor/app/services/prediction_service.py)

---

## 💡 Common Tasks

### Task: Create an Asset

```bash
# Read: API_REFERENCE.md → POST /market/asset section
curl -X POST http://localhost:8100/market/asset \
  -H "Content-Type: application/json" \
  -d '{"name":"AAPL","current_price":273.67,"drop_alert":true}'
```

### Task: Check Drop Alerts

```bash
# Read: API_REFERENCE.md → GET /market/drop-alert/assets
curl http://localhost:8100/market/drop-alert/assets
```

### Task: Ingest News

```bash
# Read: API_REFERENCE.md → POST /ingest/news
curl -X POST http://localhost:8200/ingest/news
```

### Task: Get Predictions

```bash
# Read: API_REFERENCE.md → GET /predict
curl http://localhost:8300/predict
```

### Task: Setup Locally

```bash
# Read: QUICKSTART.md → Local Development section
cd magfi-core
python3.14 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Task: Deploy to Production

```bash
# Read: docker-compose.yml + README.md deployment section
docker-compose up --build
```

---

## 🔍 Search by Topic

### Price Alerts

→ [ANALYSIS.md - Drop Alert Algorithm](./ANALYSIS.md#drop-alert-algorithm)
→ [API_REFERENCE.md - GET /market/drop-alert/assets](./API_REFERENCE.md)
→ [magfi-core/app/services/asset_service.py](./magfi-core/app/services/asset_service.py)

### Financial Indicators (P/L, P/VPA)

→ [ANALYSIS.md - Financial Sector Comparison](./ANALYSIS.md#financial-sector-comparison-strategy)
→ [magfi-core/app/models.py - Asset model](./magfi-core/app/models.py)

### Multi-Currency

→ [ANALYSIS.md - Multi-Currency Conversion](./ANALYSIS.md#3-multi-currency-conversion)
→ [API_REFERENCE.md - Currency endpoints](./API_REFERENCE.md#currency-management)

### AI Predictions

→ [magfi-predictor/app/services/prediction_service.py](./magfi-predictor/app/services/prediction_service.py)
→ [API_REFERENCE.md - GET /predict](./API_REFERENCE.md)

### News Sentiment

→ [magfi-ingestor/app/services/ai_analyzer.py](./magfi-ingestor/app/services/ai_analyzer.py)
→ [API_REFERENCE.md - POST /ingest/news](./API_REFERENCE.md)

### Database Schema

→ [PROJECT_STRUCTURE.md - Database Schema Overview](./PROJECT_STRUCTURE.md#-database-schema-overview)
→ [`magfi-core/ddl/` files](./magfi-core/ddl/)

---

## 🚀 Recommended Reading Order

**For Users (Just want to use it):**

1. QUICKSTART.md (5 min)
2. API_REFERENCE.md (reference as needed)

**For Developers (Want to extend it):**

1. QUICKSTART.md (5 min)
2. PROJECT_STRUCTURE.md (15 min)
3. Relevant service README
4. API_REFERENCE.md (detailed reference)
5. Code in appropriate service

**For Architects (Understanding everything):**

1. README.md (overview)
2. ANALYSIS.md (30 min deep dive)
3. PROJECT_STRUCTURE.md (architecture)
4. API_REFERENCE.md (endpoints)
5. Individual service READMEs
6. Source code review

---

## 📊 Statistics

| Metric              | Value   |
| ------------------- | ------- |
| Total Services      | 3       |
| Python Files        | 55+     |
| SQL Files           | 8       |
| API Endpoints       | 23      |
| Database Tables     | 30+     |
| Documentation Files | 7       |
| Code Lines          | ~4,000+ |

---

## 🔗 External Resources

- **FastAPI**: https://fastapi.tiangolo.com/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **Supabase**: https://supabase.com/docs/
- **PostgreSQL**: https://www.postgresql.org/docs/
- **Docker**: https://docs.docker.com/

---

## 📝 Document Versions

| Document             | Last Updated | Status      |
| -------------------- | ------------ | ----------- |
| QUICKSTART.md        | 2025-12-25   | ✅ Complete |
| README.md            | 2025-12-25   | ✅ Complete |
| API_REFERENCE.md     | 2025-12-25   | ✅ Complete |
| ANALYSIS.md          | 2025-12-25   | ✅ Complete |
| PROJECT_STRUCTURE.md | 2025-12-25   | ✅ Complete |
| Individual READMEs   | 2025-12-25   | ✅ Complete |

---

## 🎯 Next Steps

1. **Start Here**: Open [QUICKSTART.md](./QUICKSTART.md)
2. **Setup**: Follow 5-minute Docker setup
3. **Explore**: Try first API calls
4. **Learn**: Read relevant documentation
5. **Build**: Extend with custom features

---

**Happy coding! 🚀**

_MAGFI - Manage Assets and Get Financial Insights_
