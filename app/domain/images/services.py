from uuid import UUID

from .models import ImageModel, ImageUsage
from .ports import ImagePort

class ImageServices:
    def __init__(self, port: ImagePort):
        self.port = port

    def create_image(self, file_bytes: bytes, file_name: str, content_type: str, usage_type: ImageUsage, user_id: UUID, token: str) -> ImageModel:
       return self.port.upload_image(file_bytes, file_name, content_type, usage_type, user_id, token)

    def get_image_by_id(self, user_id: UUID, image_id: UUID, token: str) -> ImageModel | None:
        return self.port.get_image_by_id(user_id=user_id, image_id=image_id, token=token)

    def get_all_images(self, token: str) -> list[ImageModel] | None:
        return self.port.get_all_images(token)

    def get_user_images(self, user_id: UUID, token: str) -> list[ImageModel] | None:
        return self.port.get_user_images(user_id, token)

    def delete_image(self, image_id: UUID, token: str) -> None:
        self.port.delete_image(image_id, token)
