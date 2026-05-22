from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends

from app.api.dependencies import get_profile_settings_service, get_current_user, is_user_admin
from app.domain.profile_settings.services import ProfileSettingService
from app.domain.users.models import UserProfile

router = APIRouter()

@router.get("/")
async def get_profile_settings(
        service: ProfileSettingService = Depends(get_profile_settings_service),
        user_auth: tuple[UserProfile, str] = Depends(is_user_admin)
):
    try:
        token = user_auth[1]
        profile_settings = service.get_profile_settings(token)
        if not profile_settings:
            return "No profile settings to show"
        return profile_settings

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}")
async def get_user_settings(
        user_id: UUID,
        service: ProfileSettingService = Depends(get_profile_settings_service),
        user_auth: tuple[UserProfile, str] = Depends(get_current_user)
):
    try:
        user, token = user_auth[1]
        if user.id != user_id:
            raise HTTPException(status_code=403, detail="Not authenticated user")

        profile_settings = service.get_user_settings(user_id, token)
        if not profile_settings:
            return "No profile settings to show"
        return profile_settings

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}?setting_id={setting_id}")
async def get_profile_setting_by_id(
        user_id: UUID,
        setting_id: UUID,
        service: ProfileSettingService = Depends(get_profile_settings_service),
        user_auth: tuple[UserProfile, str] = Depends(is_user_admin)
):
    try:
        token = user_auth[1]
        profile_setting = service.get_profile_setting_by_id(user_id, setting_id, token)
        if not profile_setting:
            raise HTTPException(status_code=404, detail="Profile setting not found")
        return profile_setting

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{user_id}?setting_id={setting_id}")
async def update_profile_setting(
        user_id: UUID,
        setting_id: UUID,
        service: ProfileSettingService = Depends(get_profile_settings_service),
        user_auth: tuple[UserProfile, str] = Depends(get_current_user)
):
    try:
        user, token = user_auth
        if user.id != user_id and not user.is_authorized:
            raise HTTPException(status_code=403, detail="Not authenticated user")

        profile_setting = service.get_profile_setting_by_id(user_id, setting_id, token)
        if not profile_setting:
            raise HTTPException(status_code=404, detail="Profile setting not found")
        service.update_profile_setting(user_id, setting_id, profile_setting)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{user_id}?setting_id={setting_id}")
async def delete_profile_setting(
        user_id: UUID,
        setting_id: UUID,
        service: ProfileSettingService = Depends(get_profile_settings_service),
        user_auth: tuple[UserProfile, str] = Depends(get_current_user)
):
    try:
        user, token = user_auth
        if user.id != user_id and not user.is_authorized:
            raise HTTPException(status_code=403, detail="Not authenticated user")

        profile_setting = service.get_profile_setting_by_id(user_id, setting_id, token)
        if not profile_setting:
            raise HTTPException(status_code=404, detail="Profile setting not found")

        service.delete_profile_setting(user_id, setting_id)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
