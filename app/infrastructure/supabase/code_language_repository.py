from uuid import UUID

from app.domain.code_languages.models import CodeLanguagesModel
from app.domain.code_languages.ports import CodeLanguagesPort
from app.infrastructure.supabase.client import supabase_client


class SupabaseCodeLanguageRepository(CodeLanguagesPort):
    """
    Repository class to manage code languages in the Supabase database.
    This class implements the CodeLanguagesPort interface, providing methods to save and retrieve code languages using the Supabase client.
    """
    def __init__(self):
        """
        Initializes the SupabaseCodeLanguageRepository with the Supabase client and sets the table name.
        """
        self.client = supabase_client
        self.table_name = "code_languages"

    def save_code_language(self, code_language: CodeLanguagesModel, token: str) -> None:
        """
        Saves a code language to the Supabase database.
        Args:
            code_language (CodeLanguagesModel): The code language to save.
            token (str): The autheuntication token for the request.
        Raises:
            Exception: If saving the code language fails for any reason.
        """
        try:
            code_language_dict = code_language.model_dump(exclude_none=True)
            if code_language_dict.get("id") is not None:
                code_language_dict["id"] = str(code_language_dict["id"])

            if code_language_dict.get("icon") is not None:
                code_language_dict["icon"] = str(code_language_dict["icon"])
                
            if code_language_dict.get("created_at") is not None:
                code_language_dict["created_at"] = code_language_dict["created_at"].isoformat()

            self.client.postgrest.auth(token)
            response = self.client.from_(self.table_name).upsert(code_language_dict).execute()

            if hasattr(response, 'error') and response.error:
                print(f"Database unexpected erro5: {response.error}")
                raise Exception(response.error['message'])
            
            if getattr(response, "data", None):
                res_data = response.data[0]
                if not code_language.id and res_data.get("id"):
                    code_language.id = UUID(res_data["id"])
                if not code_language.created_at and res_data.get("created_at"):
                    from datetime import datetime
                    code_language.created_at = datetime.fromisoformat(res_data["created_at"].replace("Z", "+00:00"))

        except Exception as e:
            print(f"Error occurred while saving: {e}")

    def get_all_code_languages(self, token: str) -> list[CodeLanguagesModel] | None:
        """
         Retrieves all code languages from the Supabase database.
        Args:
            token (str): The authentication token for the request.
        Returns:
            list[ProjectModel] | None: The list of all code languages, or None if not found.
        Raises:
            Exception: If retrieving all code languages fails for any reason.
        """
        try:
            self.client.postgrest.auth(token)
            response = self.client.from_(self.table_name).select("*").execute()
            if not getattr(response, "data", None):
                return None

            return [CodeLanguagesModel(**row) for row in response.data]

        except Exception as e:
            print(f"Error occured while showing all code languages: {e}")
            return None

    def get_code_language_by_id(self, code_language_id: UUID, token: str) -> CodeLanguagesModel | None:
        """
        Retrieves a code language by its unique identifier from the Supabase database.
        Args:
            code_language_id (UUID): The unique identifier of the code language to retrieve.
            token (str): The authentication token for the request.
        Returns:
            CodeLanguagesModel | None: The code language associated with the provided ID, or None if not found.
        Raises:
            Exception: If retrieving the code language fails for any reason.
        """
        try:
            self.client.postgrest.auth(token)
            response = self.client.from_(self.table_name).select("*").eq("id", str(code_language_id)).execute()
            if not getattr(response, "data", None):
                return None

            return CodeLanguagesModel(**response.data[0])

        except Exception as e:
            print(f"Error occurred while retrieving code language: {e}")
            return None

    def delete_code_language(self, code_language_id: UUID, token: str) -> None:
        """
        Deletes a code language from the Supabase database based on its unique identifier.
        Args:
            code_language_id (UUID): The unique identifier of the code language to delete.
            token (str): The authentication token for the request.
        Raises:
            Exception: If deleting the code language fails for any reason.
        """
        try:
            self.client.postgrest.auth(token)
            self.client.from_(self.table_name).delete().eq("id", str(code_language_id)).execute()

        except Exception as e:
            print(f"Error occurred while deleting code language: {e}")