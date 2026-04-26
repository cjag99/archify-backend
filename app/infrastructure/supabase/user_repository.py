from uuid import UUID
from app.domain.users.models import UserProfile
from app.domain.users.ports import UserRepositoryPort
from .client import supabase_client

class SupabaseUserRepository(UserRepositoryPort):
    """
    Repository class to manage user profiles in the Supabase database.
    This class implements the UserRepositoryPort interface, providing methods to save and retrieve user profiles using the Supabase client.
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
                "last_name": user.last_name
            }
            self.client.from_(self.table_name).upsert(user_data).execute()
        except Exception as e:
            raise Exception(f"Failed to save user profile: {str(e)}")
        
    def get_user_by_id(self, user_id: UUID) -> UserProfile | None:
        """
        Retrieves a user profile by its unique identifier from the Supabase database.
        Args:
            user_id (UUID): The unique identifier of the user to retrieve.
        Returns:
            UserProfile | None: The user profile associated with the provided ID, or None if not found.
        Raises:
            Exception: If retrieving the user profile fails for any reason.
        """
        try:
            response = self.client.from_(self.table_name).select("*").eq("id", str(user_id)).maybe_single().execute()
            
            if not response.data:
                return None
            
            return UserProfile(
                id=UUID(response.data["id"]),
                username=response.data["username"],
                email=response.data["email"],
                first_name=response.data["first_name"],
                last_name=response.data["last_name"]
            )
        except Exception as e:
            raise Exception(f"Failed to retrieve user profile: {str(e)}")