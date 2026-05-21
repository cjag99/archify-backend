from pydantic import BaseModel, ConfigDict, field_validator

from app.domain.jsonb_type import JsonDict
from app.domain.utils import sanitize_string


class SettingsRequest(BaseModel):
    name: str
    values: JsonDict

    @field_validator("name", mode="before")
    @classmethod
    def validate_fields(cls, value: str) -> str:
        return sanitize_string(value)

    model_config = ConfigDict(from_attributes=True, strict=False)
