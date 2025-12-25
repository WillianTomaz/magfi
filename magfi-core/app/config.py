from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "magfi-core"
    app_env: str = "development"
    debug: bool = True
    
    database_url: str
    supabase_url: str
    supabase_key: str
    
    magfi_ingestor_url: str
    magfi_predictor_url: str
    
    openai_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    
    api_port: int = 8000
    api_host: str = "0.0.0.0"
    log_level: str = "INFO"
    
    jwt_secret_key: str = "change-me-in-production"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
