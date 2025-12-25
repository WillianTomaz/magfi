# MAGFI Ingestor

## Overview
MAGFI Ingestor is responsible for collecting financial news from various RSS feeds and sources, storing raw data in `stg_news_raw` table, and processing it through AI models for sentiment analysis and impact scoring. Results are stored in `fct_news_analysis` table.

## Features
- 📰 RSS feed collection from financial news sources
- 🤖 AI-powered sentiment analysis (OpenAI/Gemini)
- 🔄 Automatic batch processing and scheduling
- 📊 Impact scoring for market relevance
- 🔗 Integration with magfi-core for asset tagging

## Technology Stack
- **Python 3.14**
- **FastAPI**
- **PostgreSQL + Supabase**
- **APScheduler** - Task scheduling
- **Feedparser** - RSS feed parsing
- **OpenAI/Gemini API** - AI Analysis

## Installation

```bash
cd magfi/magfi-ingestor

python3.14 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
# Configure your environment variables

# Run with Docker
docker-compose up --build
```

## API Endpoints

- `GET /health` - Health check
- `POST /ingest/news` - Manually trigger news ingestion
- `GET /tasks/status` - Get processing task status
- `GET /news/raw` - View raw ingested news
- `GET /news/processed` - View processed news analysis
