from uuid import UUID
from pydantic import BaseModel, ConfigDict, field_validator

from app.domain.utils import sanitize_string


class ProfileSettingsRequest(BaseModel):
    profile_id: UUID
    settings_id: UUID
    value: str

    @field_validator('value', mode='before')
    @classmethod
    def validate_fields(cls, value: str) -> str:
        return sanitize_string(value)

    model_config = ConfigDict(from_attributes=True, strict=False)
