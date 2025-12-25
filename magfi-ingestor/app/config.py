from pydantic_settings import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
    app_name: str = "magfi-ingestor"
    app_env: str = "development"
    debug: bool = True
    
    database_url: str
    supabase_url: str
    supabase_key: str
    
    openai_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    
    api_port: int = 8001
    api_host: str = "0.0.0.0"
    log_level: str = "INFO"
    
    rss_feeds: str = ""
    batch_processing_interval: int = 300
    sentiment_analysis_model: str = "openai"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def feeds_list(self) -> List[str]:
        return [feed.strip() for feed in self.rss_feeds.split(",") if feed.strip()]


settings = Settings()
