from uuid import UUID

from app.domain.code_languages.models import CodeLanguagesModel
from app.domain.code_languages.ports import CodeLanguagesPort
from app.infrastructure.supabase.client import supabase_client


class SupabaseCodeLanguageRepository(CodeLanguagesPort):
    def __init__(self):
        self.client = supabase_client
        self.table_name = "code_languages"

    def save_code_language(self, code_language: CodeLanguagesModel, token: str) -> None:
        try:
            code_language_dict = code_language.model_dump(exclude_none=True)
            if code_language_dict.get("id") is not None:
                code_language_dict["id"] = str(code_language_dict["id"])

            if code_language_dict.get("created_at") is not None:
                code_language_dict["created_at"] = code_language_dict["created_at"].isoformat()

            self.client.postgrest.auth(token)
            response = self.client.from_(self.table_name).upsert(code_language_dict).execute()
            if hasattr(response, 'error') and response.error:
                print(f"Error de base de datos: {response.error}")
                raise Exception(response.error['message'])
            
            if getattr(response, "data", None):
                res_data = response.data[0]
                if not code_language.id and res_data.get("id"):
                    code_language.id = UUID(res_data["id"])
                if not code_language.created_at and res_data.get("created_at"):
                    from datetime import datetime
                    code_language.created_at = datetime.fromisoformat(res_data["created_at"].replace("Z", "+00:00"))
        except Exception as e:
            print(f"Error al guardar: {e}")

    def get_all_code_languages(self, token: str) -> list[CodeLanguagesModel] | None:
        try:
            self.client.postgrest.auth(token)
            response = self.client.from_(self.table_name).select("*").execute()
            if not getattr(response, "data", None):
                return None
            return [CodeLanguagesModel(**row) for row in response.data]
        except Exception as e:
            print(f"Error showing all code languages: {e}")
            return None

    def get_code_language_by_id(self, code_language_id: UUID, token: str) -> CodeLanguagesModel | None:
        try:
            self.client.postgrest.auth(token)
            response = self.client.from_(self.table_name).select("*").eq("id", str(code_language_id)).execute()
            if not getattr(response, "data", None):
                return None
            return CodeLanguagesModel(**response.data[0])
        except Exception as e:
            print(f"Error retrieving code language: {e}")
            return None

    def delete_code_language(self, code_language_id: UUID, token: str) -> None:
        try:
            self.client.postgrest.auth(token)
            self.client.from_(self.table_name).delete().eq("id", str(code_language_id)).execute()
        except Exception as e:
            print(f"Error deleting code language: {e}")