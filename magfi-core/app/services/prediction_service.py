import httpx
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class PredictionService:
    @staticmethod
    async def get_market_prediction():
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.magfi_predictor_url}/predict",
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error fetching prediction: {str(e)}")
            return {
                "success": False,
                "error": "Unable to fetch predictions at the moment"
            }

    @staticmethod
    async def get_asset_prediction(ticker_symbol: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.magfi_predictor_url}/predict/{ticker_symbol}",
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error fetching prediction for {ticker_symbol}: {str(e)}")
            return {
                "success": False,
                "error": "Unable to fetch prediction for this asset"
            }
