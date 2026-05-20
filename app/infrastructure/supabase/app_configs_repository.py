from uuid import UUID

from .client import supabase_client
from app.domain.app_configs.ports import AppConfigPort
from ...domain.app_configs.models import AppConfigModel


class AppConfigService(AppConfigPort):
    def __init__(self):
        self.client = supabase_client
        self.table_name = "app_configs"

    def save_config(self, config: AppConfigModel, token: str) -> None:
        try:
            config_dict = config.model_dump(exclude_none=True)
            if config_dict.get("id") is not None:
                config_dict["id"] = str(config_dict.get("id"))

            if config_dict.get("created_at") is not None:
                config_dict["created_at"] = config_dict.get("created_at").isoformat()

            self.client.postgrest.auth(token)
            response = self.client.from_(self.table_name).update(config_dict).execute()
            
            if hasattr(response, 'error') and response.error:
                print(f"Database unexpected error: {response.error}")
                raise Exception(response.error['message'])

            if getattr(response, "data", None):
                res_data = response.data[0]
                if not config.id and res_data.get("id"):
                    config.id = UUID(res_data["id"])
                if not config.created_at and res_data.get("created_at"):
                    from datetime import datetime
                    config.created_at = datetime.fromisoformat(res_data["created_at"].replace("Z", "+00:00"))

        except Exception as e:
            print(f"Error occurred while saving: {e}")

    def get_all_configs(self, token: str) -> list[AppConfigModel]:
        try:
            self.client.postgrest.auth_token(token)
            res = self.client.from_(self.table_name).select("*").execute()

            if not getattr(res, "data", None):
                return None

            return [AppConfigModel(**row) for row in res.data]

        except Exception as e:
            print(f"Error occurred while showing all app configs: {e}")
            return None

    def get_config_by_id(self, config_id: UUID, token: str) -> AppConfigModel:
        try:
            self.client.postgrest.auth_token(token)
            res = self.client.from_(self.table_name).select("*").eq("id", str(config_id)).execute()

            if not getattr(res, "data", None):
                return None

            return AppConfigModel(**res.data[0])

        except Exception as e:
            print(f"Error occurred while retrieving app config: {e}")
            return None

    def get_config_by_key(self, key: str, token: str) -> AppConfigModel:
        try:
            self.client.postgrest.auth_token(token)
            res = self.client.from_(self.table_name).select("*").eq(key, key).execute()

            if not getattr(res, "data", None):
                return None

            return AppConfigModel(**res.data[0])

        except Exception as e:
            print(f"Error occurred while retrieving app config: {e}")
            return None

    def delete_config(self, config_id: UUID, token: str) -> None:
        try:
            self.client.postgrest.auth_token(token)
            self.client.from_(self.table_name).delete().eq("id", config_id).execute()

        except Exception as e:
            print(f"Error occurred while deleting architecture: {e}")
