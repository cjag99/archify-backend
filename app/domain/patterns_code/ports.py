"""
Port definitions for patterns code domain.
"""
from abc import ABC, abstractmethod
from uuid import UUID

from .models import PatternsCodeModel

class PatternsCodePort(ABC):
    """
    Abstract base class defining the port for patterns code operations.
    """
    @abstractmethod
    def save_pattern_code(self, data: PatternsCodeModel, token: str) -> PatternsCodeModel:
        """
        Saves a pattern code.

        Args:
            data (PatternsCodeModel): The pattern code data to save.
            token (str): The authorization token.

        Returns:
            PatternsCodeModel: The saved pattern code.
        """
        pass

    @abstractmethod
    def get_all_pattern_codes(self) -> list[PatternsCodeModel]:
        """
        Retrieves all pattern codes.

        Returns:
            list[PatternsCodeModel]: A list of all pattern codes.
        """
        pass

    @abstractmethod
    def get_pattern_code_by_id(self, pattern_id: UUID) -> PatternsCodeModel:
        """
        Retrieves a pattern code by its pattern ID.

        Args:
            pattern_id (UUID): The UUID of the pattern.

        Returns:
            PatternsCodeModel: The requested pattern code.
        """
        pass

    @abstractmethod
    def get_pattern_code_by_all_id(self, code_id: UUID, pattern_id: UUID) -> PatternsCodeModel:
        """
        Retrieves a pattern code by both code ID and pattern ID.

        Args:
            code_id (UUID): The UUID of the code.
            pattern_id (UUID): The UUID of the pattern.

        Returns:
            PatternsCodeModel: The requested pattern code.
        """
        pass

    @abstractmethod
    def delete_pattern_code(self, code_id: UUID, pattern_id: UUID, token: str) -> None:
        """
        Deletes a pattern code.

        Args:
            code_id (UUID): The UUID of the code.
            pattern_id (UUID): The UUID of the pattern.
            token (str): The authorization token.
        """
        pass