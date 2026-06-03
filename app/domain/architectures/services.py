from uuid import UUID

from .models import ArchitectureModel
from .dtos import ArchitectureRequest
from .ports import ArchitecturePort

class ArchitectureService:
    """
    Service class handling business logic for architectures.
    """
    def __init__(self, port: ArchitecturePort):
        """
        Initializes the ArchitectureService with a given port.
        
        Args:
            port (ArchitecturePort): The port for persistence operations.
        """
        self.port = port

    def create_architecture(self, data: ArchitectureRequest, token: str) -> ArchitectureModel | None:
        """
        Creates a new architecture.
        
        Args:
            data (ArchitectureRequest): The architecture data.
            token (str): The authorization token.
            
        Returns:
            ArchitectureModel | None: The created architecture model.
        """
        architecture = ArchitectureModel(
            name=data.name,
            description=data.description,
            base_structure=data.base_structure
        )

        self.port.save_architecture(architecture, token)
        return architecture

    def get_architecture_by_id(self, architecture_id: UUID, token: str) -> ArchitectureModel | None:
        """
        Retrieves an architecture by its unique ID.
        
        Args:
            architecture_id (UUID): The unique identifier of the architecture.
            token (str): The authorization token.
            
        Returns:
            ArchitectureModel | None: The architecture model if found, else None.
        """
        return self.port.get_architecture_by_id(architecture_id, token)

    def get_all_architectures(self, token:str)-> list[ArchitectureModel]:
        """
        Retrieves all architectures.
        
        Args:
            token (str): The authorization token.
            
        Returns:
            list[ArchitectureModel]: A list of architecture models.
        """
        return self.port.get_all_architectures(token)

    def delete_architecture(self, architecture_id: UUID, token: str) -> None:
        """
        Deletes an architecture by its unique ID.
        
        Args:
            architecture_id (UUID): The unique identifier of the architecture.
            token (str): The authorization token.
        """
        return self.port.delete_architecture(architecture_id, token)

    def update_architecture(self, architecture_id: UUID, data: ArchitectureRequest, token: str) -> None:
        """
        Updates an existing architecture.
        
        Args:
            architecture_id (UUID): The unique identifier of the architecture to update.
            data (ArchitectureRequest): The new architecture data.
            token (str): The authorization token.
        """
        architecture = self.port.get_architecture_by_id(architecture_id, token)
        if data.name and data.name != architecture.name:
            architecture.name = data.name

        if data.description and data.description != architecture.description:
            architecture.description = data.description

        if data.base_structure and data.base_structure != architecture.base_structure:
            architecture.base_structure = data.base_structure

        if data.enabled != architecture.enabled:
            architecture.enabled = data.enabled

        self.port.save_architecture(architecture, token)
