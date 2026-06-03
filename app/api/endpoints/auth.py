from fastapi import APIRouter, HTTPException, Depends
from app.api.dependencies import get_auth_service
from app.domain.auth.dtos import UserLoginRequest, UserRegistrationRequest
from app.domain.auth.services import AuthService


router = APIRouter()

@router.post("/register", response_model=str)
async def register_user(
    data: UserRegistrationRequest,
    service: AuthService = Depends(get_auth_service)
) -> str:
    """
    Register a new user.

    Creates a new user profile using the provided registration data.
    """
    try:
        user_profile = service.register_user(data)
        return user_profile
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.post("/login", response_model=str)
async def login_user(
    data: UserLoginRequest,
    service: AuthService = Depends(get_auth_service)
) -> str:
    """
    Log in a user.

    Authenticates the user with email and password and returns an access token.
    """
    try:
       response = service.login_user(data)
       return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))