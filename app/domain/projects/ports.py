from abc import ABC, abstractmethod
from uuid import UUID
from .models import ProjectModel

class ProjectPort(ABC):
    @abstractmethod
    def save_project(self, project: ProjectModel, token: str) -> None:
        """
        Saves a project in the repository.
        Args:
            project (ProjectModel): The project to save.
            token (str): The authentication token.
        """
        pass

    @abstractmethod
    def get_project_by_id(self, project_id: UUID, token: str) -> ProjectModel | None:
        """
        Retrieves a project from the repository based on its unique identifier.
        Args:
            project_id (UUID): The unique identifier of the project to retrieve.
            token (str): The authentication token.
        Returns:
            ProjectModel | None: The project associated with the provided ID, or None if not found.
        """
        pass

    @abstractmethod
    def get_projects_by_user_id(self, user_id: UUID, token: str) -> list[ProjectModel] | None:
        """
        Retrieves all projects associated with a specific user from the repository.
        Args:
            user_id (UUID): The unique identifier of the user whose projects to retrieve.
            token (str): The authentication token.
        Returns:
            list[ProjectModel] | None: A list of projects associated with the provided user ID, or None if no projects are found.
        """
        pass

    @abstractmethod
    def delete_project(self, project_id: UUID, token: str) -> None:
        """
        Deletes a project from the repository based on its unique identifier.
        Args:
            project_id (UUID): The unique identifier of the project to delete.
            token (str): The authentication token.
        """
        pass
