from uuid import UUID

from .client import supabase_client
from app.domain.architectures.models import ArchitectureModel
from app.domain.architectures.ports import ArchitecturePort

class SupabaseArchitectureRepository(ArchitecturePort):
    def __init__(self):
        self.client = supabase_client
        self.table_name = "architectures"

    def save_architecture(self, architecture: ArchitectureModel, token: str) -> None:
        try:
            architecture_dict = architecture.model_dump(exclude_none=True)
            if architecture_dict.get("id") is not None:
                architecture_dict["id"] = str(architecture_dict["id"])

            if architecture_dict.get("created_at") is not None:
                architecture_dict["created_at"] = architecture_dict["created_at"].isoformat()

            self.client.postgrest.auth(token)
            response = self.client.from_(self.table_name).upsert(architecture_dict).execute()
            if hasattr(response, 'error') and response.error:
                print(f"Error de base de datos: {response.error}")
                raise Exception(response.error['message'])

            if getattr(response, "data", None):
                res_data = response.data[0]
                if not architecture.id and res_data.get("id"):
                    architecture.id = UUID(res_data["id"])
                if not architecture.created_at and res_data.get("created_at"):
                    from datetime import datetime
                    architecture.created_at = datetime.fromisoformat(res_data["created_at"].replace("Z", "+00:00"))
        except Exception as e:
            print(f"Erro al guardar: {e}")

    def get_all_architectures(self, token:str) -> list[ArchitectureModel]:
        try:
            self.client.postgrest.auth(token)
            res = self.client.from_(self.table_name).select("*").execute()
            if not getattr(res, "data", None):
                return None

            return [ArchitectureModel(**row) for row in res.data]
        except Exception as e:
            print(f"Error al obtener todos los patterns: {e}")
            return None

    def get_architecture_by_id(self, architecture_id: UUID, token: str) -> ArchitectureModel:
        try:
            self.client.postgrest.auth(token)
            res = self.client.from_(self.table_name).select("*").eq("id", str(architecture_id)).execute()
            if not getattr(res, "data", None):
                return None

            return ArchitectureModel(**res.data[0])
        except Exception as e:
            print(f"Error al obtener: {e}")
            return None

    def delete_architecture(self, architecture_id: UUID, token: str) -> None:
        try:
            self.client.postgrest.auth(token)
            self.client.from_(self.table_name).delete().eq("id", architecture_id).execute()
        except Exception as e:
            print(f"Error al eliminar pattern: {e}")
