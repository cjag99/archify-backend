from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, field_validator

from app.domain.utils import sanitize_string


class CodeLanguagesModel(BaseModel):
    """
    Domain model for a code language.
    """
    id: UUID | None = None
    name: str
    file_extension: str
    icon: UUID | None = None
    created_at: datetime | None = None
    @field_validator("name", "file_extension", mode='before')
    @classmethod
    def validate_field(cls, value: str) -> str:
        """
        Validate and sanitize string fields.

        Args:
            value (str): The string value to validate.

        Returns:
            str: The sanitized string.
        """
        return sanitize_string(value)

    model_config = ConfigDict(from_attributes=True, strict=False)
