from uuid import UUID
from datetime import datetime
from app.domain.users.models import UserProfile, UserProfileRole
from app.domain.users.ports import UserPort
from .client import supabase_client

class SupabaseUserRepository(UserPort):
    """
    Repository class to manage user profiles in the Supabase database.
    This class implements the UserPort interface, providing methods to save and retrieve user profiles using the Supabase client.
    """

    def __init__(self):
        self.client = supabase_client
        self.table_name = "profiles"

    def save_user(self, user: UserProfile) -> None:
        """
        Saves a user profile to the Supabase database.
        Args:
            user (UserProfile): The user profile to save.
        Raises:
            Exception: If saving the user profile fails for any reason.
        """
        try:
            user_data = {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_authorized": user.is_authorized,
                "role": user.role.value,
                "created_at": user.created_at.isoformat() if user.created_at else datetime.utcnow().isoformat()
            }
            self.client.from_(self.table_name).upsert(user_data).execute()
        except Exception as e:
            raise Exception(f"Failed to save user profile: {str(e)}")
        
    def get_user_by_id(self, user_id: UUID, token: str) -> UserProfile | None:
        """
        Retrieves a user profile by its unique identifier from the Supabase database.
        Args:
            user_id (UUID): The unique identifier of the user to retrieve.
            token (str): The authentication token for the request.
        Returns:
            UserProfile | None: The user profile associated with the provided ID, or None if not found.
        Raises:
            Exception: If retrieving the user profile fails for any reason.
        """
        try:
            self.client.postgrest.auth(token)
            response = self.client.from_(self.table_name).select("*").eq("id", str(user_id)).execute()
            
            if not getattr(response, "data", None):
                return None
                
            data = response.data[0]
            
            return UserProfile(
                id=UUID(data["id"]),
                username=data.get("username"),
                email=data.get("email"),
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                is_authorized=data.get("is_authorized"),
                role=UserProfileRole(data.get("role", "user")),
                created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None
            )
        except Exception as e:
            raise Exception(f"Failed to retrieve user profile: {str(e)}")
        
    def delete_user(self, user_id: UUID, token: str) -> None:
        """
        Deletes a user profile from the Supabase database based on its unique identifier.
        Args:
            user_id (UUID): The unique identifier of the user to delete.
            token (str): The authentication token for the request.
        Raises:            
            Exception: If deleting the user profile fails for any reason.
        """
        try:
            self.client.postgrest.auth(token)
            self.client.from_(self.table_name).delete().eq("id", str(user_id)).execute()
        except Exception as e:
            raise Exception(f"Failed to delete user profile: {str(e)}")
        
    def get_all_users(self, token: str) -> list[UserProfile]:
        """
        Retrieves a list of all user profiles from the Supabase database.
        Args:
            token (str): The authentication token for the request.
        Returns:
            list[UserProfile]: A list of all user profiles.
        Raises:
            Exception: If retrieving the list of user profiles fails for any reason.
        """
        try:
            self.client.postgrest.auth(token)
            response = self.client.from_(self.table_name).select("*").execute()
            if not getattr(response, "data", None):
                return None
            return [UserProfile(**row) for  row in response.data]
        except Exception as e:
            raise Exception(f"Failed to retrieve user profiles: {str(e)}")
        
    def update_user(self, updated_user: UserProfile, token: str) -> None:
        """
        Updates a user profile in the Supabase database based on its unique identifier.
        Args:
            updated_user (UserProfile): The updated user profile information.
            token (str): The authentication token for the request.
        Raises:
            Exception: If updating the user profile fails for any reason.
        """
        self.client.postgrest.auth(token)
        return self.save_user(updated_user)