from uuid import UUID

from .client import supabase_client
from app.domain.patterns_code.models import PatternsCodeModel
from app.domain.patterns_code.ports import PatternsCodePort

class SupabasePatternCodeRepository(PatternsCodePort):
    def __init__(self):
        self.client = supabase_client
        self.table_name = "patterns_code"

    def save_pattern_code(self, data: PatternsCodeModel, token: str) -> None:
        try:
            pattern_code_dict = data.model_dump(exclude_none=True)
            if pattern_code_dict.get("id") is not None:
                pattern_code_dict["id"] = str(pattern_code_dict["id"])

            if pattern_code_dict.get("pattern_id") is not None:
                pattern_code_dict["pattern_id"] = str(pattern_code_dict["pattern_id"])

            if pattern_code_dict.get("code_id") is not None:
                pattern_code_dict["code_id"] = str(pattern_code_dict["code_id"])
            
            if pattern_code_dict.get("created_at") is not None:
                pattern_code_dict["created_at"] = pattern_code_dict["created_at"].isoformat()
                
            self.client.postgrest.auth(token)
            response = self.client.from_(self.table_name).upsert(pattern_code_dict).execute()

            if hasattr(response, 'error') and response.error:
                print(f"Error de base de datos: {response.error}")
                raise Exception(response.error['message'])
            
            if getattr(response, "data", None):
                res_data = response.data[0]
                if not data.id and res_data.get("id"):
                    data.id = UUID(res_data["id"])
                if not data.created_at and res_data.get("created_at"):
                    from datetime import datetime
                    data.created_at = datetime.fromisoformat(res_data["created_at"].replace("Z", "+00:00"))
        except Exception as e:
            print(f"Error al guardar: {e}")

    def get_all_pattern_codes(self) -> list[PatternsCodeModel]:
        try:
            response = self.client.from_(self.table_name).select("*").execute()
            if not getattr(response, "data", None):
                return None
            return [PatternsCodeModel(**row) for row in response.data]
        except Exception as e:
            print(f"Error showing all pattern codes: {e}")
            return None

    def get_pattern_code_by_id(self, pattern_code_id: UUID) -> PatternsCodeModel:
        try:
            response = self.client.from_(self.table_name).select("*").eq("id", str(pattern_code_id)).execute()
            if not getattr(response, "data", None):
                return None
            return PatternsCodeModel(**response.data[0])
        except Exception as e:
            print(f"Error retrieving pattern code: {e}")
            return None

    def delete_pattern_code(self, pattern_code_id: UUID, token: str) -> None:
        try:
            self.client.postgrest.auth(token)
            self.client.from_(self.table_name).delete().eq("id", str(pattern_code_id)).execute()
        except Exception as e:
            print(f"Error deleting pattern code: {e}")
