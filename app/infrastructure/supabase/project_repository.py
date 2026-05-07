from uuid import UUID
from app.domain.projects.ports import ProjectRepositoryPort
from app.domain.projects.models import ProjectModel
from .client import supabase_client

class SupabaseProjectRepository(ProjectRepositoryPort):
    def __init__(self):
        self.client = supabase_client
        self.table_name = "projects"

    def save_project(self, project: ProjectModel, token: str) -> None:
        try:
            project_data = {
                "name": project.name,
                "description": project.description,
                "user_id": str(project.user_id),
                "project_logo": str(project.project_logo) if project.project_logo else None,
                "architecture": str(project.architecture) if project.architecture else None,
            }

            self.client.postgrest.auth(token)
            response = self.client.from_(self.table_name).upsert(project_data).execute()
            if response.data:
                res_data = response.data[0]
                if not project.id and res_data.get("id"):
                    project.id = UUID(res_data["id"])
                if not project.created_at and res_data.get("created_at"):
                    from datetime import datetime
                    project.created_at = datetime.fromisoformat(res_data["created_at"].replace("Z", "+00:00"))
        except Exception as e:
            print(f"Error occurred while saving project: {e}")

    def get_project_by_id(self, project_id: UUID, token: str) -> ProjectModel | None:
        try:
            self.client.postgrest.auth(token)
            response = self.client.from_(self.table_name).select("*").eq("id", str(project_id)).execute()
            if response.data:
                project_data = response.data[0]
                return ProjectModel(**project_data)
            return None
        except Exception as e:
            print(f"Error occurred while retrieving project by ID: {e}")
            return None

    def get_projects_by_user_id(self, user_id: UUID, token: str) -> list[ProjectModel] | None:
        try:
            self.client.postgrest.auth(token)
            response = self.client.from_(self.table_name).select("*").eq("user_id", str(user_id)).execute()
            if response.data:
                return [ProjectModel(**project_data) for project_data in response.data]

            return None
        except Exception as e:
            print(f"Error occurred while retrieving projects by user ID: {e}")
            return None

    def delete_project(self, project_id: UUID, token: str) -> None:
        try:
            self.client.postgrest.auth(token)
            self.client.from_(self.table_name).delete().eq("id", str(project_id)).execute()
        except Exception as e:
            print(f"Error occurred while deleting project: {e}")
