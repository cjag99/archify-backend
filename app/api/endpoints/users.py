from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_user_service, is_user_admin, get_current_user
from app.domain.users.models import UserProfile, UserUpdateRequest
from app.domain.users.services import UserService


router = APIRouter()

@router.get("/")
async def get_all_users(
    service: UserService = Depends(get_user_service),
    user_auth: tuple[UserProfile, str] = Depends(is_user_admin),
):
    try:
        token = user_auth[1]
        users = service.get_all_users(token)
        if not users:
            return "No users to show"
        return users
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}")
async def get_profile(
        user_id: UUID,
        service: UserService = Depends(get_user_service),
        user_auth: tuple[UserProfile, str] = Depends(get_current_user)
) -> UserProfile | None:
    try:
        user, token = user_auth
        if user.id == user_id or user.is_authorized:
            user = service.get_user_by_id(user_id, token)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{user_id}")
async def update_profile(
        user_id: UUID,
        data: UserUpdateRequest,
        service: UserService = Depends(get_user_service),
        user_auth: tuple[UserProfile, str] = Depends(get_current_user)
) -> UserProfile:
    try:
        user, token = user_auth
        if user.id == user_id or user.role == "admin":
            return service.update_user_profile(user_id, data, token)
        else:
            raise HTTPException(status_code=403, detail="Not authorized to update this profile")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{user_id}")
async def delete_profile(
        user_id: UUID,
        service: UserService = Depends(get_user_service),
        user_auth: tuple[UserProfile, str] = Depends(get_current_user)
) -> None:
    try:
        user, token = user_auth
        if user.id == user_id or user.is_authorized:
            service.delete_user(user_id, token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
