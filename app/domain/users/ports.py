from abc import ABC, abstractmethod
from uuid import UUID
from .models import UserProfile

class UserRepositoryPort(ABC):
    """
    Interface for user repository implementations.
    Defines the contract for data access operations related to user profiles.
    """
    @abstractmethod
    def get_user_by_id(self, user_id: UUID) -> UserProfile:
        """
        Retrieves a user profile by its unique identifier.
        Args:
            user_id (UUID): The unique identifier of the user to retrieve.
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