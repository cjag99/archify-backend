from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, field_validator
from ..jsonb_type import JsonDict

from app.domain.utils import sanitize_string


class ProjectModel(BaseModel):
    """
    Data model representing a project within the application.
    Attributes:
        id (UUID): Unique identifier for the project.
        name (str): Name of the project.
        description (str | None): Optional description of the project.
        user_id (UUID): Unique identifier of the user who owns the project.
        project_logo (UUID | None): Optional unique identifier for the project's logo image.
        architecture (UUID | None): Optional unique identifier for the project's architecture structure.
        created_at (datetime | None): Timestamp indicating when the project was created.
    """
    id: UUID | None = None
    name: str
    description: str | None = None
    user_id: UUID
    project_logo: UUID | None = None
    architecture: JsonDict | None = None
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True, strict=False)