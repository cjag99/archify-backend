from pydantic import BaseModel, ConfigDict, field_validator
from uuid import UUID

from app.domain.utils import sanitize_string
from ..jsonb_type import JsonDict

class ProjectCreateModel(BaseModel):
    """
    Data model for creating a new project.
    Attributes:
        name (str): Name of the project, must be 1-255 characters.
        description (str | None): Optional description of the project, must be 1-1000 characters if provided.
    """
    name: str
    description: str | None = None
    project_logo: UUID | None = None
    architecture: JsonDict | None = None
    user_id: UUID

    @field_validator("name", "description", mode="before")
    @classmethod
    def validate_fields(cls, value: str) -> str:
        if value is None:
            return value
        return sanitize_string(value)
    
    model_config = ConfigDict(from_attributes=True, strict=False)

