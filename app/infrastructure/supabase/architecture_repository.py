from uuid import UUID

from .client import supabase_client
from app.domain.architectures.models import ArchitectureModel
from app.domain.architectures.ports import ArchitecturePort

class SupabaseArchitectureRepository(ArchitecturePort):
    """
    Repository class to manage architectures in the Supabase database.
    This class implements the ArchitecturePort interface, providing methods to save and retrieve architectures using the Supabase client.
    """
    def __init__(self):
        self.client = supabase_client
        self.table_name = "architectures"

    def save_architecture(self, architecture: ArchitectureModel, token: str) -> None:
        """
        Saves an architecture to the Supabase database.
        Args:
            architecture (ArchitectureModel): The architecture to save.
            token (str): The autheuntication token for the request.
        Raises:
            Exception: If saving the architecture fails for any reason.
        """
        try:
            architecture_dict = architecture.model_dump(exclude_none=True)
            if architecture_dict.get("id") is not None:
                architecture_dict["id"] = str(architecture_dict["id"])

            if architecture_dict.get("created_at") is not None:
                architecture_dict["created_at"] = architecture_dict["created_at"].isoformat()

            self.client.postgrest.auth(token)
            response = self.client.from_(self.table_name).upsert(architecture_dict).execute()

            if hasattr(response, 'error') and response.error:
                print(f"Database unexpected error: {response.error}")
                raise Exception(response.error['message'])

            if getattr(response, "data", None):
                res_data = response.data[0]
                if not architecture.id and res_data.get("id"):
                    architecture.id = UUID(res_data["id"])
                if not architecture.created_at and res_data.get("created_at"):
                    from datetime import datetime
                    architecture.created_at = datetime.fromisoformat(res_data["created_at"].replace("Z", "+00:00"))

        except Exception as e:
            print(f"Error occurred while saving: {e}")

    def get_all_architectures(self, token:str) -> list[ArchitectureModel] | None:
        """
        Retrieves all architectures from the Supabase database.
        Args:
            token (str): The authentication token for the request.
        Returns:
            list[ArchitectureModel] | None: The list of all architectures, or None if not found.
        Raises:
            Exception: If retrieving all architectures fails for any reason.
        """
        try:
            self.client.postgrest.auth(token)
            res = self.client.from_(self.table_name).select("*").execute()

            if not getattr(res, "data", None):
                return None

            return [ArchitectureModel(**row) for row in res.data]

        except Exception as e:
            print(f"Error occurred while showing all architectures: {e}")
            return None

    def get_architecture_by_id(self, architecture_id: UUID, token: str) -> ArchitectureModel | None:
        """
         Retrieves an architecture by its unique identifier from the Supabase database.
        Args:
            architecture_id (UUID): The unique identifier of the architecture to retrieve.
            token (str): The authentication token for the request.
        Returns:
            ArchitectureModel | None: The architecture associated with the provided ID, or None if not found.
        Raises:
            Exception: If retrieving the architecture fails for any reason.
        """
        try:
            self.client.postgrest.auth(token)
            res = self.client.from_(self.table_name).select("*").eq("id", str(architecture_id)).execute()

            if not getattr(res, "data", None):
                return None

            return ArchitectureModel(**res.data[0])

        except Exception as e:
            print(f"Error occurred while retrieving architecture: {e}")
            return None

    def delete_architecture(self, architecture_id: UUID, token: str) -> None:
        """
        Deletes an architecture from the Supabase database based on its unique identifier.
        Args:
            architecture_id (UUID): The unique identifier of the architecture to delete.
            token (str): The authentication token for the request.
        Raises:
            Exception: If deleting the architecture fails for any reason.
        """
        try:
            self.client.postgrest.auth(token)
            self.client.from_(self.table_name).delete().eq("id", architecture_id).execute()

        except Exception as e:
            print(f"Error occurred while deleting architecture: {e}")
