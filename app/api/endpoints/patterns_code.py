from csv import excel
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_pattern_code_service, is_user_admin
from app.domain.patterns_code.dtos import PatternsCodeRequest
from app.domain.patterns_code.models import PatternsCodeModel
from app.domain.patterns_code.services import PatternCodeService
from app.domain.users.models import UserProfile

router = APIRouter()

@router.get("/", response_model=list[PatternsCodeModel] | str)
async def get_all_pattern_codes(service: PatternCodeService = Depends(get_pattern_code_service)) -> list[PatternsCodeModel] | str:
    """
    Get all pattern codes.

    Retrieves a list of all pattern code mappings.
    Returns a list of PatternsCodeModel or a string if none are found.
    """
    try:
        patterns_codes = service.get_all_pattern_codes()
        if not patterns_codes:
            return "No patterns codes to show"
        return patterns_codes
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{pattern_id}", response_model=list[PatternsCodeModel] | PatternsCodeModel)
async def get_pattern_code_by_id(
        pattern_id: UUID,
        code_id: UUID,
        service: PatternCodeService = Depends(get_pattern_code_service)
) -> list[PatternsCodeModel] | PatternsCodeModel:
    """
    Get pattern codes by ID.

    Retrieves pattern codes by pattern ID. If code_id is provided, retrieves a specific pattern code.
    """
    try:
        if code_id is None:
            pattern_code = service.get_pattern_code_by_id(pattern_id=pattern_id)
        else:
            pattern_code = service.get_pattern_code_by_all_id(code_id, pattern_id)
        if not pattern_code:
            return []

        return  pattern_code
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/", response_model=PatternsCodeModel)
async def create_pattern_code(
        data: PatternsCodeRequest,
        service: PatternCodeService = Depends(get_pattern_code_service),
        user_auth: tuple[UserProfile, str] = Depends(is_user_admin)
) -> PatternsCodeModel:
    """
    Create a new pattern code.

    Creates a new pattern code mapping. Requires admin privileges.
    """
    try:
        token = user_auth[1]
        return service.create_pattern_code(data, token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{pattern_id}", response_model=PatternsCodeModel)
async def update_pattern_code(
        pattern_id: UUID,
        code_id: UUID,
        data: PatternsCodeRequest,
        service: PatternCodeService = Depends(get_pattern_code_service),
        user_auth: tuple[UserProfile, str] = Depends(is_user_admin)
) -> PatternsCodeModel:
    """
    Update a pattern code.

    Updates the specified pattern code. Requires admin privileges.
    """
    try:
        token = user_auth[1]
        pattern_code = service.update_pattern_code(code_id,pattern_id, data, token)
        return  pattern_code
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{pattern_id}", status_code=204)
async def delete_pattern_code(
        pattern_id: UUID,
        code_id: UUID,
        service: PatternCodeService = Depends(get_pattern_code_service),
        user_auth: tuple[UserProfile, str] = Depends(is_user_admin)
) -> None:
    """
    Delete a pattern code.

    Deletes the specified pattern code from the system. Requires admin privileges.
    """
    try:
        token = user_auth[1]
        service.delete_pattern_code(code_id, pattern_id, token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
