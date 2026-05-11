from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_code_language_service, get_current_user, is_user_admin
from app.domain.code_languages.dtos import CodeLanguagesRequest
from app.domain.code_languages.models import CodeLanguagesModel
from app.domain.code_languages.services import CodeLanguagesService
from app.domain.users.models import UserProfile

router = APIRouter()

@router.get("/")
async def get_all_code_languages(
        service: CodeLanguagesService = Depends(get_code_language_service),
        user_auth: tuple[UserProfile, str] = Depends(get_current_user)
) -> list[CodeLanguagesModel] | str:
    try:
        token = user_auth[1]
        code_languages = service.get_all_code_languages(token)
        if not code_languages:
            return "No code languages to show"
        return code_languages
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{code_language_id}")
async  def get_code_language_by_id(
        code_language_id: UUID,
        service: CodeLanguagesService = Depends(get_code_language_service),
        user_auth: tuple[UserProfile, str] = Depends(get_current_user)
) -> CodeLanguagesModel:
    try:
        token = user_auth[1]
        code_language = service.get_code_language_by_id(code_language_id, token)
        if not code_language:
            raise HTTPException(status_code=404, detail="Code language not found")
        return code_language
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/")
async def create_code_language(
        data: CodeLanguagesRequest,
        service: CodeLanguagesService = Depends(get_code_language_service),
        user_auth: tuple[UserProfile, str] = Depends(is_user_admin)
) -> CodeLanguagesModel:
    try:
        token = user_auth[1]
        code_language = service.create_code_language(data, token)
        return  code_language
    except Exception as e:
        raise  HTTPException(status_code=400, detail=str(e))

@router.patch("/{code_language_id}")
async def update_code_language(
        code_language_id: UUID,
        data: CodeLanguagesRequest,
        service: CodeLanguagesService = Depends(get_code_language_service),
        user_auth: tuple[UserProfile, str] = Depends(is_user_admin)
) -> None:
    try:
        token = user_auth[1]
        service.update_code_language(code_language_id, data, token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{code_language_id}")
async def delete_code_language(
        code_language_id: UUID,
        service: CodeLanguagesService = Depends(get_code_language_service),
        user_auth: tuple[UserProfile, str] = Depends(is_user_admin)
) -> None:
    try:
        token = user_auth[1]
        service.delete_code_language(code_language_id, token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))