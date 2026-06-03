from uuid import UUID

from .client import supabase_client
from app.domain.patterns_code.models import PatternsCodeModel
from app.domain.patterns_code.ports import PatternsCodePort

class SupabasePatternCodeRepository(PatternsCodePort):
    """
    Repository class to manage pattern code snippets in the Supabase database.
    This class implements the PatternsCodePort interface, providing methods to save and retrieve patterns code snippets using the Supabase client.
    """
    def __init__(self):
        """
        Initializes the SupabasePatternCodeRepository with the Supabase client and sets the table name.
        """
        self.client = supabase_client
        self.table_name = "patterns_code"

    def save_pattern_code(self, data: PatternsCodeModel, token: str) -> None:
        """
        Saves a pattern code snippet to the Supabase database.
        Args:
            data (PatternsCodeModel): The pattern code snippet to save.
            token (str): The autheuntication token for the request.
        Raises:
            Exception: If saving the snippet fails for any reason.
        """
        try:
            pattern_code_dict = data.model_dump(exclude_none=True)

            if pattern_code_dict.get("pattern_id") is not None:
                pattern_code_dict["pattern_id"] = str(pattern_code_dict["pattern_id"])

            if pattern_code_dict.get("code_id") is not None:
                pattern_code_dict["code_id"] = str(pattern_code_dict["code_id"])
            
            if pattern_code_dict.get("created_at") is not None:
                pattern_code_dict["created_at"] = pattern_code_dict["created_at"].isoformat()

            print(f"DEBUG BACKEND - Datos que van a Supabase: {pattern_code_dict}")
            self.client.postgrest.auth(token)
            response = self.client.from_(self.table_name).upsert(pattern_code_dict).execute()

            if hasattr(response, 'error') and response.error:
                print(f"Database unexpected error: {response.error}")
                raise Exception(response.error['message'])
            
            if getattr(response, "data", None):
                res_data = response.data[0]
                if not data.created_at and res_data.get("created_at"):
                    from datetime import datetime
                    data.created_at = datetime.fromisoformat(res_data["created_at"].replace("Z", "+00:00"))

        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Error occured while saving: {e}")

    def get_all_pattern_codes(self) -> list[PatternsCodeModel]:
        """
        Retrieves all pattern code snippets from the Supabase database.
        Returns:
            list[PatternCodeModel] | None: The list of all pattern code snippets, or None if not found.
        Raises:
            Exception: If retrieving all pattern snippets fails for any reason.
        """
        try:
            response = self.client.from_(self.table_name).select("*").execute()
            if not getattr(response, "data", None):
                return None
            return [PatternsCodeModel(**row) for row in response.data]
        except Exception as e:
            print(f"Error occurred while showing all pattern codes: {e}")
            return None

    def get_pattern_code_by_id(self, pattern_id: UUID) -> list[PatternsCodeModel]:
        """
        Retrieves all pattern code snippets using its unique identifier from the Supabase database.
        Args:
            pattern_code_id (UUID): The unique identifier of the pattern code snippet to retrieve.
        Returns:
            PatternCodeModel | None: The pattern code snippet associated with the provided ID, or None if not found.
        Raises:
            Exception: If retrieving the list of snippets fails for any reason.
        """
        try:
            response = self.client.from_(self.table_name).select("*").eq("pattern_id", str(pattern_id)).execute()
            if not getattr(response, "data", None):
                return None
            return [PatternsCodeModel(**row) for row in response.data]
        except Exception as e:
            print(f"Error occurred while retrieving pattern code: {e}")
            return None

    def get_pattern_code_by_all_id(self, code_id: UUID, pattern_id: UUID) -> PatternsCodeModel:
        try:
            response = self.client.from_(self.table_name).select("*")\
            .eq("code_id", str(code_id)) .eq("pattern_id", str(pattern_id)).execute()
            if not getattr(response, "data", None):
                return None
            return PatternsCodeModel(**response.data[0])

        except Exception as e:
            print(f"Error occurred while retrieving pattern code: {e}")

    def delete_pattern_code(self, code_id: UUID, pattern_id: UUID, token: str) -> None:
        """
         Deletes a pattern code snippet from the Supabase database based on its unique identifier.
        Args:
            pattern_code_id (UUID): The unique identifier of the pattern code snippet to delete.
            token (str): The authentication token for the request.
        Raises:
            Exception: If deleting the snippet fails for any reason.
        """
        try:
            self.client.postgrest.auth(token)
            self.client.from_(self.table_name).delete().eq("code_id", str(code_id)).eq("pattern_id", str(pattern_id)).execute()
        except Exception as e:
            print(f"Error occurred while deleting pattern code: {e}")
