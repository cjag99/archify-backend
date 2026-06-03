from uuid import UUID
from abc import ABC, abstractmethod

from .models import ImageModel, ImageUsage

class ImagePort(ABC):
    @abstractmethod
    def upload_image(self, file_bytes: bytes, file_name: str, content_type: str, usage_type: ImageUsage, user_id: UUID, token: str) -> ImageModel:
        pass

    @abstractmethod
    def get_image_by_id(self, user_id: UUID, image_id: UUID, token: str) -> ImageModel | None:
        pass

    @abstractmethod
    def get_all_images(self, token: str) -> list[ImageModel] | None:
        pass

    @abstractmethod
    def get_user_images(self, user_id: UUID, token: str) -> list[ImageModel] | None:
        pass

    @abstractmethod
    def delete_image(self, image_id: UUID, token: str) -> None:
        pass
