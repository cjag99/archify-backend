from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from app.api.dependencies import get_pattern_service, is_user_admin, get_token_from_header
from app.domain.patterns.dtos import PatternRequestModel
from app.domain.patterns.models import PatternModel
from app.domain.patterns.services import PatternService
from app.domain.users.models import UserProfile

router = APIRouter()

@router.get("/")
async def get_patterns(service: PatternService = Depends(get_pattern_service)):
    try:
        patterns = service.get_all_patterns()
        if not patterns:
            return "No patterns to show"

        return patterns
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/")
async def create_pattern(
        data: PatternRequestModel,
        service: PatternService = Depends(get_pattern_service),
        user_auth: tuple[UserProfile, str] = Depends(is_user_admin),
) -> PatternModel:
    user, token = user_auth
    try:
        pattern = service.create_pattern(data, user.id, token)
        return pattern
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{pattern_id}")
async def get_pattern_from_id(
        pattern_id: UUID,
        service: PatternService = Depends(get_pattern_service),
):
    try:
        pattern = service.get_pattern_by_id(pattern_id)
        if not pattern:
            return None
        return pattern
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
@router.patch("/{pattern_id}")
async def update_pattern(
        pattern_id: UUID,
        data: PatternRequestModel,
        service: PatternService = Depends(get_pattern_service),
        user_auth: tuple[UserProfile, str] = Depends(is_user_admin),

):
    try:
        user, token = user_auth
        service.update_pattern(pattern_id, data, token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{pattern_id}")
async def delete_pattern(
        pattern_id: UUID,
        service: PatternService = Depends(get_pattern_service),
        user_auth: tuple[UserProfile, str] = Depends(is_user_admin),
):
    try:
        user, token = user_auth
        service.delete_pattern(pattern_id, token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))