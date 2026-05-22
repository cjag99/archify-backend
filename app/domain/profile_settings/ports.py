from uuid import UUID
from abc import ABC, abstractmethod

from .models import ProfileSettingsModel


class ProfileSettingsPort(ABC):
    @abstractmethod
    def save_profile_setting(self, data: ProfileSettingsModel, token: str) -> ProfileSettingsModel:
        pass

    @abstractmethod
    def get_profile_settings(self, token: str) -> list[ProfileSettingsModel]:
        pass

    @abstractmethod
    def get_profile_setting_by_id(self, profile_setting_id: UUID, token: str) -> ProfileSettingsModel:
        pass

    @abstractmethod
    def delete_profile_setting(self, profile_setting_id: UUID, token: str) -> None:
        pass
