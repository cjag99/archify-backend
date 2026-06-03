from abc import ABC, abstractmethod
from uuid import UUID
from .models import AppConfigModel

class AppConfigPort(ABC):
    """
    Port interface for application configuration persistence operations.
    """
    @abstractmethod
    def save_config(self, config: AppConfigModel, token: str) -> None:
        """
        Saves an application configuration.
        
        Args:
            config (AppConfigModel): The configuration model to save.
            token (str): The authorization token.
        """
        pass

    @abstractmethod
    def get_all_configs(self, token: str) -> list[AppConfigModel]:
        """
        Retrieves all application configurations.
        
        Args:
            token (str): The authorization token.
            
        Returns:
            list[AppConfigModel]: A list of all configuration models.
        """
        pass

    @abstractmethod
    def get_config_by_id(self, config_id: UUID, token: str) -> AppConfigModel:
        """
        Retrieves a configuration by its unique ID.
        
        Args:
            config_id (UUID): The unique identifier of the configuration.
            token (str): The authorization token.
            
        Returns:
            AppConfigModel: The requested configuration model.
        """
        pass

    @abstractmethod
    def get_config_by_key(self, key: str, token: str) -> AppConfigModel:
        """
        Retrieves a configuration by its key.
        
        Args:
            key (str): The key of the configuration.
            token (str): The authorization token.
            
        Returns:
            AppConfigModel: The requested configuration model.
        """
        pass

    @abstractmethod
    def get_enabled_configs(self,) -> dict[str, str]:
        """
        Retrieves all enabled configurations as a key-value mapping.
        
        Returns:
            dict[str, str]: A dictionary of enabled configuration keys and values.
        """
        pass

    @abstractmethod
    def delete_config(self, config_id: UUID, token: str) -> None:
        """
        Deletes a configuration by its unique ID.
        
        Args:
            config_id (UUID): The unique identifier of the configuration to delete.
            token (str): The authorization token.
        """
        pass
