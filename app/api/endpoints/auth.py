from fastapi import APIRouter, HTTPException, Depends

from app.api.dependencies import get_auth_service, get_current_user
from app.domain.auth.dtos import UserLoginRequest, UserRegistrationRequest
from app.domain.auth.services import AuthService
from app.domain.users.models import UserProfile


router = APIRouter()

@router.post("/register", response_model=UserProfile)
async def register_user(
    data: UserRegistrationRequest,
    service: AuthService = Depends(get_auth_service)
) -> UserProfile:
    """
    Register a new user.

    Creates a new user profile using the provided registration data.
    """
    try:
        user_profile = service.register_user(data)
        return user_profile
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.post("/login", response_model=dict)
async def login_user(
    data: UserLoginRequest,
    service: AuthService = Depends(get_auth_service)
) -> dict:
    """
    Log in a user.

    Authenticates the user with email and password and returns an access token.
    """
    try:
       response = service.login_user(data)
       return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/logout", response_model=dict)
async def logout_user(
    service: AuthService = Depends(get_auth_service),
    user_auth: tuple[UserProfile, str] = Depends(get_current_user)
) -> dict:
    """
    Log out the current user.

    Inactivates or blacklists the user's current session/token.
    """
    try:
        token = user_auth[1]
        service.logout_user(token)
        return {"detail": "Successfully logged out"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))