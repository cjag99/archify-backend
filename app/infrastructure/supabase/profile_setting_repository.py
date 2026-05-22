from uuid import UUID

from app.domain.profile_settings.dtos import ProfileSettingsRequest
from app.domain.profile_settings.models import ProfileSettingsModel
from app.domain.profile_settings.ports import ProfileSettingsPort
from app.infrastructure.supabase.client import supabase_client


class SupabaseProfileSettingRepository(ProfileSettingsPort):
    def __init__(self):
        self.client = supabase_client
        self.table_name = "profile_settings"

    def save_profile_setting(self, data: ProfileSettingsRequest, token: str) -> ProfileSettingsModel:
        try:
            profile_settings_dict = data.model_dump(exclude_none=True)
            self.client.postgrest.auth(token)
            response = self.client.from_(self.table_name).upsert(profile_settings_dict).execute()
            
            if hasattr(response, 'error') and response.error:
                print(f"Database unexpected error: {response.error}")
                raise Exception(response.error['message'])

            if getattr(response, "data", None):
                res_data = response.data[0]
                if not data.created_at and res_data.get("created_at"):
                    from datetime import datetime
                    data.created_at = datetime.fromisoformat(res_data["created_at"].replace("Z", "+00:00"))

        except Exception as e:
            print(f"Error occurred while saving profile setting: {e}")

    def get_profile_settings(self, token: str) -> list[ProfileSettingsModel]:
        try:
            self.client.postgrest.auth(token)
            response = self.client.from_(self.table_name).select("*").execute()

            if not getattr(response, "data", None):
                return None
            return [ProfileSettingsModel(**row) for row in response.data]

        except Exception as e:
            print(f"Error occurred while retrieving profile settings: {e}")

    def get_profile_setting_by_id(self, user_id: UUID, profile_setting_id: UUID, token: str) -> ProfileSettingsModel:
        try:
            self.client.postgrest.auth(token)
            response = (self.client.from_(self.table_name).select("*")
                        .eq("settings_id", str(profile_setting_id))
                        .eq("profile_id", str(user_id))
                        .execute())

            if not getattr(response, "data", None):
                return None

            return ProfileSettingsModel(**response.data[0])

        except Exception as e:
            print(f"Error occurred while retrieving profile setting: {e}")

    def get_user_settings(self, user_id: UUID, token: str) -> list[ProfileSettingsModel]:
        try:
            self.client.postgrest.auth(token)
            response = self.client.from_(self.table_name).select("*").eq("profile_id", str(user_id)).execute()

            if not getattr(response, "data", None):
                return None

            return [ProfileSettingsModel(**row) for row in response.data]

        except Exception as e:
            print(f"Error occurred while retrieving profile setting: {e}")

    def delete_profile_setting(self, profile_setting_id: UUID, token: str) -> ProfileSettingsModel:
        try:
            self.client.postgrest.auth(token)
            self.client.delete(self.table_name).delete("*").eq("id", str(profile_setting_id)).execute()

        except Exception as e:
            print(f"Error occurred while deleting profile setting: {e}")
