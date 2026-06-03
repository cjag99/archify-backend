from uuid import UUID
from abc import ABC, abstractmethod

from .models import ImageModel, ImageUsage

class ImagePort(ABC):
    """
    Abstract base class defining the port interface for image operations.
    """
    @abstractmethod
    def upload_image(self, file_bytes: bytes, file_name: str, content_type: str, usage_type: ImageUsage, user_id: UUID, token: str) -> ImageModel:
        """
        Uploads an image.

        Args:
            file_bytes (bytes): The raw byte content of the image.
            file_name (str): The name of the file.
            content_type (str): The MIME type of the file.
            usage_type (ImageUsage): The intended usage of the image.
            user_id (UUID): The ID of the user uploading the image.
            token (str): The authorization token.

        Returns:
            ImageModel: The uploaded image model.
        """
        pass

    @abstractmethod
    def get_image_by_id(self, user_id: UUID, image_id: UUID, token: str) -> ImageModel | None:
        """
        Retrieves an image by its ID.

        Args:
            user_id (UUID): The ID of the user.
            image_id (UUID): The ID of the image.
            token (str): The authorization token.

        Returns:
            ImageModel | None: The requested image if found, else None.
        """
        pass

    @abstractmethod
    def get_all_images(self, token: str) -> list[ImageModel] | None:
        """
        Retrieves all images.

        Args:
            token (str): The authorization token.

        Returns:
            list[ImageModel] | None: A list of all images, or None.
        """
        pass

    @abstractmethod
    def get_user_images(self, user_id: UUID, token: str) -> list[ImageModel] | None:
        """
        Retrieves all images belonging to a specific user.

        Args:
            user_id (UUID): The ID of the user.
            token (str): The authorization token.

        Returns:
            list[ImageModel] | None: A list of the user's images, or None.
        """
        pass

    @abstractmethod
    def delete_image(self, image_id: UUID, token: str) -> None:
        """
        Deletes an image by its ID.

        Args:
            image_id (UUID): The ID of the image to delete.
            token (str): The authorization token.
        """
        pass
