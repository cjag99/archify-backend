from pydantic import BaseModel, ConfigDict, field_validator

from app.domain.utils import sanitize_string

class AppConfigRequest(BaseModel):
    key: str
    value: str
    name: str

    @field_validator("key", "value", "name", mode="before")
    @classmethod
    def validate_field(cls, value: str) -> str:
        return sanitize_string(value)

    model_config = ConfigDict(from_attributes=True, strict=False)
