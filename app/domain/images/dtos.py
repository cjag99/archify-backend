from pydantic import BaseModel, ConfigDict, field_validator

from .models import ImageUsage
from ..utils import sanitize_string


class ImageRequestModel(BaseModel):
    file_name: str
    url: str
    usage_type: ImageUsage

    @field_validator("file_name", "url", mode="before")
    @classmethod
    def validate_fields(cls, value: str) -> str:
        return sanitize_string(value)

    model_config = ConfigDict(from_attributes=True, strict=False)