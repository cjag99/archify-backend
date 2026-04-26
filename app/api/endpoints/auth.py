from fastapi import APIRouter, HTTPException, Depends
from app.api.dependencies import get_auth_service
from app.domain.auth.dtos import UserRegistrationRequest
from app.domain.auth.services import AuthService


router = APIRouter()

@router.post("/register")
async def register_user(
    data: UserRegistrationRequest,
    service: AuthService = Depends(get_auth_service)
):
    try:
        user_profile = service.register_user(data)
        return user_profile
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.post("/login")
async def login_user(
    data: UserRegistrationRequest,
    service: AuthService = Depends(get_auth_service)
):
    try:
        token = service.login_user(data)
        return {"token": token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))