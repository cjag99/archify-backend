"""
Ports and interfaces for authentication domain.
"""
from abc import ABC, abstractmethod
from uuid import UUID
from .dtos import UserLoginRequest, UserRegistrationRequest

class AuthException(Exception):
    """
    Base exception class for authentication-related errors.
    """
    pass


class AuthPort(ABC):
    """
    Interface for authentication providers.
    Defines the contract for external identity management (e.g., Supabase Auth).
    """
    @abstractmethod
    def register_user(self, registration_request: UserRegistrationRequest) -> UUID:
        """
        Registers a new user based on the provided registration request data.
        Args:
            registration_request (UserRegistrationRequest): The data required to register a new user.
        Returns:
            UUID: The unique identifier of the newly registered user.
        """
        pass

    @abstractmethod
    def login_user(self, login_request: UserLoginRequest) -> dict:
        """
        Authenticates a user based on the provided login request data and returns an authentication token.
        Args:
            login_request (UserLoginRequest): The data required to authenticate a user.
        Returns:
            dict: A dictionary containing the authentication token and user information for the authenticated user.
        """        
        pass

    @abstractmethod
    def logout_user(self, token: str) -> None:
        """
        Logs out the user associated with the provided authentication token.
        Args:
            token (str): The authentication token of the user to log out.
        """
        pass

    @abstractmethod
    def verify_token(self, token: str) -> UUID:
        """
        Retrieves the unique identifier of a user based on their authentication token.
        Args:
            token (str): The authentication token of the user.
        Returns:
            UUID: The unique identifier of the user associated with the provided token.
        """
        pass

    @abstractmethod
    def update_password(self, user_id: UUID, new_password: str) -> None:
        """
        Updates the password of a user.
        Args:
            user_id (UUID): The unique identifier of the user.
            new_password (str): The new password for the user.
        """
        pass