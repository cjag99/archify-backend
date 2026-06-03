from uuid import UUID

from .models import ImageModel, ImageUsage
from .ports import ImagePort

class ImageServices:
    """
    Service class handling business logic for image operations.
    """
    def __init__(self, port: ImagePort):
        """
        Initializes the ImageServices with a specific port.

        Args:
            port (ImagePort): The image port implementation.
        """
        self.port = port

    def create_image(self, file_bytes: bytes, file_name: str, content_type: str, usage_type: ImageUsage, user_id: UUID, token: str) -> ImageModel:
        """
        Creates a new image.

        Args:
            file_bytes (bytes): The raw byte content of the image.
            file_name (str): The name of the file.
            content_type (str): The MIME type of the file.
            usage_type (ImageUsage): The intended usage of the image.
            user_id (UUID): The ID of the user.
            token (str): The authorization token.

        Returns:
            ImageModel: The newly created image.
        """
        return self.port.upload_image(file_bytes, file_name, content_type, usage_type, user_id, token)

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
        return self.port.get_image_by_id(user_id=user_id, image_id=image_id, token=token)

    def get_all_images(self, token: str) -> list[ImageModel] | None:
        """
        Retrieves all images.

        Args:
            token (str): The authorization token.

        Returns:
            list[ImageModel] | None: A list of all images, or None.
        """
        return self.port.get_all_images(token)

    def get_user_images(self, user_id: UUID, token: str) -> list[ImageModel] | None:
        """
        Retrieves all images belonging to a specific user.

        Args:
            user_id (UUID): The ID of the user.
            token (str): The authorization token.

        Returns:
            list[ImageModel] | None: A list of the user's images, or None.
        """
        return self.port.get_user_images(user_id, token)

    def delete_image(self, image_id: UUID, token: str) -> None:
        """
        Deletes an image by its ID.

        Args:
            image_id (UUID): The ID of the image to delete.
            token (str): The authorization token.
        """
        self.port.delete_image(image_id, token)
