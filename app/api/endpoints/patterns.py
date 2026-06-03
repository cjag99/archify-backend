from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from app.api.dependencies import get_pattern_service, is_user_admin
from app.domain.patterns.dtos import PatternRequestModel
from app.domain.patterns.models import PatternModel
from app.domain.patterns.services import PatternService
from app.domain.users.models import UserProfile

router = APIRouter()

@router.get("/", response_model=list[PatternModel] | str)
async def get_patterns(service: PatternService = Depends(get_pattern_service)) -> list[PatternModel] | str:
    """
    Get all patterns.

    Retrieves a list of all patterns available.
    Returns a list of PatternModel or a string if none are found.
    """
    try:
        patterns = service.get_all_patterns()
        if not patterns:
            return "No patterns to show"

        return patterns
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/", response_model=PatternModel)
async def create_pattern(
        data: PatternRequestModel,
        service: PatternService = Depends(get_pattern_service),
        user_auth: tuple[UserProfile, str] = Depends(is_user_admin),
) -> PatternModel:
    """
    Create a new pattern.

    Creates a new design pattern. Requires admin privileges.
    """
    user, token = user_auth
    try:
        pattern = service.create_pattern(data, user.id, token)
        return pattern
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{pattern_id}", response_model=PatternModel | None)
async def get_pattern_from_id(
        pattern_id: UUID,
        service: PatternService = Depends(get_pattern_service),
) -> PatternModel | None:
    """
    Get pattern by ID.

    Retrieves a specific design pattern by its unique identifier.
    """
    try:
        pattern = service.get_pattern_by_id(pattern_id)
        if not pattern:
            return None
        return pattern
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
@router.patch("/{pattern_id}", response_model=PatternModel)
async def update_pattern(
        pattern_id: UUID,
        data: PatternRequestModel,
        service: PatternService = Depends(get_pattern_service),
        user_auth: tuple[UserProfile, str] = Depends(is_user_admin),

) -> PatternModel:
    """
    Update a pattern.

    Updates the specified pattern. Requires admin privileges.
    """
    try:
        user, token = user_auth
        service.update_pattern(pattern_id, data, token)
        return service.get_pattern_by_id(pattern_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{pattern_id}", status_code=204)
async def delete_pattern(
        pattern_id: UUID,
        service: PatternService = Depends(get_pattern_service),
        user_auth: tuple[UserProfile, str] = Depends(is_user_admin),
) -> None:
    """
    Delete a pattern.

    Deletes the specified pattern from the system. Requires admin privileges.
    """
    try:
        user, token = user_auth
        service.delete_pattern(pattern_id, token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))