from uuid import UUID

from .dtos import SettingsRequest
from .models import SettingsModel
from .ports import SettingsPort

class SettingsService:
    def __init__(self, port: SettingsPort):
        self.port = port

    def create_settings(self, data: SettingsRequest, token: str) -> SettingsModel:
        settings = SettingsModel(**data)
        return self.port.save_setting(settings, token)

    def get_settings(self, token: str) -> list[SettingsModel]:
        return self.port.get_settings(token)

    def get_setting_by_id(self, setting_id: UUID, token: str) -> SettingsModel:
        return self.port.get_setting_by_id(setting_id, token)

    def delete_setting(self, setting_id: UUID, token: str) -> None:
        self.port.delete_setting(setting_id, token)

    def update_setting(self, setting_id: UUID, data: SettingsRequest, token: str) -> SettingsModel:
        settings = self.port.get_setting_by_id(setting_id, token)
        data_setting = SettingsModel(**data)
        data_setting.id = setting_id
        if settings != data_setting:
            self.port.save_setting(data_setting, token)
