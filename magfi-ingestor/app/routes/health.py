from fastapi import APIRouter, Depends
from app.schemas import HealthResponseSchema
from app.config import settings

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponseSchema)
def health_check():
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "environment": settings.app_env,
    }
