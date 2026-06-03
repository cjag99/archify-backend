from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_user_service, is_user_admin, get_current_user, get_auth_service
from app.domain.users.models import UserProfile, UserUpdateRequest
from app.domain.users.services import UserService
from app.domain.auth.services import AuthService
from app.domain.auth.dtos import UserPasswordUpdateRequest


router = APIRouter()

@router.get("/", response_model=list[UserProfile] | str)
async def get_all_users(
    service: UserService = Depends(get_user_service),
    user_auth: tuple[UserProfile, str] = Depends(is_user_admin),
) -> list[UserProfile] | str:
    """
    Get all users.

    Retrieves a list of all user profiles. Requires admin privileges.
    Returns a list of UserProfile objects or a string if no users are found.
    """
    try:
        token = user_auth[1]
        users = service.get_all_users(token)
        if not users:
            return "No users to show"
        return users
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}", response_model=UserProfile | None)
async def get_profile(
        user_id: UUID,
        service: UserService = Depends(get_user_service),
        user_auth: tuple[UserProfile, str] = Depends(get_current_user)
) -> UserProfile | None:
    """
    Get user profile.

    Retrieves the profile of a specific user by their ID.
    Users can only access their own profile unless they have admin privileges.
    """
    try:
        user, token = user_auth
        if user.id == user_id or user.is_authorized:
            user = service.get_user_by_id(user_id, token)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{user_id}", response_model=UserProfile)
async def update_profile(
        user_id: UUID,
        data: UserUpdateRequest,
        service: UserService = Depends(get_user_service),
        user_auth: tuple[UserProfile, str] = Depends(get_current_user)
) -> UserProfile:
    """
    Update user profile.

    Updates the profile information for a specific user.
    Users can only update their own profile unless they have admin privileges.
    """
    try:
        user, token = user_auth
        if user.id == user_id or user.is_authorized:
            return service.update_user_profile(user_id, data, token)
        else:
            raise HTTPException(status_code=403, detail="Not authorized to update this profile")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{user_id}", status_code=204)
async def delete_profile(
        user_id: UUID,
        service: UserService = Depends(get_user_service),
        user_auth: tuple[UserProfile, str] = Depends(get_current_user)
) -> None:
    """
    Delete user profile.

    Deletes the profile of a specific user by their ID.
    Users can only delete their own profile unless they have admin privileges.
    """
    try:
        user, token = user_auth
        if user.id == user_id or user.is_authorized:
            service.delete_user(user_id, token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{user_id}/password", status_code=200)
async def update_password(
    user_id: UUID,
    data: UserPasswordUpdateRequest,
    auth_service: AuthService = Depends(get_auth_service),
    user_auth: tuple[UserProfile, str] = Depends(get_current_user)
) -> dict:
    """
    Update user password.
    """
    try:
        user, _ = user_auth
        if user.id == user_id or user.is_authorized:
            auth_service.update_password(user_id, data.password)
            return {"detail": "Password updated"}
        else:
            raise HTTPException(status_code=403, detail="Not authorized to update this password")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
