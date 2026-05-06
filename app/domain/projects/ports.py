from abc import ABC, abstractmethod
from uuid import UUID
from .models import ProjectModel
from .dtos import ProjectCreateModel, ProjectUpdateModel

class ProjectRepositoryPort(ABC):
    @abstractmethod
    def save_project(self, project: ProjectModel) -> None:
        """
        Saves a project in the repository.
        Args:
            project (ProjectModel): The project to save.
        """
        pass

    @abstractmethod
    def get_project_by_id(self, project_id: UUID) -> ProjectModel | None:
        """
        Retrieves a project from the repository based on its unique identifier.
        Args:
            project_id (UUID): The unique identifier of the project to retrieve.
        Returns:
            ProjectModel | None: The project associated with the provided ID, or None if not found.
        """
        pass

    @abstractmethod
    def get_projects_by_user_id(self, user_id: UUID) -> list[ProjectModel] | None:
        """
        Retrieves all projects associated with a specific user from the repository.
        Args:
            user_id (UUID): The unique identifier of the user whose projects to retrieve.
        Returns:
            list[ProjectModel] | None: A list of projects associated with the provided user ID, or None if no projects are found.
        """
        pass

    @abstractmethod
    def delete_project(self, project_id: UUID) -> None:
        """
        Deletes a project from the repository based on its unique identifier.
        Args:
            project_id (UUID): The unique identifier of the project to delete.
        """
        pass

    @abstractmethod
    def update_project(self, project: ProjectModel, data: dict) -> None:
        """
        Updates an existing project in the repository.
        Args:
            project (ProjectModel): The project to update.
            data (dict): The data dictionary to update.
        """
        pass
