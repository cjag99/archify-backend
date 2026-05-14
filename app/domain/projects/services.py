from app.domain.projects.ports import ProjectPort
from uuid import UUID

from .models import ProjectModel
from .dtos import ProjectCreateModel


class ProjectService:
    def __init__(self, project_repository: ProjectPort):
        self.project_repository = project_repository

    def create_project(self, project_data: ProjectCreateModel, user_id: UUID, token: str) -> ProjectModel:
        
        project = ProjectModel(
            name=project_data.name,
            description=project_data.description,
            user_id=user_id
        )
        self.project_repository.save_project(project, token)
        return project

    def get_project_by_id(self, project_id: str, token: str) -> ProjectModel | None:
        return self.project_repository.get_project_by_id(project_id, token)

    def get_projects_by_user_id(self, user_id: str, token: str) -> list[ProjectModel] | None:
        return self.project_repository.get_projects_by_user_id(user_id, token)

    def delete_project(self, project_id: str, token: str) -> None:
        self.project_repository.delete_project(project_id, token)

    def update_project(self, project: ProjectModel, data: dict, token: str) -> None:
        self.project_repository.update_project(project, data, token)