from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator

from app.domain.utils import sanitize_string
from app.domain.jsonb_type import JsonDict



class PatternRequestModel(BaseModel):
    name: str
    description: str | None = None
    base_structure: JsonDict | None = None
    image_id: UUID | None = None

    @field_validator("name", "description", mode="before")
    @classmethod
    def validate_fields(cls, value: str) -> str:
        """
        Applies global sanitization to string fields to prevent XSS attacks.

        Delegates the actual sanitization logic to the sanitize_string function defined in domain.utils.sanitize_string.
        """
        return sanitize_string(value)

    model_config = ConfigDict(from_attributes=True, strict=False)
