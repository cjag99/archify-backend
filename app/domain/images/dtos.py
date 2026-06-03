from pydantic import BaseModel, ConfigDict, field_validator

from .models import ImageUsage
from ..utils import normalize_image_url, sanitize_string


class ImageRequestModel(BaseModel):
    """
    Data transfer object representing a request for an image.
    """
    file_name: str
    url: str
    usage_type: ImageUsage

    @field_validator("file_name", mode="before")
    @classmethod
    def validate_file_name(cls, value: str) -> str:
        """
        Validates and sanitizes the file name.

        Args:
            value (str): The original file name.

        Returns:
            str: The sanitized file name.
        """
        return sanitize_string(value)

    @field_validator("url", mode="before")
    @classmethod
    def validate_url(cls, value: str) -> str:
        """
        Validates and normalizes the image URL.

        Args:
            value (str): The original image URL.

        Returns:
            str: The normalized image URL.
        """
        return normalize_image_url(value)

    model_config = ConfigDict(from_attributes=True, strict=False)