# MAGFI - Manage Assets and Get Financial Insights

## Overview

MAGFI is a financial management API that provides real-time analysis of assets and currencies in financial markets. It helps investors track their portfolio, identify optimal buying moments through price alerts, and make informed investment decisions using financial indicators (P/L ratio, P/VPA).

The system continuously monitors assets and currencies, comparing current market prices with user-defined targets and calculates fair value metrics based on sector comparisons.

## Core Features

- 📊 Asset and currency tracking with price monitoring
- 🎯 Smart price drop alerts (time-to-buy indicators)
- 💰 Financial analysis using P/L and P/VPA indicators
- 💵 Multi-currency support with configurable default currency
- 📈 Portfolio management and dividend tracking
- 🔄 Integration with AI-powered market predictions (magfi-predictor)
- 📰 News-based market analysis (magfi-ingestor)

## Technology Stack

- **Python 3.13**
- **FastAPI** - Async web framework
- **PostgreSQL + Supabase** - Data persistence
- **Pydantic** - Data validation
- **SQLAlchemy** - ORM
- **Docker & Docker Compose** - Containerization

## Local Setup

### Prerequisites

- Python 3.13
- PostgreSQL 15+
- pip & virtualenv

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd magfi/magfi-core

# Create virtual environment
python3.13 -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment variables
cp .env.example .env
# Edit .env with your Supabase credentials and API keys

# Run migrations (if applicable)
python -m alembic upgrade head

# Start the application
uvicorn main:app --reload --host 0.0.0.0 --port 8100
```

### Running with Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Application will be available at http://localhost:8100
# Health check: http://localhost:8100/health
# API documentation: http://localhost:8100/docs
```

## API Endpoints

### Health & Config

- `GET /health` - Health check
- `GET /config` - Get all configurations
- `GET /config/?configName=last-update` - Get specific configuration
- `PUT /config` - Update configuration

### Assets Management

- `POST /market/asset` - Create new asset
- `GET /market/asset/?tickerSymbol=AAPL` - Get specific asset
- `GET /market/assets` - Get all assets
- `PUT /market/asset/?tickerSymbol=AAPL` - Update asset
- `DELETE /market/asset/?tickerSymbol=AAPL` - Delete asset

### Currencies Management

- `POST /market/currency` - Create new currency
- `GET /market/currency/?currencyCode=USD` - Get specific currency
- `GET /market/currencies` - Get all currencies
- `PUT /market/currency/?currencyCode=USD` - Update currency
- `DELETE /market/currency/?currencyCode=USD` - Delete currency

### Market Analysis & Alerts

- `GET /market/drop-alert/assets` - Assets ready to buy (price targets met)
- `GET /market/drop-alert/currencies` - Currencies ready to buy (price targets met)
- `GET /market/report/prediction` - AI-powered market prediction report

### Portfolio Management

- `GET /market/dividend-gains` - Get portfolio dividend gains
- `GET /market/accounts` - Get all accounts
- `POST /market/account` - Create investment account

## Configuration

### Environment Variables (.env)

```
APP_NAME=magfi-core
APP_ENV=development
DEBUG=true

DATABASE_URL=postgresql://user:password@localhost:5432/magfi_db
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-api-key

MAGFI_INGESTOR_URL=http://localhost:8200
MAGFI_PREDICTOR_URL=http://localhost:8300

OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...

API_PORT=8100
LOG_LEVEL=INFO
```

## Project Structure

```
magfi-core/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models/
│   ├── schemas/
│   ├── routes/
│   ├── database/
│   ├── services/
│   └── utils/
├── migrations/
├── tests/
├── ddl/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

## Database Schema

See `ddl/` folder for complete PostgreSQL DDL statements:

- `01_config.sql` - Configuration table
- `02_assets.sql` - Assets and indicators
- `03_currencies.sql` - Currency pairs
- `04_accounts.sql` - Investment accounts
- `05_dividends.sql` - Dividend tracking

## Development

```bash
# Run tests
pytest tests/ -v

# Run with auto-reload
uvicorn app.main:app --reload

# Format code
black app/

# Lint
pylint app/
```

## API Response Format

### Success Response

```json
{
  "success": true,
  "data": {...},
  "message": "Operation completed successfully"
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

## Integration with Other MAGFI Services

- **magfi-ingestor**: Provides financial news analysis data (fct_news_analysis table)
- **magfi-predictor**: Consumes asset/currency data and returns market predictions

Note: magfi-core operates independently and doesn't require these services to function.

## Contributing

Follow PEP 8 guidelines. Code should be clean, typed, and well-tested.

## License

MIT
