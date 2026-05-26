from uuid import UUID
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from fastapi.params import Query

from app.api.dependencies import get_image_service, get_current_user, is_user_admin
from app.domain.images.dtos import ImageRequestModel
from app.domain.images.models import ImageUsage
from app.domain.images.services import ImageServices
from app.domain.users.models import UserProfile
from app.infrastructure.supabase.client import supabase_client

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
        content_type = image.content_type or "image/jpeg"
        image_path = f"{user_uuid}/{image.filename}"

        storage_response = supabase_client.storage.from_("archify").upload(
            path=image_path,
            file=image_bytes,
            file_options={"contentType": content_type}
        )

        image_url = supabase_client.storage.from_("archify").get_public_url(image_path)
        data = ImageRequestModel(
            file_name=image.filename,
            url=image_url,
            usage_type=usage_type
        )
        created = service.create_image(data, user_uuid, token)
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

@router.delete("/{image_id}")
async def delete_image(
        image_id: UUID,
        service: ImageServices = Depends(get_image_service),
        user_auth: tuple[UserProfile, str] = Depends(is_user_admin)
):
    try:
        user, token = user_auth
        image = service.get_image_by_id(user_id=user.id, image_id=image_id, token=token)
        if image:
            supabase_client.storage.from_("archify").remove(image.url)
            service.delete_image(image_id, token)
            return
        raise HTTPException(status_code=404, detail="Image not found")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))
