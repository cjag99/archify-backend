from abc import ABC, abstractmethod
from uuid import UUID

from .models import CodeLanguagesModel

class CodeLanguagesPort(ABC):
    @abstractmethod
    def save_code_language(self, code_language: CodeLanguagesModel, token: str):
        pass

    @abstractmethod
    def get_all_code_languages(self, token: str) -> list[CodeLanguagesModel] | None:
        pass

    @abstractmethod
    def get_code_language_by_id(self, code_language_id: UUID, token: str) -> CodeLanguagesModel:
        pass

    @abstractmethod
    def delete_code_language(self, code_language_id: UUID, token: str) -> None:
        pass