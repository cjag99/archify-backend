from abc import ABC, abstractmethod
from uuid import UUID

from .models import CodeLanguagesModel

class CodeLanguagesPort(ABC):
    """
    Abstract port for code language operations.
    """
    @abstractmethod
    def save_code_language(self, code_language: CodeLanguagesModel, token: str):
        """
        Save a code language model.

        Args:
            code_language (CodeLanguagesModel): The model to save.
            token (str): Authentication token.
        """
        pass

    @abstractmethod
    def get_all_code_languages(self, token: str) -> list[CodeLanguagesModel] | None:
        """
        Retrieve all code languages.

        Args:
            token (str): Authentication token.

        Returns:
            list[CodeLanguagesModel] | None: A list of code languages or None.
        """
        pass

    @abstractmethod
    def get_code_language_by_id(self, code_language_id: UUID, token: str) -> CodeLanguagesModel:
        """
        Retrieve a specific code language by its ID.

        Args:
            code_language_id (UUID): The unique identifier of the code language.
            token (str): Authentication token.

        Returns:
            CodeLanguagesModel: The retrieved code language model.
        """
        pass

    @abstractmethod
    def delete_code_language(self, code_language_id: UUID, token: str) -> None:
        """
        Delete a code language by its ID.

        Args:
            code_language_id (UUID): The unique identifier of the code language to delete.
            token (str): Authentication token.
        """
        pass