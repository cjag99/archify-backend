from pydantic import BaseModel, ConfigDict, field_validator

from app.domain.utils import sanitize_string

class AppConfigRequest(BaseModel):
    """
    Data transfer object for creating or updating an application configuration.
    """
    key: str
    value: str
    name: str

    @field_validator("key", "value", "name", mode="before")
    @classmethod
    def validate_field(cls, value: str) -> str:
        """
        Validates and sanitizes string fields.
        
        Args:
            value (str): The string value to sanitize.
            
        Returns:
            str: The sanitized string.
        """
        return sanitize_string(value)

    model_config = ConfigDict(from_attributes=True, strict=False)
