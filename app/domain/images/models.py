from enum import Enum
from uuid import UUID
from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime

from app.domain.utils import sanitize_string


class ImageUsage(str, Enum):
    LOGO = "project_logo"
    AVATAR = "avatar"
    REACT_NODE = "react_node"
    CODE_LOGO = "code_logo"
    PATTERN_GRAPHIC = "pattern_graphic"

class ImageModel(BaseModel):
    id: UUID | None = None
    file_name: str
    url: str
    user_id: UUID | None = None
    usage_type: ImageUsage
    created_at: datetime | None = None

    @field_validator("file_name", "url", mode="before")
    @classmethod
    def validate_field(cls, value: str) -> str:
        return sanitize_string(value)

    model_config = ConfigDict(from_attributes=True, strict=False)
