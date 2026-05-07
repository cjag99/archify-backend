from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_pattern_service
from app.domain.patterns.services import PatternService

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