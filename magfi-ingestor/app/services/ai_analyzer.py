from app.config import settings
import logging
import json
from typing import Optional

logger = logging.getLogger(__name__)


class AIAnalyzer:
    @staticmethod
    async def analyze_sentiment(text: str) -> dict:
        if settings.sentiment_analysis_model == "openai":
            return await AIAnalyzer._analyze_with_openai(text)
        else:
            return await AIAnalyzer._analyze_with_gemini(text)

    @staticmethod
    async def _analyze_with_openai(text: str) -> dict:
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=settings.openai_api_key)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": f"""Analyze this financial news and provide:
1. Sentiment (positive, negative, neutral)
2. Impact score (0-1)
3. Brief analysis
4. Potential asset tickers mentioned

Text: {text}

Return as JSON."""
                    }
                ],
                temperature=0.3,
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
        except Exception as e:
            logger.error(f"OpenAI analysis error: {str(e)}")
            return {"sentiment": "neutral", "impact_score": 0.5, "analysis": "Unable to analyze"}

    @staticmethod
    async def _analyze_with_gemini(text: str) -> dict:
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=settings.gemini_api_key)
            model = genai.GenerativeModel("gemini-pro")
            
            response = model.generate_content(f"""Analyze this financial news and provide:
1. Sentiment (positive, negative, neutral)
2. Impact score (0-1)
3. Brief analysis
4. Potential asset tickers mentioned

Text: {text}

Return as JSON.""")
            
            result = json.loads(response.text)
            return result
        except Exception as e:
            logger.error(f"Gemini analysis error: {str(e)}")
            return {"sentiment": "neutral", "impact_score": 0.5, "analysis": "Unable to analyze"}
