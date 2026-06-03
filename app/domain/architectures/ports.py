from abc import ABC, abstractmethod
from uuid import UUID

from .models import ArchitectureModel

class ArchitecturePort(ABC):
    """
    Port interface for architecture persistence operations.
    """

    @abstractmethod
    def save_architecture(self, architecture: ArchitectureModel, token: str) -> None:
        """
        Saves an architecture.
        
        Args:
            architecture (ArchitectureModel): The architecture model to save.
            token (str): The authorization token.
        """
        pass

    @abstractmethod
    def get_all_architectures(self, token:str) -> list[ArchitectureModel]:
        """
        Retrieves all architectures.
        
        Args:
            token (str): The authorization token.
            
        Returns:
            list[ArchitectureModel]: A list of all architecture models.
        """
        pass

    @abstractmethod
    def get_architecture_by_id(self, architecture_id: UUID, token: str) -> ArchitectureModel:
        """
        Retrieves an architecture by its unique ID.
        
        Args:
            architecture_id (UUID): The unique identifier of the architecture.
            token (str): The authorization token.
            
        Returns:
            ArchitectureModel: The requested architecture model.
        """
        pass

    @abstractmethod
    def delete_architecture(self, architecture_id: UUID, token: str) -> None:
        """
        Deletes an architecture by its unique ID.
        
        Args:
            architecture_id (UUID): The unique identifier of the architecture to delete.
            token (str): The authorization token.
        """
        pass