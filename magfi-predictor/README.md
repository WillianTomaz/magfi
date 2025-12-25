# MAGFI Predictor

## Overview
MAGFI Predictor consumes financial data from magfi-core and news analysis from magfi-ingestor to generate AI-powered market predictions. It forecasts asset price movements and market trends using machine learning and sentiment analysis.

## Features
- 🤖 ML-based price prediction models
- 📊 Sentiment-driven market forecasts
- 📈 Historical trend analysis
- 🔮 Multi-horizon predictions (1-week, 1-month, 3-month)
- 🎯 Confidence scoring

## Technology Stack
- **Python 3.14**
- **FastAPI**
- **PostgreSQL + Supabase**
- **scikit-learn** - Machine learning
- **pandas** - Data analysis

## Installation

```bash
cd magfi/magfi-predictor

python3.14 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env

# Run with Docker
docker-compose up --build
```

## API Endpoints

- `GET /health` - Health check
- `GET /predict` - Get market predictions
- `GET /predict/{ticker}` - Get asset-specific prediction
- `POST /model/retrain` - Trigger model retraining
