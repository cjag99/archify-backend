from abc import ABC, abstractmethod
from uuid import UUID

from .models import SettingsModel

class SettingsPort(ABC):
    @abstractmethod
    def save_setting(self, setting: SettingsModel) -> SettingsModel:
        pass

    @abstractmethod
    def get_settings(self, token: str) -> list[SettingsModel]:
        pass

    @abstractmethod
    def get_setting_by_id(self, setting_id: UUID, token: str) -> SettingsModel:
        pass

    @abstractmethod
    def delete_setting(self, setting_id: UUID, token: str) -> None:
        pass
