from abc import ABC, abstractmethod
from uuid import UUID
from .models import AppConfigModel

class AppConfigPort(ABC):
    @abstractmethod
    def save_config(self, config: AppConfigModel, token: str) -> None:
        pass

    @abstractmethod
    def get_all_configs(self, token: str) -> list[AppConfigModel]:
        pass

    @abstractmethod
    def get_config_by_id(self, config_id: UUID, token: str) -> AppConfigModel:
        pass

    @abstractmethod
    def get_config_by_key(self, key: str, token: str) -> AppConfigModel:
        pass

    @abstractmethod
    def delete_config(self, config_id: UUID, token: str) -> None:
        pass
