from uuid import UUID
from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime

from app.domain.utils import sanitize_string


class AppConfigModel(BaseModel):
    id: UUID | None = None
    key: str
    value: str
    name: str
    enabled: bool = False
    created_at: datetime | None = None

    @field_validator("key", "value", "name", mode="before")
    @classmethod
    def validate_fieds(cls, value: str) -> str:
        return sanitize_string(value)

    model_config = ConfigDict(from_attributes=True, strict=False)
    