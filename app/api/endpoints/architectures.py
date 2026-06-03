from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from app.domain.users.models import UserProfile
from app.api.dependencies import get_architecture_service, get_current_user, is_user_admin
from app.domain.architectures.models import ArchitectureModel
from app.domain.architectures.dtos import ArchitectureRequest
from app.domain.architectures.services import ArchitectureService

router = APIRouter()

@router.get("/", response_model=list[ArchitectureModel] | str)
async def get_all_architectures(
        service: ArchitectureService = Depends(get_architecture_service),
        user_auth: tuple[UserProfile, str] = Depends(get_current_user)
) -> list[ArchitectureModel] | str:
    """
    Get all architectures.

    Retrieves all architectures from the system.
    Returns a list of ArchitectureModel or a string if none are found.
    """
    try:
        token = user_auth[1]
        architectures = service.get_all_architectures(token)
        if not architectures:
            return "No architectures to show"
        return architectures
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{architecture_id}", response_model=ArchitectureModel)
async def get_architecture_by_id(
        architecture_id: UUID,
        service: ArchitectureService = Depends(get_architecture_service),
        user_auth: tuple[UserProfile, str] = Depends(get_current_user)
) -> ArchitectureModel:
    """
    Get architecture by ID.

    Retrieves a specific architecture by its unique identifier.
    """
    try:
        token = user_auth[1]
        architecture = service.get_architecture_by_id(architecture_id, token)
        if not architecture:
            raise HTTPException(status_code=404, detail="Architecture not found")
        return  architecture
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/", response_model=ArchitectureModel | str)
async def create_architecture(
        data: ArchitectureRequest,
        service: ArchitectureService = Depends(get_architecture_service),
        user_auth: tuple[UserProfile, str] = Depends(is_user_admin)
) -> ArchitectureModel | str:
    """
    Create a new architecture.

    Creates a new architecture in the system. Requires admin privileges.
    """
    try:
        token = user_auth[1]
        architecture = service.create_architecture(data, token)
        return architecture
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{architecture_id}", response_model=ArchitectureModel)
async def update_architecture(
        architecture_id: UUID,
        data: ArchitectureRequest,
        service: ArchitectureService = Depends(get_architecture_service),
        user_auth: tuple[UserProfile, str] = Depends(is_user_admin)
) -> ArchitectureModel:
    """
    Update an architecture.

    Updates the specified architecture. Requires admin privileges.
    """
    try:
        token = user_auth[1]
        architecture = service.update_architecture(architecture_id, data, token)
        return architecture
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{architecture_id}", status_code=204)
async  def delete_architecture(
        architecture_id: UUID,
        service: ArchitectureService = Depends(get_architecture_service),
        user_auth: tuple[UserProfile, str] = Depends(is_user_admin)
) -> None:
    """
    Delete an architecture.

    Deletes the specified architecture from the system. Requires admin privileges.
    """
    try:
        token = user_auth[1]
        service.delete_architecture(architecture_id, token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))