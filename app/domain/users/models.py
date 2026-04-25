from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator
from uuid import UUID

from ..utils import sanitize_string

USERNAME_REGEX = r"^[a-zA-Z0-9._-]+$"
NAME_REGEX = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s'-]+$"

class UserProfileRole(str, Enum):
    """
    Role definitions for user profiles.
    Attributes:
        ADMIN (str): Represents an administrator role with elevated permissions.
        USER (str): Represents a regular user role.
    """
    ADMIN = "admin"
    USER = "user"

class UserProfile(BaseModel):
    """
    Data model for user profiles.
    Attributes:
        id (UUID): Unique identifier for the user profile.
        first_name (str): User's first name, must be 1-64 characters and match NAME_REGEX.
        last_name (str): User's last name, must be 1-100 characters and match NAME_REGEX.
        email (EmailStr): User's email address, must be 5-255 characters.
        username (str): User's username, must be 3-20 characters and match USERNAME_REGEX.
        is_authorized (bool): Indicates if the user is authorized to admin panel, defaults to False.
        role (UserProfileRole): Role of the user, defaults to USER.
        created_at (datetime | None): Timestamp of profile creation, optional.
    """
    id: UUID
    first_name: str = Field(..., min_length=1, max_length=64, pattern=NAME_REGEX)
    last_name: str = Field(..., min_length=1, max_length=100, pattern=NAME_REGEX)
    email: EmailStr = Field(..., min_length=5, max_length=255)
    username: str = Field( ..., min_length=3, max_length=20, pattern=USERNAME_REGEX)
    is_authorized: bool = False
    role: UserProfileRole = UserProfileRole.USER
    created_at: datetime | None = None
    @field_validator("first_name", "last_name", "username", mode="before")
    @classmethod
    def validate_fields(value: str) -> str:
       """
       Applies global sanitization to string fields to prevent XSS attacks.

       Delegates the actual sanitization logic to the sanitize_string function defined in domain.utils.sanitize_string.
       """
       return sanitize_string(value)

    model_config = ConfigDict(from_attributes=True, strict=True)