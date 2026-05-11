from uuid import UUID

from .models import ArchitectureModel
from .dtos import ArchitectureRequest
from .ports import ArchitecturePort

class ArcchitectureService:
    def __init__(self, port: ArchitecturePort):
        self.port = port

    def create_architecture(self, data: ArchitectureRequest, token: str) -> ArchitectureModel | None:
        architecture = ArchitectureModel(
            name=data.name,
            description=data.description,
            base_structure=data.base_structure
        )

        self.port.save_architecture(architecture, token)
        return architecture

    def get_architecture_by_id(self, architecture_id: UUID, token: str) -> ArchitectureModel | None:
        return self.port.get_architecture_by_id(architecture_id, token)

    def get_all_architectures(self, token:str)-> list[ArchitectureModel]:
        return self.port.get_all_architectures(token)

    def delete_architecture(self, architecture_id: UUID, token: str) -> None:
        return self.port.delete_architecture(architecture_id, token)

    def update_architecture(self, architecture_id: UUID, data: ArchitectureRequest, token: str) -> None:
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
