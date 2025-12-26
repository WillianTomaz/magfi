from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "magfi-predictor"
    app_env: str = "development"
    debug: bool = True
    
    database_url: str
    supabase_url: str
    supabase_key: str
    
    api_port: int = 8300
    api_host: str = "0.0.0.0"
    log_level: str = "INFO"
    
    magfi_core_url: str
    magfi_ingestor_url: str
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
