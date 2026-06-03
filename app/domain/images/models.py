from enum import Enum
from uuid import UUID
from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime

from app.domain.utils import normalize_image_url, sanitize_string


class ImageUsage(str, Enum):
    """
    Enumeration defining the allowed usage types for an image.
    """
    LOGO = "project_logo"
    AVATAR = "avatar"
    REACT_NODE = "react_node"
    CODE_LOGO = "code_logo"
    PATTERN_GRAPHIC = "pattern_graphic"

class ImageModel(BaseModel):
    """
    Domain model representing an image entity.
    """
    id: UUID | None = None
    file_name: str
    url: str
    user_id: UUID | None = None
    usage_type: ImageUsage
    created_at: datetime | None = None

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
