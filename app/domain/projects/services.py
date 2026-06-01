from app.domain.projects.ports import ProjectPort
from uuid import UUID

from .models import ProjectModel
from .dtos import ProjectCreateModel


class ProjectService:
    def __init__(self, port: ProjectPort):
        self.port = port

    def create_project(self, project_data: ProjectCreateModel, user_id: UUID, token: str) -> ProjectModel:
        
        project = ProjectModel(**project_data.model_dump(exclude_none=True))
        project.user_id = user_id
        self.port.save_project(project, token)
        return project

    def get_project_by_id(self, project_id: UUID, token: str) -> ProjectModel | None:
        return self.port.get_project_by_id(project_id, token)

    def get_projects_by_user_id(self, user_id: UUID, token: str) -> list[ProjectModel] | None:
        return self.port.get_projects_by_user_id(user_id, token)

    def delete_project(self, project_id: UUID, token: str) -> None:
        self.port.delete_project(project_id, token)

    def get_all_projects(self, token: str) -> list[ProjectModel] | None:
        return self.port.get_all_projects(token)
