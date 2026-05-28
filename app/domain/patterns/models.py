from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, field_validator

from app.domain.utils import sanitize_string
from app.domain.jsonb_type import JsonDict

class PatternModel(BaseModel):
    """
    Data model representing a desing pattern within the application
    Attributes:
        id (UUID): Unique identifier for the pattern.
        name (str): Name of the pattern.
        description (str): Explanation of the pattern.
        base_structure (JsonDict | None): Optional JSON containing nodes positions for pattern schema.
        created_at (datetime): Timestamp indicating when the pattern was created.
    """
    id: UUID | None = None
    name: str
    description: str
    base_structure: JsonDict | None = None
    image_id: UUID | None = None
    created_at: datetime | None = None

    @field_validator("name", "description", mode="before")
    @classmethod
    def validate_fields(cls, value: str) -> str:
        """
        Applies global sanitization to string fields to prevent XSS attacks.

        Delegates the actual sanitization logic to the sanitize_string function defined in domain.utils.sanitize_string.
        """
        return sanitize_string(value)

    model_config = ConfigDict(from_attributes=True, strict=False)