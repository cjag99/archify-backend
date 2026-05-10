from abc import ABC, abstractmethod
from uuid import UUID
from .models import UserProfile

class UserPort(ABC):
    """
    Interface for user repository implementations.
    Defines the contract for data access operations related to user profiles.
    """
    @abstractmethod
    def get_user_by_id(self, user_id: UUID, token: str) -> UserProfile:
        """
        Retrieves a user profile by its unique identifier.
        Args:
            user_id (UUID): The unique identifier of the user to retrieve.
            token (str): The authentication token for the request.
        Returns:
            UserProfile: The user profile associated with the provided ID.
        """
        pass

    
    @abstractmethod
    def save_user(self, user: UserProfile) -> None:
        """
        Saves a user profile to the data store.
        Args:
            user (UserProfile): The user profile to save.
        """
        pass

    def delete_user(self, user_id: UUID) -> None:
        """
        Deletes a user profile from the data store based on its unique identifier.
        Args:
            user_id (UUID): The unique identifier of the user to delete.
        """
        pass

    def get_all_users(self, token: str) -> list[UserProfile]:
        """
        Retrieves a list of all user profiles from the data store.
        Args:
            token (str): The authentication token for the request.
        Returns:
            list[UserProfile]: A list of all user profiles.
        """
        pass