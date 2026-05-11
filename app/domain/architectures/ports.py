from abc import ABC, abstractmethod
from uuid import UUID

from .models import ArchitectureModel

class ArchitecturePort(ABC):

    @abstractmethod
    def save_architecture(self, architecture: ArchitectureModel, token: str) -> None:
        pass

    @abstractmethod
    def get_all_architectures(self, token:str) -> list[ArchitectureModel]:
        pass

    @abstractmethod
    def get_architecture_by_id(self, architecture_id: UUID, token: str) -> ArchitectureModel:
        pass

    @abstractmethod
    def delete_architecture(self, architecture_id: UUID, token: str) -> None:
        pass