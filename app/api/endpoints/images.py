import mimetypes
from uuid import UUID
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from fastapi.params import Query

from app.api.dependencies import get_image_service, get_current_user, is_user_admin
from app.domain.images.models import ImageUsage, ImageModel
from app.domain.images.services import ImageServices
from app.domain.users.models import UserProfile

router = APIRouter()

@router.post("/")
async def upload_image(
        usage_type: ImageUsage = Query(...),
        image: UploadFile = File(),
        service: ImageServices = Depends(get_image_service),
        user_auth: tuple[UserProfile, str] = Depends(get_current_user),
):
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


@router.get("/")
async def get_all_images(
        service: ImageServices = Depends(get_image_service),
        user_auth: tuple[UserProfile, str] = Depends(is_user_admin)
):
    try:
        token = user_auth[1]
        images = service.get_all_images(token)
        if not images:
            return "No images to show"
        return images

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{image_id}")
async def get_image_by_id(
        image_id: UUID,
        service: ImageServices = Depends(get_image_service),
        user_auth: tuple[UserProfile, str] = Depends(get_current_user)
):
    try:
        user, token = user_auth
        image = service.get_image_by_id(user.id, image_id, token)
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")
        return image

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}")
async def get_user_images(
        user_id: UUID,
        service: ImageServices = Depends(get_image_service),
        user_auth: tuple[UserProfile, str] = Depends(get_current_user)
):
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

@router.delete("/{image_id}")
async def delete_image(
    image_id: UUID,
    service: ImageServices = Depends(get_image_service),
    user_auth: tuple[UserProfile, str] = Depends(is_user_admin)
):
    try:
        user, token = user_auth

        service.delete_image(image_id, token)

        return {"success": True}

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))