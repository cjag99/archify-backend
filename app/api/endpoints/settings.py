from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends

from app.api.dependencies import get_settings_service, get_current_user, is_user_admin
from app.domain.settings.dtos import SettingsRequest
from app.domain.settings.services import SettingsService
from app.domain.users.models import UserProfile

router = APIRouter()

@router.get("/")
async def get_settings(
        service: SettingsService = Depends(get_settings_service),
        user_auth: tuple[UserProfile, str] = Depends(get_current_user)
):
    try:
        token = user_auth[1]
        settings = service.get_settings(token)
        if not settings:
            return "No settings to show"
        return settings

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/")
async def create_setting(
        data: SettingsRequest,
        service: SettingsService = Depends(get_settings_service),
        user_auth: tuple[UserProfile, str] = Depends(is_user_admin)
):
    try:
        token = user_auth[1]
        service.create_settings(data, token)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{setting_id}")
async def get_setting_by_id(
        setting_id: UUID,
        service: SettingsService = Depends(get_settings_service),
        user_auth: tuple[UserProfile, str] = Depends(get_current_user)
):
    try:
        token = user_auth[1]
        setting = service.get_setting_by_id(setting_id, token)
        if not setting:
            raise HTTPException(status_code=404, detail="Setting not found")
        return setting

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{setting_id}")
async def update_setting(
        setting_id: UUID,
        data: SettingsRequest,
        service: SettingsService = Depends(get_settings_service),
        user_auth: tuple[UserProfile, str] = Depends(is_user_admin)
):
    try:
        token = user_auth[1]
        service.update_setting(setting_id, data, token)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{setting_id}")
async def delete_setting(
        setting_id: UUID,
        service: SettingsService = Depends(get_settings_service),
        user_auth: tuple[UserProfile, str] = Depends(is_user_admin)
):
    try:
        token = user_auth[1]
        service.delete_setting(setting_id, token)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
