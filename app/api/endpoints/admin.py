from fastapi import APIRouter, Depends

from app.api.dependencies import get_user_service, is_user_admin
from app.domain.users.models import UserProfile
from app.domain.users.services import UserService


router = APIRouter()

@router.get("/users")
async def get_all_users(
    service: UserService = Depends(get_user_service),
    user_auth: tuple[UserProfile, str] = Depends(is_user_admin),
) -> list[UserProfile]:
    token = user_auth[1]
    return service.get_all_users(token)