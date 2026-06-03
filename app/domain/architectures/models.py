from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, field_validator

from app.domain.jsonb_type import JsonDict
from app.domain.utils import sanitize_string


class ArchitectureModel(BaseModel):
    """
    Domain model representing an architecture.
    """
    id: UUID | None = None
    name: str
    description: str
    base_structure: JsonDict | None = None
    enabled: bool = False
    created_at: datetime | None = None

    @field_validator("name", "description", mode='before')
    @classmethod
    def validate_field(cls, value: str) -> str:
        """
        Validates and sanitizes string fields.
        
        Args:
            value (str): The string value to sanitize.
            
        Returns:
            str: The sanitized string.
        """
        return sanitize_string(value)

    model_config = ConfigDict(from_attributes=True, strict=False)