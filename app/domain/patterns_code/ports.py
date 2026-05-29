from abc import ABC, abstractmethod
from uuid import UUID

from .models import PatternsCodeModel

class PatternsCodePort(ABC):
    @abstractmethod
    def save_pattern_code(self, data: PatternsCodeModel, token: str) -> PatternsCodeModel:
        pass

    @abstractmethod
    def get_all_pattern_codes(self) -> list[PatternsCodeModel]:
        pass

    @abstractmethod
    def get_pattern_code_by_id(self, code_id: UUID, pattern_id: UUID) -> PatternsCodeModel:
        pass

    @abstractmethod
    def delete_pattern_code(self, code_id: UUID, pattern_id: UUID, token: str) -> None:
        pass