from uuid import UUID

from .client import supabase_client
from ...domain.patterns.models import PatternModel
from ...domain.patterns.ports import PatternPort


class SupabasePatternRepository(PatternPort):
    """
    Repository class to manage patterns in the Supabase database.
    This class implements the PatternPort interface, providing methods to save and retrieve patterns using the Supabase client.
    """
    def __init__(self):
        self.client = supabase_client
        self.table_name = "patterns"

    def save_pattern(self, pattern: PatternModel, token: str) -> None:
        """
        Saves a profile to the Supabase database.
        Args:
            pattern (PatternModel): The pattern to save.
            token (str): The autheunticated user bearer token.
        Raises:
            Exception: If saving the pattern fails for any reason.
        """
        try:
            pattern_dict = pattern.model_dump(exclude_none=True)
            if pattern_dict.get("id") is not None:
                pattern_dict["id"] = str(pattern_dict["id"])
            if pattern_dict.get("created_at") is not None:
                pattern_dict["created_at"] = pattern_dict["created_at"].isoformat()

            self.client.postgrest.auth(token)
            response = self.client.from_(self.table_name).upsert(pattern_dict).execute()
            if hasattr(response, 'error') and response.error:
                print(f"Database unexpected error: {response.error}")
                raise Exception(response.error['message'])

            if getattr(response, "data", None):
                res_data = response.data[0]
                if not pattern.id and res_data.get("id"):
                    pattern.id = UUID(res_data["id"])
                if not pattern.created_at and res_data.get("created_at"):
                    from datetime import datetime
                    pattern.created_at = datetime.fromisoformat(res_data["created_at"].replace("Z", "+00:00"))

        except Exception as e:
            print(f"Error occurred while saving pattern: {e}")

    def get_pattern_by_id(self, pattern_id: UUID) -> PatternModel | None:
        """
        Retrieves a pattern by its unique identifier from the Supabase database.
        Args:
            pattern_id (UUID): The unique identifier of the pattern to retrieve.
        Returns:
            PatternModeul | None: The pattern associated with the provided ID, or None if not found.
        Raises:
            Exception: If retrieving the pattern fails for any reason.
        """
        try:
            res = self.client.from_(self.table_name).select("*").eq("id", str(pattern_id)).execute()
            if not getattr(res, "data", None):
                return None

            return PatternModel(**res.data[0])

        except Exception as e:
            print(f"Error occurred while retrieving pattern: {e}")
            return None

    def get_all_patterns(self) -> list[PatternModel] | None:
        """
        Retrieves all patterns from the Supabase database.
        Returns:
            list[PatternModel] | None: The list of all patterns, or None if not found.
        Raises:
            Exception: If retrieving all pattern fails for any reason.
        """
        try:
            res = self.client.from_(self.table_name).select("*").execute()
            if not getattr(res, "data", None):
                return None

            return [PatternModel(**row) for row in res.data]

        except Exception as e:
            print(f"Error occurred while retrieving all patterns: {e}")
            return None

    def delete_pattern(self, pattern_id: UUID, token: str) -> None:
        """
        Deletes a pattern from the Supabase database based on its unique identifier.
        Args:
            pattern_id (UUID): The unique identifier of the pattern to delete.
            token (str): The authentication token for the request.
        Raises:
            Exception: If deleting the pattern fails for any reason.
        """
        try:
            self.client.postgrest.auth(token)
            self.client.from_(self.table_name).delete().eq("id", pattern_id).execute()

        except Exception as e:
            print(f"Error occurred while deleting pattern: {e}")
