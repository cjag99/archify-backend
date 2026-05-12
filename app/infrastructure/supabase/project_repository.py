from uuid import UUID

from app.domain.projects.ports import ProjectPort
from app.domain.projects.models import ProjectModel
from .client import supabase_client

class SupabaseProjectRepository(ProjectPort):
    """
    Repository class to manage projects in the Supabase database.
    This class implements the ProjectPort interface, providing methods to save and retrieve projects using the Supabase client.
    """
    def __init__(self):
        self.client = supabase_client
        self.table_name = "projects"

    def save_project(self, project: ProjectModel, token: str) -> None:
        """
        Saves a profile to the Supabase database.
        Args:
            project (ProjectModel): The project to save.
            token (str): The autheunticated user bearer token.
        Raises:
            Exception: If saving the project fails for any reason.
        """
        try:
            project_dict = {project.model_dump(exclude_none=True)}
            self.client.postgrest.auth(token)
            response = self.client.from_(self.table_name).upsert(project_dict).execute()

            if hasattr(response, 'error') and response.error:
                print(f"Database unexpected error: {response.error}")
                raise Exception(response.error['message'])

            if getattr(response, "data", None):
                res_data = response.data[0]
                if not project.id and res_data.get("id"):
                    project.id = UUID(res_data["id"])
                if not project.created_at and res_data.get("created_at"):
                    from datetime import datetime
                    project.created_at = datetime.fromisoformat(res_data["created_at"].replace("Z", "+00:00"))

        except Exception as e:
            print(f"Error occurred while saving project: {e}")

    def get_project_by_id(self, project_id: UUID, token: str) -> ProjectModel | None:
        """
        Retrieves a project by its unique identifier from the Supabase database.
        Args:
            project_id (UUID): The unique identifier of the project to retrieve.
            token (str): The authentication token for the request.
        Returns:
            ProjectModel | None: The project associated with the provided ID, or None if not found.
        Raises:
            Exception: If retrieving the project fails for any reason.
        """
        try:
            self.client.postgrest.auth(token)
            response = self.client.from_(self.table_name).select("*").eq("id", str(project_id)).execute()
            if not getattr(response, "data", None):
                return None
            return ProjectModel(**response.data[0])

        except Exception as e:
            print(f"Error occurred while retrieving project by ID: {e}")
            return None

    def get_projects_by_user_id(self, user_id: UUID, token: str) -> list[ProjectModel] | None:
        """
        Retrieves all projects from a user by the owner's unique identifier from the Supabase database.
        Args:
            user_id (UUID): The unique identifier of the owner of all projects to retrieve.
            token (str): The authentication token for the request.
        Returns:
            list[ProjectModel] | None: The list of projects associated with the owner provided ID, or None if not found.
        Raises:
            Exception: If retrieving the list of projects fails for any reason.
        """
        try:
            self.client.postgrest.auth(token)
            response = self.client.from_(self.table_name).select("*").eq("user_id", str(user_id)).execute()
            if not getattr(response, "data", None):
                return None
            return [ProjectModel(**row) for row in response.data]

        except Exception as e:
            print(f"Error occurred while retrieving projects by user ID: {e}")
            return None

    def get_all_projects(self, token: str) -> list[ProjectModel] | None:
        """
        Retrieves all projects from the Supabase database.
        Args:
            token (str): The authentication token for the request.
        Returns:
            list[ProjectModel] | None: The list of all projects, or None if not found.
        Raises:
            Exception: If retrieving all projects fails for any reason.
        """
        try:
            self.client.postgrest.auth(token)
            response = self.client.from_(self.table_name).select("*").execute()
            if not getattr(response, "data", None):
                return None
            return [ProjectModel(**row) for row in response.data]

        except Exception as e:
            print(f"Error occurred while retrieving all projects: {e}")
            return None

    def delete_project(self, project_id: UUID, token: str) -> None:
        """
        Deletes a project from the Supabase database based on its unique identifier.
        Args:
            project_id (UUID): The unique identifier of the project to delete.
            token (str): The authentication token for the request.
        Raises:
            Exception: If deleting the project fails for any reason.
        """
        try:
            self.client.postgrest.auth(token)
            self.client.from_(self.table_name).delete().eq("id", str(project_id)).execute()

        except Exception as e:
            print(f"Error occurred while deleting project: {e}")
