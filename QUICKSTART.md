# MAGFI - Quick Start Guide

## 🚀 Fast Setup (5 minutes with Docker)

### Prerequisites

- Docker & Docker Compose installed
- Supabase account (free tier: supabase.com)
- OpenAI or Gemini API key (optional for news analysis)

### Step 1: Clone & Configure

```bash
git clone <your-repo-url> magfi
cd magfi

# Copy environment template
cp .env.example .env

# Edit .env with your credentials
nano .env
# Fill in:
# - SUPABASE_URL: From Supabase project settings
# - SUPABASE_KEY: From Supabase project API settings
# - OPENAI_API_KEY: From OpenAI dashboard (optional)
# - GEMINI_API_KEY: From Google Cloud (optional)
```

### Step 2: Run Docker Compose

```bash
# Start all 3 services + PostgreSQL
docker-compose up --build

# Wait for all services to be ready (30-60 seconds)
# You'll see "Uvicorn running on http://0.0.0.0:PORT"
```

### Step 3: Verify Services

```bash
# In another terminal
curl http://localhost:8100/health
curl http://localhost:8200/health
curl http://localhost:8300/health

# All should return:
# {"status":"healthy","app_name":"magfi-core|ingestor|predictor","environment":"development"}
```

### Step 4: Access APIs

- **magfi-core** (main API): http://localhost:8100/docs
- **magfi-ingestor** (news): http://localhost:8200/docs
- **magfi-predictor** (predictions): http://localhost:8300/docs

---

## 📝 First Steps - Create Your First Asset

### Using cURL

```bash
# 1. Create an asset
curl -X POST http://localhost:8100/market/asset \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Petroleo Brasileiro SA Petrobras Preference Shares",
    "ticker_symbol": "PETR4",
    "currency_code": "BRL",
    "current_price": 30.31
  }'

# Response:
# {
#   "success": true,
#   "data": {"id": "...", "ticker_symbol": "AAPL", "asset_name": "AAPL"},
#   "message": "Asset created successfully"
# }
```

### Using Swagger UI

1. Go to http://localhost:8100/docs
2. Click "Try it out" on POST /market/asset
3. Paste this JSON:

```json
{
  "name": "PETR4",
  "currency_code": "BRL",
  "current_price": 31.01,
  "target_price": 29.0,
  "drop_alert": true,
  "sector": "Energy"
}
```

4. Click "Execute"

---

## 🔔 Common Workflows

### Workflow 1: Monitor Stock Price

```bash
# Create asset with target price
curl -X POST http://localhost:8100/market/asset \
  -H "Content-Type: application/json" \
  -d '{"name":"IBM","current_price":180,"target_price":175,"drop_alert":true}'

# Check if price target is met (run daily)
curl http://localhost:8100/market/drop-alert/assets

# Response shows assets ready to buy
```

### Workflow 2: Track Currency Exchange

```bash
# Create currency
curl -X POST http://localhost:8100/market/currency \
  -H "Content-Type: application/json" \
  -d '{
    "name": "USD",
    "current_price": 5.54,
    "target_price": 5.00,
    "drop_alert": true
  }'

# Check when USD hits 5.00 BRL
curl http://localhost:8100/market/drop-alert/currencies
```

### Workflow 3: Get AI Predictions

```bash
# Get market predictions (aggregated from all assets + news)
curl http://localhost:8100/market/report/prediction

# Or get specific asset prediction
curl http://localhost:8300/predict/AAPL
```

### Workflow 4: Ingest Financial News

```bash
# Manually trigger news collection
curl -X POST http://localhost:8200/ingest/news

# View analyzed news (AI-processed)
curl http://localhost:8200/ingest/news/analyzed

# View raw news (before AI processing)
curl http://localhost:8200/ingest/news/raw
```

---

## 📊 API Response Format

All responses follow this pattern:

**Success:**

```json
{
  "success": true,
  "data": {
    /* actual data */
  },
  "message": "Description of what happened"
}
```

**Error:**

```json
{
  "success": false,
  "error": "error_code",
  "message": "Why it failed"
}
```

---

## 🔧 Local Development (Without Docker)

### Setup Individual Services

```bash
# Terminal 1: magfi-core
cd magfi-core
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with DATABASE_URL pointing to your local PostgreSQL
uvicorn app.main:app --reload --port 8100

# Terminal 2: magfi-ingestor
cd magfi-ingestor
python3.14 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Configure .env
uvicorn app.main:app --reload --port 8200

# Terminal 3: magfi-predictor
cd magfi-predictor
python3.14 -m venv venv
source venv/activate
pip install -r requirements.txt
cp .env.example .env
# Configure .env
uvicorn app.main:app --reload --port 8300
```

### Setup PostgreSQL Locally

```bash
# Install PostgreSQL (macOS: brew install postgresql, Linux: apt-get install postgresql)
# Start PostgreSQL
psql postgres

# Create database and user
CREATE USER magfi_user WITH PASSWORD 'magfi_password';
CREATE DATABASE magfi_db OWNER magfi_user;

# Run DDL scripts
psql -U magfi_user -d magfi_db -f magfi-core/ddl/01_config.sql
psql -U magfi_user -d magfi_db -f magfi-core/ddl/02_asset.sql
psql -U magfi_user -d magfi_db -f magfi-core/ddl/03_currency.sql
psql -U magfi_user -d magfi_db -f magfi-core/ddl/04_account.sql
psql -U magfi_user -d magfi_db -f magfi-core/ddl/05_analytics.sql
psql -U magfi_user -d magfi_db -f magfi-ingestor/ddl/01_news_raw.sql
psql -U magfi_user -d magfi_db -f magfi-ingestor/ddl/02_news_analysis.sql
psql -U magfi_user -d magfi_db -f magfi-predictor/ddl/01_prediction.sql
```

---

## 🚨 Troubleshooting

### Services Won't Start

**Error:** `Connection refused to database`

- **Fix**: Ensure PostgreSQL is running and DATABASE_URL in .env is correct
- Check: `docker-compose ps` to see service status

**Error:** `Module not found: sqlalchemy`

- **Fix**: `pip install -r requirements.txt` in each service directory

### Port Already in Use

```bash
# Kill process using port 8100
lsof -ti:8100 | xargs kill -9

# Or use different port
uvicorn app.main:app --port 8010
```

### Can't Connect to Services

- Check .env files have correct URLs (http://service:port NOT localhost:port inside Docker)
- Use `docker-compose logs <service>` to see error messages
- Verify all 3 services are running: `docker-compose ps`

---

## 📚 Next Steps

1. **Read ANALYSIS.md** for deep dive into financial logic
2. **Check individual README.md** in each service folder
3. **Explore API docs** at http://localhost:8100/docs (Swagger UI)
4. **Create more assets** and set different targets
5. **Integrate with Supabase** for cloud backup

---

## 💡 Pro Tips

### Tip 1: Monitor Multiple Assets

```bash
# Create portfolio of assets
for ticker in AAPL IBM MSFT; do
  curl -X POST http://localhost:8100/market/asset \
    -H "Content-Type: application/json" \
    -d "{\"name\":\"$ticker\",\"current_price\":100,\"drop_alert\":true}"
done

# Check all at once
curl http://localhost:8100/market/assets
```

### Tip 2: Set Different Base Currencies

```bash
# Create config for different base currency
curl -X PUT http://localhost:8100/config \
  -H "Content-Type: application/json" \
  -d '{"default_currency": "USD"}'
```

### Tip 3: Automate with Cron Job

```bash
# Check alerts every hour
0 * * * * curl http://localhost:8100/market/drop-alert/assets >> /var/log/magfi_alerts.log
```

---

## 📞 Support

- **Issues**: Check logs: `docker-compose logs -f magfi-core`
- **Questions**: Review ANALYSIS.md and endpoint documentation
- **Bugs**: Enable DEBUG=true in .env for verbose logging

---

## 🎓 Learning Resources

- FastAPI Docs: https://fastapi.tiangolo.com
- SQLAlchemy ORM: https://docs.sqlalchemy.org
- PostgreSQL: https://www.postgresql.org/docs
- Supabase Guide: https://supabase.com/docs

Happy investing! 📈
