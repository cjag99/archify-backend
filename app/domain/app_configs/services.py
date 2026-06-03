from uuid import UUID

from .ports import AppConfigPort
from .models import AppConfigModel
from .dtos import AppConfigRequest

class AppConfigService:
    """
    Service class handling business logic for application configurations.
    """
    def __init__(self, port: AppConfigPort):
        """
        Initializes the AppConfigService with a given port.
        
        Args:
            port (AppConfigPort): The port for persistence operations.
        """
        self.port = port

    def create_config(self, data: AppConfigRequest, token: str) -> AppConfigModel | None:
        """
        Creates a new application configuration.
        
        Args:
            data (AppConfigRequest): The configuration data.
            token (str): The authorization token.
            
        Returns:
            AppConfigModel | None: The created configuration model, or None if failed.
        """
        config = AppConfigModel(**data)
        return  self.port.save_architecture(config)

    def get_all_configs(self, token: str) -> list[AppConfigModel]:
        """
        Retrieves all application configurations.
        
        Args:
            token (str): The authorization token.
            
        Returns:
            list[AppConfigModel]: A list of all configuration models.
        """
        return self.port.get_all_configs(token)

    def get_config_by_id(self, config_id: UUID, token: str) -> AppConfigModel | None:
        """
        Retrieves a configuration by its unique ID.
        
        Args:
            config_id (UUID): The unique identifier of the configuration.
            token (str): The authorization token.
            
        Returns:
            AppConfigModel | None: The requested configuration model, or None if not found.
        """
        return self.port.get_config_by_id(config_id, token)

    def get_config_by_key(self, config_key: str, token: str) -> AppConfigModel | None:
        """
        Retrieves a configuration by its key.
        
        Args:
            config_key (str): The key of the configuration.
            token (str): The authorization token.
            
        Returns:
            AppConfigModel | None: The requested configuration model, or None if not found.
        """
        return self.port.get_config_by_key(config_key, token)

    def get_enabled_configs(self) -> dict[str, str]:
        """
        Retrieves all enabled configurations.
        
        Returns:
            dict[str, str]: A dictionary mapping enabled configuration keys to values.
        """
        return self.port.get_enabled_configs()
    def delete_config(self, config_id: UUID, token: str) -> None:
        """
        Deletes a configuration by its unique ID.
        
        Args:
            config_id (UUID): The unique identifier of the configuration.
            token (str): The authorization token.
        """
        return self.port.delete_config(config_id, token)

    def update_config(self, config_id: UUID, data: AppConfigRequest, token: str) -> AppConfigModel | None:
        """
        Updates an existing configuration.
        
        Args:
            config_id (UUID): The unique identifier of the configuration to update.
            data (AppConfigRequest): The new configuration data.
            token (str): The authorization token.
            
        Returns:
            AppConfigModel | None: The updated configuration model, or None if failed.
        """
        config = self.port.get_config_by_id(config_id, token)
        data_config = AppConfigModel(**data)
        data_config.id = config_id
        if data_config != config:
            return self.port.save_config(data_config, token)
        return data_config
