from uuid import UUID

from .ports import AppConfigPort
from .models import AppConfigModel
from .dtos import AppConfigRequest

class AppConfigService:
    def __init__(self, port: AppConfigPort):
        self.port = port

    def create_config(self, data: AppConfigRequest, token: str) -> AppConfigModel | None:
        config = AppConfigModel(**data)
        return  self.port.save_architecture(config)

    def get_all_configs(self, token: str) -> list[AppConfigModel]:
        return self.port.get_all_configs(token)

    def get_config_by_id(self, config_id: UUID, token: str) -> AppConfigModel | None:
        return self.port.get_config_by_id(config_id, token)

    def get_config_by_key(self, config_key: str, token: str) -> AppConfigModel | None:
        return self.port.get_config_by_key(config_key, token)

    def get_enabled_configs(self) -> dict[str, str]:
        return self.port.get_enabled_configs()
    def delete_config(self, config_id: UUID, token: str) -> None:
        return self.port.delete_config(config_id, token)

    def update_config(self, config_id: UUID, data: AppConfigRequest, token: str) -> AppConfigModel | None:
        config = self.port.get_config_by_id(config_id, token)
        data_config = AppConfigModel(**data)
        data_config.id = config_id
        if data_config != config:
            return self.port.save_config(data_config, token)
        return data_config
