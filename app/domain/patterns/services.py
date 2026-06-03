from uuid import UUID
from .models import PatternModel
from .dtos import PatternRequestModel
from .ports import PatternPort

class PatternService:
    """
    Service class handling the business logic for patterns.
    """
    def __init__(self, port: PatternPort):
        """
        Initializes the PatternService.

        Args:
            port (PatternPort): The port interface for pattern operations.
        """
        self.port = port

    def create_pattern(self, data: PatternRequestModel, user_id: UUID, token: str) -> PatternModel | None:
        """
        Creates a new pattern.

        Args:
            data (PatternRequestModel): The request data to create the pattern.
            user_id (UUID): The unique identifier of the user creating the pattern.
            token (str): The authentication token.

        Returns:
            PatternModel | None: The created pattern model.
        """
        pattern = PatternModel(
            name=data.name,
            description=data.description,
            base_structure=data.base_structure,
            image_id=data.image_id,
        )
        self.port.save_pattern(pattern, token)
        return  pattern

    def get_pattern_by_id(self, pattern_id: UUID) -> PatternModel | None:
        """
        Retrieves a pattern by its unique identifier.

        Args:
            pattern_id (UUID): The unique identifier of the pattern.

        Returns:
            PatternModel | None: The pattern if found, otherwise None.
        """
        return self.port.get_pattern_by_id(pattern_id)

    def get_all_patterns(self) -> list[PatternModel] | None:
        """
        Retrieves all patterns.

        Returns:
            list[PatternModel] | None: A list of patterns, or None if no patterns exist.
        """
        return self.port.get_all_patterns()

    def delete_pattern(self, pattern_id: UUID, token: str) -> None:
        """
        Deletes a pattern by its unique identifier.

        Args:
            pattern_id (UUID): The unique identifier of the pattern.
            token (str): The authentication token.
        """
        return self.port.delete_pattern(pattern_id, token)

    def update_pattern(self, pattern_id: UUID, data: PatternRequestModel, token: str) -> None:
        """
        Updates an existing pattern.

        Args:
            pattern_id (UUID): The unique identifier of the pattern to update.
            data (PatternRequestModel): The request data containing the updates.
            token (str): The authentication token.
        """
        pattern = self.port.get_pattern_by_id(pattern_id)
        new_pattern = PatternModel(**data.model_dump(exclude_none=True))

        new_pattern.id = pattern_id

        if pattern != new_pattern:
            self.port.save_pattern(new_pattern, token)