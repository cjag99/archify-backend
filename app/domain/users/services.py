from uuid import UUID
from .models import UserProfile, UserUpdateRequest
from .ports import UserPort

class UserService:
    """
    Application Service that manages user-related operations.
    
    This service acts as a facade, coordinating the UserPort (domain data).
    """

    def __init__(self, user_port: UserPort):
        self.user_port = user_port

    def get_user_by_id(self, user_id: UUID, token: str) -> UserProfile:
        """
        Retrieves a user's profile by their ID.
        
        Args:
            user_id (UUID): The unique identifier of the user.
            token (str): The authentication token for the request.
        Returns:
            UserProfile: The user's profile information.
        Raises:
            ValueError: If no user is found with the given ID.
        """
        user_profile = self.user_port.get_user_by_id(user_id, token)
        if not user_profile:
            raise ValueError(f"User with ID {user_id} not found")
        return user_profile
    
    def delete_user(self, user_id: UUID, token: str) -> None:
        """
        Deletes a user by their ID.
        
        Args:
            user_id (UUID): The unique identifier of the user to delete.
            token (str): The authentication token for the request.
        Raises:
            ValueError: If no user is found with the given ID.
        """
        user_profile = self.user_port.get_user_by_id(user_id, token)
        if not user_profile:
            raise ValueError(f"User with ID {user_id} not found")
        self.user_port.delete_user(user_id, token)

    def update_user_profile(self, user_id: UUID, update_req: "UserUpdateRequest", token: str) -> UserProfile:
        """
        Updates a user's profile information.
        
        Args:
            user_id (UUID): The unique identifier of the user to update.
            update_req (UserUpdateRequest): The updated profile information.
            token (str): The authentication token for the request.
        Returns:
            UserProfile: The updated user profile.
        Raises:
            ValueError: If no user is found with the given ID.
        """
        existing_profile = self.user_port.get_user_by_id(user_id, token)
        if not existing_profile:
            raise ValueError(f"User with ID {user_id} not found")
        
        update_data = update_req.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                setattr(existing_profile, key, value)
        
        self.user_port.save_user(existing_profile)
        return existing_profile
    
    def get_all_users(self, token: str) -> list[UserProfile]:
        """
        Retrieves a list of all user profiles.
        
        Args:
            token (str): The authentication token for the request.
        Returns:
            list[UserProfile]: A list of all user profiles.
        """
        return self.user_port.get_all_users(token)