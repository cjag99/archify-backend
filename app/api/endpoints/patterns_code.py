from csv import excel
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_pattern_code_service, is_user_admin
from app.domain.patterns_code.dtos import PatternsCodeRequest
from app.domain.patterns_code.models import PatternsCodeModel
from app.domain.patterns_code.services import PatternCodeService
from app.domain.users.models import UserProfile

router = APIRouter()

@router.get("/")
async def get_all_pattern_codes(service: PatternCodeService = Depends(get_pattern_code_service)):
    try:
        patterns_codes = service.get_all_pattern_codes()
        if not patterns_codes:
            return "No patterns codes to show"
        return patterns_codes
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{pattern_id}")
async def get_pattern_code_by_id(
        pattern_id: UUID,
        code_id: UUID,
        service: PatternCodeService = Depends(get_pattern_code_service)
) -> PatternsCodeModel:
    try:
        pattern_code = service.get_pattern_code_by_id(code_id, pattern_id)
        if not pattern_code:
            raise HTTPException(status_code=404, detail="Pattern code not found")
        return  pattern_code
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/")
async def create_pattern_code(
        data: PatternsCodeRequest,
        service: PatternCodeService = Depends(get_pattern_code_service),
        user_auth: tuple[UserProfile, str] = Depends(is_user_admin)
) -> PatternsCodeModel:
    try:
        token = user_auth[1]
        return service.create_pattern_code(data, token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{pattern_id}")
async def update_pattern_code(
        pattern_id: UUID,
        code_id: UUID,
        data: PatternsCodeRequest,
        service: PatternCodeService = Depends(get_pattern_code_service),
        user_auth: tuple[UserProfile, str] = Depends(is_user_admin)
) -> PatternsCodeModel:
    try:
        token = user_auth[1]
        pattern_code = service.update_pattern_code(code_id,pattern_id, data, token)
        return  pattern_code
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{pattern_id}")
async def delete_pattern_code(
        pattern_id: UUID,
        code_id: UUID,
        service: PatternCodeService = Depends(get_pattern_code_service),
        user_auth: tuple[UserProfile, str] = Depends(is_user_admin)
) -> None:
    try:
        token = user_auth[1]
        service.delete_pattern_code(code_id, pattern_id, token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
