from uuid import UUID
from datetime import datetime

from supabase_auth.helpers import model_dump

from app.domain.settings.models import SettingsModel
from app.domain.settings.ports import SettingsPort
from app.infrastructure.supabase.client import supabase_client


class SupabaseSettingsRepository(SettingsPort):
    def __init__(self):
        self.client = supabase_client
        self.table_name = "settings"

    def save_setting(self, settings: SettingsModel, token: str) -> SettingsModel:
        try:
            setttings_dict = settings.model_dump(exclude_none=True)
            if setttings_dict.get("id") is not None:
                setttings_dict["id"] = str(setttings_dict["id"])

            if setttings_dict.get("created_at") is not None:
                setttings_dict["created_at"] = setttings_dict["created_at"].isoformat()

            self.client.postgrest.auth(token)
            response = self.client.from_(self.table_name).upsert(setttings_dict).execute()
            
            if hasattr(response, 'error') and response.error:
                print(f"Database unexpected error: {response.error}")
                raise Exception(response.error['message'])

            if getattr(response, "data", None):
                res_data = response.data[0]
                if not settings.id and res_data.get("id"):
                    settings.id = UUID(res_data["id"])
                if not settings.created_at and res_data.get("created_at"):
                    from datetime import datetime
                    settings.created_at = datetime.fromisoformat(res_data["created_at"].replace("Z", "+00:00"))

        except Exception as e:
            print(f"Error occurred while saving settings: {e}")

    def get_settings(self, token: str) -> list[SettingsModel]:
        try:
            self.client.postgrest.auth(token)
            response = self.client.from_(self.table_name).select("*").execute()

            if not getattr(response, "data", None):
                return None
            return [SettingsModel(**row) for row in response.data]

        except Exception as e:
            print(f"Error occurred while retrieving all settings: {e}")
            return None

    def get_setting_by_id(self, setting_id: UUID, token: str) -> SettingsModel:
        try:
            self.client.postgrest.auth(token)
            response = self.client.from_(self.table_name).select("*").eq("id", str(setting_id)).execute()
            if not getattr(response, "data", None):
                return None

            return SettingsModel(**response.data[0])

        except Exception as e:
            print(f"Error occurred while retrieving setting: {e}")
            return None

    def delete_setting(self, setting_id: UUID, token: str) -> None:
        try:
            self.client.postgrest.auth(token)
            self.client.from_(self.table_name).delete().eq(setting_id).execute()

        except Exception as e:
            print(f"Error occurred while deleting setting: {e}")
