"""
Services for patterns code domain.
"""
from uuid import UUID

from .models import PatternsCodeModel
from .dtos import PatternsCodeRequest
from .ports import PatternsCodePort


class PatternCodeService:
    """
    Service class for managing pattern codes.
    """
    def __init__(self, port: PatternsCodePort):
        """
        Initializes the PatternCodeService.

        Args:
            port (PatternsCodePort): The port to use for patterns code operations.
        """
        self.port = port

    def create_pattern_code(self, data: PatternsCodeRequest, token: str) -> PatternsCodeModel | None:
        """
        Creates a new pattern code.

        Args:
            data (PatternsCodeRequest): The data for the new pattern code.
            token (str): The authorization token.

        Returns:
            PatternsCodeModel | None: The created pattern code, or None if creation failed.
        """
        pattern_code = PatternsCodeModel(
            pattern_id=data.pattern_id,
            code_id=data.code_id,
            code_snippet=data.code_snippet
        )
        self.port.save_pattern_code(pattern_code, token)
        return  pattern_code

    def get_all_pattern_codes(self) -> list[PatternsCodeModel] | None:
        """
        Retrieves all pattern codes.

        Returns:
            list[PatternsCodeModel] | None: A list of pattern codes, or None.
        """
        return  self.port.get_all_pattern_codes()

    def get_pattern_code_by_id(self, code_id: UUID, pattern_id: UUID) -> list[PatternsCodeModel] | None:
        """
        Retrieves pattern codes by pattern ID.

        Args:
            code_id (UUID): The UUID of the code (unused).
            pattern_id (UUID): The UUID of the pattern.

        Returns:
            list[PatternsCodeModel] | None: A list of requested pattern codes, or None.
        """
        return self.port.get_pattern_code_by_id(pattern_id)

    def get_pattern_code_by_all_id(self, code_id: UUID, pattern_id: UUID) -> PatternsCodeModel:
        """
        Retrieves a pattern code by both code ID and pattern ID.

        Args:
            code_id (UUID): The UUID of the code.
            pattern_id (UUID): The UUID of the pattern.

        Returns:
            PatternsCodeModel: The requested pattern code.
        """
        return self.port.get_pattern_code_by_all_id(code_id, pattern_id)
    def delete_pattern_code(self, code_id: UUID, pattern_id: UUID, token: str) -> None:
        """
        Deletes a pattern code.

        Args:
            code_id (UUID): The UUID of the code.
            pattern_id (UUID): The UUID of the pattern.
            token (str): The authorization token.
        """
        self.port.delete_pattern_code(code_id, pattern_id, token)

    def update_pattern_code(self, code_id: UUID, pattern_id: UUID, data: PatternsCodeRequest, token: str) -> PatternsCodeModel:
        """
        Updates an existing pattern code.

        Args:
            code_id (UUID): The UUID of the code to update.
            pattern_id (UUID): The UUID of the pattern to update.
            data (PatternsCodeRequest): The new data for the pattern code.
            token (str): The authorization token.

        Returns:
            PatternsCodeModel: The updated pattern code.
        """
        pattern_code = self.port.get_pattern_code_by_id(code_id, pattern_id)
        pattern_code.code_snippet = data.code_snippet
        self.port.save_pattern_code(pattern_code, token)
        return  pattern_code
