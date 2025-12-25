from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ConfigSchema, ConfigResponseSchema, ApiResponseSchema
from app.services.config_service import ConfigService

router = APIRouter(prefix="/config", tags=["config"])


@router.get("", response_model=ApiResponseSchema)
def get_all_configs(db: Session = Depends(get_db)):
    try:
        configs = ConfigService.get_all_configs(db)
        data = [{"id": str(c.id), "config_name": c.config_name, "config_value": c.config_value} for c in configs]
        return {
            "success": True,
            "data": data,
            "message": "Configuration retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=ApiResponseSchema)
def get_config_by_name(config_name: str = Query(...), db: Session = Depends(get_db)):
    try:
        config = ConfigService.get_config(db, config_name)
        if not config:
            raise HTTPException(status_code=404, detail="Configuration not found")
        
        return {
            "success": True,
            "data": {
                "id": str(config.id),
                "config_name": config.config_name,
                "config_value": config.config_value
            },
            "message": "Configuration retrieved successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("", response_model=ApiResponseSchema)
def update_config(config_data: dict, db: Session = Depends(get_db)):
    try:
        updated_configs = []
        for key, value in config_data.items():
            config = ConfigService.set_config(db, key, str(value))
            updated_configs.append({
                "id": str(config.id),
                "config_name": config.config_name,
                "config_value": config.config_value
            })
        
        return {
            "success": True,
            "data": updated_configs,
            "message": "Configuration updated successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
