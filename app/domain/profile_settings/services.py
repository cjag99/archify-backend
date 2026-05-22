from uuid import UUID

from app.domain.profile_settings.dtos import ProfileSettingsRequest
from app.domain.profile_settings.models import ProfileSettingsModel
from app.domain.profile_settings.ports import ProfileSettingsPort


class ProfileSettingService:
    def __init__(self, port: ProfileSettingsPort):
        self.port = port

    def create_profile_setting(self, data: ProfileSettingsRequest, token: str) -> ProfileSettingsModel:
        data_profile_setting = ProfileSettingsModel(**data)
        return self.port.save_profile_setting(data_profile_setting, token)

    def get_profile_settings(self, token: str) -> list[ProfileSettingsModel]:
        return self.port.get_profile_settings(token)

    def get_profile_setting_by_id(self, user_id: UUID, profile_setting_id: UUID, token: str) -> ProfileSettingsModel:
        return self.port.get_profile_setting_by_id(user_id, profile_setting_id, token)

    def get_user_settings(self, user_id: UUID, token: str) -> list[ProfileSettingsModel]:
        return self.port.get_user_settings(user_id, token)

    def delete_profile_setting(self, profile_setting_id: UUID, token: str) -> None:
        return self.port.delete_profile_setting(profile_setting_id, token)

    def update_profile_setting(self, profile_setting_id: UUID, data: ProfileSettingsRequest, token: str) -> None:
        profile_setting = self.port.get_profile_setting_by_id(profile_setting_id, token)
        data_profile_setting = ProfileSettingsModel(**data)
        if profile_setting != data_profile_setting:
            self.port.save_profile_setting(data_profile_setting, token)
