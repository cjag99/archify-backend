from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import (
    get_code_language_service,
    get_current_user,
    get_image_service,
    is_user_admin,
)
from app.domain.code_languages.dtos import CodeLanguagesRequest, CodeLanguagesResponse
from app.domain.code_languages.models import CodeLanguagesModel
from app.domain.code_languages.services import CodeLanguagesService
from app.domain.images.services import ImageServices
from app.domain.users.models import UserProfile
from app.infrastructure.supabase.storage import refresh_storage_url

router = APIRouter()


def _with_icon_url(
    code_language: CodeLanguagesModel,
    user_id: UUID,
    token: str,
    image_service: ImageServices,
) -> CodeLanguagesResponse:
    icon_url = None
    if code_language.icon:
        image = image_service.get_image_by_id(user_id, code_language.icon, token)
        if image:
            icon_url = refresh_storage_url(image.url)
    return CodeLanguagesResponse.from_model(code_language, icon_url=icon_url)


@router.get("/")
async def get_all_code_languages(
        service: CodeLanguagesService = Depends(get_code_language_service),
        image_service: ImageServices = Depends(get_image_service),
        user_auth: tuple[UserProfile, str] = Depends(get_current_user)
) -> list[CodeLanguagesResponse] | str:
    try:
        user, token = user_auth
        code_languages = service.get_all_code_languages(token)
        if not code_languages:
            return "No code languages to show"
        return [
            _with_icon_url(lang, user.id, token, image_service)
            for lang in code_languages
        ]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{code_language_id}")
async  def get_code_language_by_id(
        code_language_id: UUID,
        service: CodeLanguagesService = Depends(get_code_language_service),
        image_service: ImageServices = Depends(get_image_service),
        user_auth: tuple[UserProfile, str] = Depends(get_current_user)
) -> CodeLanguagesResponse:
    try:
        user, token = user_auth
        code_language = service.get_code_language_by_id(code_language_id, token)
        if not code_language:
            raise HTTPException(status_code=404, detail="Code language not found")
        return _with_icon_url(code_language, user.id, token, image_service)
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