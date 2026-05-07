from abc import ABC, abstractmethod
from uuid import UUID

from .dtos import PatternRequestModel
from .models import PatternModel

class PatternPort(ABC):

    @abstractmethod
    def save_pattern(self, pattern: PatternModel, token: str) -> None:
        pass

    @abstractmethod
    def get_pattern_by_id(self, pattern_id: UUID) -> PatternModel | None:
        pass

    @abstractmethod
    def get_all_patterns(self) -> list[PatternModel] | None:
        pass

    @abstractmethod
    def delete_pattern(self, pattern_id: UUID, token: str) -> None:
        pass

