from app.domain.projects.ports import ProjectRepositoryPort
from uuid import UUID

from .models import ProjectModel
from .dtos import ProjectCreateModel, ProjectUpdateModel


class ProjectService:
    def __init__(self, project_repository: ProjectRepositoryPort):
        self.project_repository = project_repository

    def create_project(self, project_data: ProjectCreateModel, user_id: UUID) -> ProjectModel:
        
        project = ProjectModel(
            name=project_data.name,
            description=project_data.description,
            user_id=user_id
        )
        self.project_repository.save_project(project)
        return project
    
    def get_project_by_id(self, project_id: str) -> ProjectModel | None:
        return self.project_repository.get_project_by_id(project_id)
    
    def get_projects_by_user_id(self, user_id: str) -> list[ProjectModel] | None:
        return self.project_repository.get_projects_by_user_id(user_id)
    
    def delete_project(self, project_id: str) -> None:
        self.project_repository.delete_project(project_id)

    def update_project(self, project: ProjectModel, data: dict) -> None:
        self.project_repository.update_project(project, data)