from sqlalchemy.orm import Session
from app.models import Config
from app.schemas import ConfigSchema
from datetime import datetime


class ConfigService:
    @staticmethod
    def set_config(db: Session, config_name: str, config_value: str):
        config = db.query(Config).filter(Config.config_name == config_name).first()
        
        if config:
            config.config_value = config_value
            config.updated_at = datetime.utcnow()
        else:
            config = Config(config_name=config_name, config_value=config_value)
            db.add(config)
        
        db.commit()
        db.refresh(config)
        return config

    @staticmethod
    def get_config(db: Session, config_name: str):
        return db.query(Config).filter(Config.config_name == config_name).first()

    @staticmethod
    def get_all_configs(db: Session):
        return db.query(Config).all()

    @staticmethod
    def update_config(db: Session, config_name: str, config_value: str):
        return ConfigService.set_config(db, config_name, config_value)
