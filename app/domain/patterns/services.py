from uuid import UUID
from .models import PatternModel
from .dtos import PatternRequestModel
from .ports import PatternPort

class PatternService:
    def __init__(self, port: PatternPort):
        self.port = port

    def create_pattern(self, data: PatternRequestModel, user_id: UUID) -> PatternModel | None:
        pattern = PatternModel(
            name=data.name,
            description=data.description,
            base_structure=data.base_structure
        )
        self.port.save_pattern(pattern)
        return  pattern

    def get_pattern_by_id(self, pattern_id: UUID) -> PatternModel | None:
        return self.port.get_pattern_by_id(pattern_id)

    def get_all_patterns(self) -> list[PatternModel] | None:
        return self.port.get_all_patterns()

    def delete_pattern(self, pattern_id: UUID) -> None:
        return self.port.delete_pattern(pattern_id)

    def update_pattern(self, pattern_id: UUID, data: PatternRequestModel) -> None:
        pattern = self.port.get_pattern_by_id(pattern_id)
        if pattern:
            if pattern.name != data.name:
                pattern.name = data.name

            if pattern.description != data.description:
                pattern.description = data.description

            if pattern.base_structure != data.base_structure:
                pattern.base_structure = data.base_structure

            self.port.save_pattern(pattern)