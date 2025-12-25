# MAGFI - Manage Assets and Get Financial Insights

Complete financial management and market analysis platform consisting of three integrated microservices.

## Architecture Overview

```
┌─────────────────┐
│   magfi-core    │  Core API - Asset/Currency management, alerts, reports
│   (port 8000)   │
└────────┬────────┘
         │
    ┌────┴────┐
    │          │
┌───▼──────┐  ┌─▼────────────┐
│magfi-     │  │magfi-        │
│ingestor   │  │predictor     │
│(8001)     │  │(8002)        │
└──────────┘  └──────────────┘

All connected to Supabase PostgreSQL
```

## Project Structure

```
magfi/
├── magfi-core/          # Main API (asset, currency, config management)
│   ├── app/
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── routes/
│   │   └── services/
│   ├── ddl/             # Database schemas
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── requirements.txt
│
├── magfi-ingestor/      # News collection & sentiment analysis
│   ├── app/
│   ├── ddl/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── magfi-predictor/     # AI market predictions
│   ├── app/
│   ├── ddl/
│   ├── Dockerfile
│   └── docker-compose.yml
│
└── docker-compose.yml   # Multi-service orchestration
```

## Quick Start

### 1. Clone & Setup

```bash
git clone <repository>
cd magfi
```

### 2. Environment Configuration

Copy environment templates and configure:

```bash
cp magfi-core/.env.example magfi-core/.env
cp magfi-ingestor/.env.example magfi-ingestor/.env
cp magfi-predictor/.env.example magfi-predictor/.env
```

Update with your Supabase credentials and API keys:
- SUPABASE_URL, SUPABASE_KEY
- OPENAI_API_KEY or GEMINI_API_KEY
- RSS feed URLs (for magfi-ingestor)

### 3. Docker Deployment

```bash
# Start all services
docker-compose up --build

# Or start individual services
cd magfi-core && docker-compose up --build
cd magfi-ingestor && docker-compose up --build
cd magfi-predictor && docker-compose up --build
```

### 4. Verify Services

```bash
# Health checks
curl http://localhost:8000/health
curl http://localhost:8001/health
curl http://localhost:8002/health

# API Documentation
- magfi-core: http://localhost:8000/docs
- magfi-ingestor: http://localhost:8001/docs
- magfi-predictor: http://localhost:8002/docs
```

## Local Development

### Setup Virtual Environment

```bash
# magfi-core
cd magfi-core
python3.14 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# magfi-ingestor
cd ../magfi-ingestor
python3.14 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# magfi-predictor
cd ../magfi-predictor
python3.14 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run Locally

```bash
# Terminal 1: magfi-core
cd magfi-core
source venv/bin/activate
uvicorn app.main:app --reload --port 8000

# Terminal 2: magfi-ingestor
cd magfi-ingestor
source venv/bin/activate
uvicorn app.main:app --reload --port 8001

# Terminal 3: magfi-predictor
cd magfi-predictor
source venv/bin/activate
uvicorn app.main:app --reload --port 8002
```

## Database Setup

The DDL files are automatically executed when using Docker. For manual setup:

```bash
# magfi-core tables
psql -U magfi_user -d magfi_db -f magfi-core/ddl/01_config.sql
psql -U magfi_user -d magfi_db -f magfi-core/ddl/02_asset.sql
psql -U magfi_user -d magfi_db -f magfi-core/ddl/03_currency.sql
psql -U magfi_user -d magfi_db -f magfi-core/ddl/04_account.sql
psql -U magfi_user -d magfi_db -f magfi-core/ddl/05_analytics.sql

# magfi-ingestor tables
psql -U magfi_user -d magfi_db -f magfi-ingestor/ddl/01_news_raw.sql
psql -U magfi_user -d magfi_db -f magfi-ingestor/ddl/02_news_analysis.sql

# magfi-predictor tables
psql -U magfi_user -d magfi_db -f magfi-predictor/ddl/01_prediction.sql
```

## Core API Endpoints

### Health & Config
- `GET /health` - Service health
- `GET /config` - All configurations
- `GET /config/?configName=last-update` - Specific config
- `PUT /config` - Update configuration

### Assets
- `POST /market/asset` - Create asset
- `GET /market/assets` - List all assets
- `GET /market/asset/?tickerSymbol=AAPL` - Get specific asset
- `PUT /market/asset/?tickerSymbol=AAPL` - Update asset
- `DELETE /market/asset/?tickerSymbol=AAPL` - Delete asset

### Currencies
- `POST /market/currency` - Create currency
- `GET /market/currencies` - List all currencies
- `GET /market/currency/?currencyCode=USD` - Get specific currency
- `PUT /market/currency/?currencyCode=USD` - Update currency
- `DELETE /market/currency/?currencyCode=USD` - Delete currency

### Alerts & Analysis
- `GET /market/drop-alert/assets` - Assets ready to buy
- `GET /market/drop-alert/currencies` - Currencies ready to buy
- `GET /market/report/prediction` - Market predictions

### Accounts & Dividends
- `POST /market/account` - Create account
- `GET /market/accounts` - List accounts
- `GET /market/dividend-gains` - Dividend tracking

## Request/Response Format

### Success Response
```json
{
  "success": true,
  "data": {...},
  "message": "Operation description"
}
```

### Error Response
```json
{
  "success": false,
  "error": "error_code",
  "message": "Error description"
}
```

## Example Workflows

### 1. Monitor Asset Price
```bash
# Create asset
curl -X POST http://localhost:8000/market/asset \
  -H "Content-Type: application/json" \
  -d '{
    "name": "AAPL",
    "currency_code": "USD",
    "current_price": 273.67,
    "target_price": 270.00,
    "drop_alert": true
  }'

# Check if price target met
curl http://localhost:8000/market/drop-alert/assets

# Get market prediction
curl http://localhost:8000/market/report/prediction
```

### 2. Ingest Financial News
```bash
# Manually trigger news ingestion
curl -X POST http://localhost:8001/ingest/news

# View processed analysis
curl http://localhost:8001/ingest/news/analyzed
```

### 3. Get Price Predictions
```bash
# General market prediction
curl http://localhost:8002/predict

# Asset-specific prediction
curl http://localhost:8002/predict/AAPL
```

## Technologies

- **Python 3.14** - Core language
- **FastAPI** - Web framework
- **SQLAlchemy** - ORM
- **PostgreSQL + Supabase** - Database
- **OpenAI/Gemini** - AI analysis
- **Feedparser** - RSS feeds
- **Pandas/NumPy** - Data processing
- **Docker** - Containerization

## Contributing

1. Follow PEP 8 guidelines
2. Use type hints
3. Keep code concise, add comments only when necessary
4. Test changes before submitting

## License

MIT

## Support

For issues, check individual service READMEs:
- `magfi-core/README.md`
- `magfi-ingestor/README.md`
- `magfi-predictor/README.md`
