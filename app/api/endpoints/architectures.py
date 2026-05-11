from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from app.domain.users.models import UserProfile
from app.api.dependencies import get_architecture_service, get_current_user
from app.domain.architectures.models import ArchitectureModel
from app.domain.architectures.dtos import ArchitectureRequest
from app.domain.architectures.services import ArchitectureService

router = APIRouter()

@router.get("/")
async def get_all_architectures(
        service: ArchitectureService = Depends(get_architecture_service),
        user_auth: tuple[UserProfile, str] = Depends(get_current_user)
) -> list[ArchitectureModel] | str:
    try:
        token = user_auth[1]
        architectures = service.get_all_architectures(token)
        if not architectures:
            return "No architectures to show"
        return architectures
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))