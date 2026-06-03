from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, field_validator

from app.domain.utils import sanitize_string
from app.domain.jsonb_type import JsonDict

class PatternModel(BaseModel):
    """
    Data model representing a design pattern within the application.

    Attributes:
        id (UUID | None): Unique identifier for the pattern.
        name (str): Name of the pattern.
        description (str): Explanation of the pattern.
        base_structure (JsonDict | None): Optional JSON containing node positions for the pattern schema.
        image_id (UUID | None): Optional unique identifier for an associated image.
        created_at (datetime | None): Timestamp indicating when the pattern was created.
    """
    id: UUID | None = None
    name: str
    description: str
    base_structure: JsonDict | None = None
    image_id: UUID | None = None
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True, strict=False)