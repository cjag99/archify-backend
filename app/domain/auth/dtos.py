from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator

from ..users.models import NAME_REGEX, USERNAME_REGEX
from ..utils import sanitize_string
class UserRegistrationRequest(BaseModel):
    """
    Data model for user registration requests.
    Attributes:
        first_name (str): User's first name, must be 1-64 characters.
        last_name (str): User's last name, must be 1-100 characters.
        email (EmailStr): User's email address, must be 5-255 characters.
        username (str): User's username, must be 3-20 characters.
        password (str): User's password, must be 8-128 characters.
    """
    first_name: str = Field(..., min_length=1, max_length=64, pattern=NAME_REGEX)
    last_name: str = Field(..., min_length=1, max_length=100, pattern=NAME_REGEX)
    email: EmailStr = Field(..., min_length=5, max_length=255)
    username: str = Field(..., min_length=3, max_length=20, pattern=USERNAME_REGEX)
    password: str = Field(..., min_length=8, max_length=128)


    @field_validator("first_name", "last_name", "username", mode="before")
    @classmethod
    def validate_fields(cls, value: str) -> str:
       """
       Applies global sanitization to string fields to prevent XSS attacks.

       Delegates the actual sanitization logic to the sanitize_string function defined in domain.utils.sanitize_string.
       """
       return sanitize_string(value)
    
    model_config = ConfigDict(from_attributes=True, strict=True)


class UserLoginRequest(BaseModel):
    """
    Data model for user login requests.
    Attributes:
        email (EmailStr): User's email address, must be 5-255 characters.
        password (str): User's password, must be 8-128 characters.
    """
    email: EmailStr = Field(..., min_length=5, max_length=255)
    password: str = Field(..., min_length=8, max_length=128)

    model_config = ConfigDict(from_attributes=True, strict=True)