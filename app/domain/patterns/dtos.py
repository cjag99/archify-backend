from typing import Dict, Any
from pydantic import BaseModel, ConfigDict, field_validator
from app.domain.utils import sanitize_string

JsonDict = Dict[str, Any]

class PatternRequestModel(BaseModel):
    name: str
    description: str
    base_structure: JsonDict | None = None

    @field_validator("name", "description", mode="before")
    @classmethod
    def validate_fields(cls, value: str) -> str:
        """
        Applies global sanitization to string fields to prevent XSS attacks.

        Delegates the actual sanitization logic to the sanitize_string function defined in domain.utils.sanitize_string.
        """
        return sanitize_string(value)

    model_config = ConfigDict(from_attributes=True, strict=True)
