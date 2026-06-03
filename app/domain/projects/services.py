from app.domain.projects.ports import ProjectPort
from uuid import UUID

from .models import ProjectModel
from .dtos import ProjectCreateModel


class ProjectService:
    """
    Service for managing projects.

    This service coordinates with the ProjectPort to handle project creation,
    retrieval, and deletion.
    """

    def __init__(self, port: ProjectPort):
        """
        Initializes the ProjectService.

        Args:
            port (ProjectPort): The repository port for projects.
        """
        self.port = port

    def save_project(self, project_data: ProjectCreateModel, user_id: UUID, token: str) -> ProjectModel:
        """
        Saves a new project.

        Args:
            project_data (ProjectCreateModel): The project creation data.
            user_id (UUID): The ID of the user creating the project.
            token (str): The authentication token.

        Returns:
            ProjectModel: The saved project model.
        """
        project = ProjectModel(**project_data.model_dump(exclude_none=True))
        project.user_id = user_id
        self.port.save_project(project, token)
        return project

    def get_project_by_id(self, project_id: UUID, token: str) -> ProjectModel | None:
        """
        Retrieves a project by its ID.

        Args:
            project_id (UUID): The ID of the project.
            token (str): The authentication token.

        Returns:
            ProjectModel | None: The project if found, otherwise None.
        """
        return self.port.get_project_by_id(project_id, token)

    def get_projects_by_user_id(self, user_id: UUID, token: str) -> list[ProjectModel] | None:
        """
        Retrieves all projects associated with a given user ID.

        Args:
            user_id (UUID): The ID of the user.
            token (str): The authentication token.

        Returns:
            list[ProjectModel] | None: A list of projects, or None if no projects found.
        """
        return self.port.get_projects_by_user_id(user_id, token)

    def delete_project(self, project_id: UUID, token: str) -> None:
        """
        Deletes a project by its ID.

        Args:
            project_id (UUID): The ID of the project to delete.
            token (str): The authentication token.
        """
        self.port.delete_project(project_id, token)

    def get_all_projects(self, token: str) -> list[ProjectModel] | None:
        """
        Retrieves all projects in the system.

        Args:
            token (str): The authentication token.

        Returns:
            list[ProjectModel] | None: A list of all projects, or None.
        """
        return self.port.get_all_projects(token)
