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


@router.get("/", response_model=list[CodeLanguagesResponse] | str)
async def get_all_code_languages(
        service: CodeLanguagesService = Depends(get_code_language_service),
        image_service: ImageServices = Depends(get_image_service),
        user_auth: tuple[UserProfile, str] = Depends(get_current_user)
) -> list[CodeLanguagesResponse] | str:
    """
    Get all code languages.

    Retrieves a list of all available code languages, including their icon URLs if present.
    Returns a list of CodeLanguagesResponse or a string if none are found.
    """
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

@router.get("/{code_language_id}", response_model=CodeLanguagesResponse)
async  def get_code_language_by_id(
        code_language_id: UUID,
        service: CodeLanguagesService = Depends(get_code_language_service),
        image_service: ImageServices = Depends(get_image_service),
        user_auth: tuple[UserProfile, str] = Depends(get_current_user)
) -> CodeLanguagesResponse:
    """
    Get code language by ID.

    Retrieves a specific code language by its unique identifier, including its icon URL.
    """
    try:
        user, token = user_auth
        code_language = service.get_code_language_by_id(code_language_id, token)
        if not code_language:
            raise HTTPException(status_code=404, detail="Code language not found")
        return _with_icon_url(code_language, user.id, token, image_service)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/", response_model=CodeLanguagesModel)
async def create_code_language(
        data: CodeLanguagesRequest,
        service: CodeLanguagesService = Depends(get_code_language_service),
        user_auth: tuple[UserProfile, str] = Depends(is_user_admin)
) -> CodeLanguagesModel:
    """
    Create a new code language.

    Creates a new code language in the system. Requires admin privileges.
    """
    try:
        token = user_auth[1]
        code_language = service.create_code_language(data, token)
        return  code_language
    except Exception as e:
        raise  HTTPException(status_code=400, detail=str(e))

@router.patch("/{code_language_id}", response_model=CodeLanguagesModel)
async def update_code_language(
        code_language_id: UUID,
        data: CodeLanguagesRequest,
        service: CodeLanguagesService = Depends(get_code_language_service),
        user_auth: tuple[UserProfile, str] = Depends(is_user_admin)
) -> CodeLanguagesModel:
    """
    Update a code language.

    Updates the specified code language. Requires admin privileges.
    """
    try:
        token = user_auth[1]
        code_language = service.update_code_language(code_language_id, data, token)
        return code_language
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{code_language_id}", status_code=204)
async def delete_code_language(
        code_language_id: UUID,
        service: CodeLanguagesService = Depends(get_code_language_service),
        user_auth: tuple[UserProfile, str] = Depends(is_user_admin)
) -> None:
    """
    Delete a code language.

    Deletes the specified code language from the system. Requires admin privileges.
    """
    try:
        token = user_auth[1]
        service.delete_code_language(code_language_id, token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))