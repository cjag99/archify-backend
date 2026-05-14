from uuid import UUID

from .models import ImageModel
from .dtos import ImageRequestModel
from .ports import ImagePort

class ImageServices:
    def __init__(self, port: ImagePort):
        self.port = port

    def create_image(self, image_data: ImageRequestModel, user_id: UUID, token: str) -> ImageModel:
       image = ImageModel(
           file_name=image_data.file_name,
           url=image_data.url,
           usage_type=image_data.usage_type,
           user_id=user_id
       )
       self.port.upload_image(image, token)
       return image

    def get_image_by_id(self, user_id: UUID, image_id: UUID, token: str) -> ImageModel | None:
        return self.port.get_image_by_id(image_id, token)

    def get_all_images(self, token: str) -> list[ImageModel] | None:
        return self.port.get_all_images(token)

    def get_user_images(self, user_id: UUID, token: str) -> list[ImageModel] | None:
        return self.port.get_user_images(user_id, token)

    def delete_image(self, image_id: UUID, token: str) -> None:
        self.port.delete_image(image_id, token)
