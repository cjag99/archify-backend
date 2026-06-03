from abc import ABC, abstractmethod
from uuid import UUID

from .dtos import PatternRequestModel
from .models import PatternModel

class PatternPort(ABC):
    """
    Abstract base class defining the interface for pattern persistence operations.
    """

    @abstractmethod
    def save_pattern(self, pattern: PatternModel, token: str) -> None:
        """
        Saves a pattern.

        Args:
            pattern (PatternModel): The pattern to save.
            token (str): The authentication token.
        """
        pass

    @abstractmethod
    def get_pattern_by_id(self, pattern_id: UUID) -> PatternModel | None:
        """
        Retrieves a pattern by its unique identifier.

        Args:
            pattern_id (UUID): The unique identifier of the pattern.

        Returns:
            PatternModel | None: The pattern if found, otherwise None.
        """
        pass

    @abstractmethod
    def get_all_patterns(self) -> list[PatternModel] | None:
        """
        Retrieves all patterns.

        Returns:
            list[PatternModel] | None: A list of patterns, or None if no patterns exist.
        """
        pass

    @abstractmethod
    def delete_pattern(self, pattern_id: UUID, token: str) -> None:
        """
        Deletes a pattern by its unique identifier.

        Args:
            pattern_id (UUID): The unique identifier of the pattern.
            token (str): The authentication token.
        """
        pass

