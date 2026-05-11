from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from app.domain.users.models import UserProfile
from app.api.dependencies import get_architecture_service, get_current_user, is_user_admin
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

@router.get("/{architecture_id}")
async def get_architecture_by_id(
        architecture_id: UUID,
        service: ArchitectureService = Depends(get_architecture_service),
        user_auth: tuple[UserProfile, str] = Depends(get_current_user)
) -> ArchitectureModel:
    try:
        token = user_auth[1]
        architecture = service.get_architecture_by_id(architecture_id, token)
        if not architecture:
            raise HTTPException(status_code=404, detail="Architecture not found")
        return  architecture
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/")
async def create_architecture(
        data: ArchitectureRequest,
        service: ArchitectureService = Depends(get_architecture_service),
        user_auth: tuple[UserProfile, str] = Depends(is_user_admin)
) -> ArchitectureModel | str:
    try:
        token = user_auth[1]
        architecture = service.create_architecture(data, token)
        return architecture
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{architecture_id}")
async def update_architecture(
        architecture_id: UUID,
        data: ArchitectureRequest,
        service: ArchitectureService = Depends(get_architecture_service),
        user_auth: tuple[UserProfile, str] = Depends(is_user_admin)
) -> None:
    try:
        token = user_auth[1]
        service.update_architecture(architecture_id, data, token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{architecture_id}")
async  def delete_architecture(
        architecture_id: UUID,
        service: ArchitectureService = Depends(get_architecture_service),
        user_auth: tuple[UserProfile, str] = Depends(is_user_admin)
) -> None:
    try:
        token = user_auth[1]
        service.delete_architecture(architecture_id, token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))