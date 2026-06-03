import mimetypes
from uuid import UUID
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from fastapi.params import Query

from app.api.dependencies import get_image_service, get_current_user, is_user_admin
from app.domain.images.models import ImageUsage, ImageModel
from app.domain.images.services import ImageServices
from app.domain.users.models import UserProfile

router = APIRouter()

@router.post("/", response_model=dict)
async def upload_image(
        usage_type: ImageUsage = Query(...),
        image: UploadFile = File(),
        service: ImageServices = Depends(get_image_service),
        user_auth: tuple[UserProfile, str] = Depends(get_current_user),
) -> dict:
    """
    Upload a new image.

    Uploads a new image file and creates a record in the database.
    """
    try:
        user, token = user_auth
        user_uuid = str(user.id)
        image_bytes = await image.read()
        content_type = image.content_type
        if not content_type or content_type == "application/octet-stream":
            guessed, _ = mimetypes.guess_type(image.filename or "")
            content_type = guessed or "image/jpeg"
        created = service.create_image(
            file_bytes=image_bytes,
            file_name=image.filename or "image",
            content_type=content_type,
            usage_type=usage_type,
            user_id=UUID(user_uuid),
            token=token
        )
        return created.model_dump()

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=list[ImageModel] | str)
async def get_all_images(
        service: ImageServices = Depends(get_image_service),
        user_auth: tuple[UserProfile, str] = Depends(is_user_admin)
) -> list[ImageModel] | str:
    """
    Get all images.

    Retrieves a list of all images in the system. Requires admin privileges.
    Returns a list of ImageModel or a string if none are found.
    """
    try:
        token = user_auth[1]
        images = service.get_all_images(token)
        if not images:
            return "No images to show"
        return images

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{image_id}", response_model=ImageModel)
async def get_image_by_id(
        image_id: UUID,
        service: ImageServices = Depends(get_image_service),
        user_auth: tuple[UserProfile, str] = Depends(get_current_user)
) -> ImageModel:
    """
    Get image by ID.

    Retrieves a specific image by its unique identifier.
    """
    try:
        user, token = user_auth
        image = service.get_image_by_id(user.id, image_id, token)
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")
        return image

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/user/{user_id}", response_model=list[ImageModel] | str)
async def get_user_images(
        user_id: UUID,
        service: ImageServices = Depends(get_image_service),
        user_auth: tuple[UserProfile, str] = Depends(get_current_user)
) -> list[ImageModel] | str:
    """
    Get user images.

    Retrieves all images associated with a specific user.
    """
    try:
        user, token = user_auth
        if user_id != user.id:
            raise HTTPException(status_code=403, detail="User not authorized to get images")
        images = service.get_user_images(user_id, token)
        if not images:
            return "No images to show"
        return images

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{image_id}", status_code=204)
async def delete_image(
    image_id: UUID,
    service: ImageServices = Depends(get_image_service),
    user_auth: tuple[UserProfile, str] = Depends(is_user_admin)
) -> None:
    """
    Delete an image.

    Deletes the specified image from the system. Requires admin privileges.
    """
    try:
        user, token = user_auth

        service.delete_image(image_id, token)

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))