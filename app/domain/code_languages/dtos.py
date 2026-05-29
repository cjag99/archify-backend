from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, field_validator

from app.domain.utils import sanitize_string
from .models import CodeLanguagesModel

class CodeLanguagesRequest(BaseModel):
    name: str
    file_extension: str
    icon: UUID | None = None

    @field_validator("name", "file_extension", mode='before')
    @classmethod
    def validate_field(cls, value: str) -> str:
        return sanitize_string(value)

    model_config = ConfigDict(from_attributes=True, strict=False)


class CodeLanguagesResponse(BaseModel):
    id: UUID | None = None
    name: str
    file_extension: str
    icon: UUID | None = None
    icon_url: str | None = None
    created_at: datetime | None = None

    @classmethod
    def from_model(cls, model: CodeLanguagesModel, icon_url: str | None = None) -> "CodeLanguagesResponse":
        return cls(
            id=model.id,
            name=model.name,
            file_extension=model.file_extension,
            icon=model.icon,
            icon_url=icon_url,
            created_at=model.created_at,
        )

    model_config = ConfigDict(from_attributes=True, strict=False)
