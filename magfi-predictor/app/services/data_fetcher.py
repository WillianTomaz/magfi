import httpx
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class DataFetcher:
    @staticmethod
    async def fetch_assets():
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.magfi_core_url}/market/assets",
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                return data.get("data", [])
        except Exception as e:
            logger.error(f"Error fetching assets: {str(e)}")
            return []

    @staticmethod
    async def fetch_asset(ticker: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.magfi_core_url}/market/asset",
                    params={"tickerSymbol": ticker},
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                return data.get("data")
        except Exception as e:
            logger.error(f"Error fetching asset {ticker}: {str(e)}")
            return None

    @staticmethod
    async def fetch_news_analysis():
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.magfi_ingestor_url}/ingest/news/analyzed",
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                return data.get("data", [])
        except Exception as e:
            logger.error(f"Error fetching news analysis: {str(e)}")
            return []
