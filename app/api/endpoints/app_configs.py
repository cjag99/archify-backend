from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from app.api.dependencies import get_app_config_service, is_user_admin, get_current_user
from app.domain.app_configs.dtos import AppConfigRequest
from app.domain.app_configs.services import AppConfigService
from app.domain.users.models import UserProfile

router = APIRouter()

@router.get("/")
async def get_app_configs(
        service: AppConfigService = Depends(get_app_config_service),
        user_auth: tuple[UserProfile, str] = Depends(is_user_admin)
):
    try:
        token =user_auth[1]
        app_configs = service.get_all_configs(token)
        if not app_configs:
            return "No app configs to show"
        return app_configs

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/enabled")
async def get_enabled_configs(
        service: AppConfigService = Depends(get_app_config_service),
        user_auth: tuple[UserProfile, str] = Depends(get_current_user)
):
    try:
        user = user_auth[0]
        if user:
            return service.get_enabled_configs()
        else:
            raise HTTPException(status_code=404, detail="User not found")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{app_config_id}")
async def get_app_config_by_id(
        app_config_id: UUID,
        service: AppConfigService = Depends(get_app_config_service),
        user_auth: tuple[UserProfile, str] = Depends(is_user_admin)
):
    try:
        token = user_auth[1]
        app_config = service.get_config_by_id(app_config_id, token)
        if not app_config:
            raise HTTPException(status_code=404, detail="App config not found")
        return app_config
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/")
async def create_app_config(
        data: AppConfigRequest,
        service: AppConfigService = Depends(get_app_config_service),
        user_auth: tuple[UserProfile, str] = Depends(is_user_admin)
):
    try:
        token = user_auth[1]
        app_config = service.create_config(data, token)
        return app_config

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{app_config_id}")
async def update_app_config(
        app_config_id: UUID,
        data: AppConfigRequest,
        service: AppConfigService = Depends(get_app_config_service),
        user_auth: tuple[UserProfile, str] = Depends(is_user_admin)
):
    try:
        token = user_auth[1]
        service.update_config(app_config_id, data, token)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{app_config_id}")
async def delete_app_config(
        app_config_id: UUID,
        service: AppConfigService = Depends(get_app_config_service),
        user_auth: tuple[UserProfile, str] = Depends(is_user_admin)
):
    try:
        token = user_auth[1]
        service.delete_config(app_config_id, token)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

