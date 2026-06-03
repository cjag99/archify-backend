from uuid import UUID

from .client import supabase_client
from app.domain.app_configs.ports import AppConfigPort
from ...domain.app_configs.models import AppConfigModel


class SupabaseAppConfigService(AppConfigPort):
    """
    Repository class to manage app configurations in the Supabase database.
    This class implements the AppConfigPort interface, providing methods to save and retrieve app configurations using the Supabase client.
    """
    def __init__(self):
        """
        Initializes the SupabaseAppConfigService with the Supabase client and sets the table name.
        """
        self.client = supabase_client
        self.table_name = "app_configs"

    def save_config(self, config: AppConfigModel, token: str) -> None:
        """
        Saves an app configuration to the Supabase database.
        Args:
            config (AppConfigModel): The app configuration to save.
            token (str): The authentication token for the request.
        Raises:
            Exception: If saving the app configuration fails for any reason.
        """
        try:
            config_dict = config.model_dump(exclude_none=True)
            if config_dict.get("id") is not None:
                config_dict["id"] = str(config_dict.get("id"))

            if config_dict.get("created_at") is not None:
                config_dict["created_at"] = config_dict.get("created_at").isoformat()

            self.client.postgrest.auth(token)
            response = self.client.from_(self.table_name).update(config_dict).execute()
            
            if hasattr(response, 'error') and response.error:
                print(f"Database unexpected error: {response.error}")
                raise Exception(response.error['message'])

            if getattr(response, "data", None):
                res_data = response.data[0]
                if not config.id and res_data.get("id"):
                    config.id = UUID(res_data["id"])
                if not config.created_at and res_data.get("created_at"):
                    from datetime import datetime
                    config.created_at = datetime.fromisoformat(res_data["created_at"].replace("Z", "+00:00"))

        except Exception as e:
            print(f"Error occurred while saving: {e}")

    def get_all_configs(self, token: str) -> list[AppConfigModel]:
        """
        Retrieves all app configurations from the Supabase database.
        Args:
            token (str): The authentication token for the request.
        Returns:
            list[AppConfigModel]: The list of all app configurations, or None if not found.
        """
        try:
            self.client.postgrest.auth_token(token)
            res = self.client.from_(self.table_name).select("*").execute()

            if not getattr(res, "data", None):
                return None

            return [AppConfigModel(**row) for row in res.data]

        except Exception as e:
            print(f"Error occurred while showing all app configs: {e}")
            return None

    def get_config_by_id(self, config_id: UUID, token: str) -> AppConfigModel:
        """
        Retrieves an app configuration by its unique identifier from the Supabase database.
        Args:
            config_id (UUID): The unique identifier of the app configuration to retrieve.
            token (str): The authentication token for the request.
        Returns:
            AppConfigModel: The app configuration associated with the provided ID, or None if not found.
        """
        try:
            self.client.postgrest.auth_token(token)
            res = self.client.from_(self.table_name).select("*").eq("id", str(config_id)).execute()

            if not getattr(res, "data", None):
                return None

            return AppConfigModel(**res.data[0])

        except Exception as e:
            print(f"Error occurred while retrieving app config: {e}")
            return None

    def get_config_by_key(self, key: str, token: str) -> AppConfigModel:
        """
        Retrieves an app configuration by its key from the Supabase database.
        Args:
            key (str): The key of the app configuration to retrieve.
            token (str): The authentication token for the request.
        Returns:
            AppConfigModel: The app configuration associated with the provided key, or None if not found.
        """
        try:
            self.client.postgrest.auth_token(token)
            res = self.client.from_(self.table_name).select("*").eq(key, key).execute()

            if not getattr(res, "data", None):
                return None

            return AppConfigModel(**res.data[0])

        except Exception as e:
            print(f"Error occurred while retrieving app config: {e}")
            return None

    def get_enabled_configs(self) -> dict[str, str]:
        """
        Retrieves a dictionary of all active app configurations.
        Returns:
            dict[str, str]: A dictionary mapping configuration keys to their string values.
        """
        try:

            res = self.client.rpc("get_active_app_configs").execute()

            if not getattr(res, "data", None):
                return {}

            return {row["key"]: row["value"] for row in res.data}

        except Exception as e:
            print(f"Error occurred while retrieving enabled keys: {e}")
            return None

    def delete_config(self, config_id: UUID, token: str) -> None:
        """
        Deletes an app configuration from the Supabase database based on its unique identifier.
        Args:
            config_id (UUID): The unique identifier of the app configuration to delete.
            token (str): The authentication token for the request.
        """
        try:
            self.client.postgrest.auth_token(token)
            self.client.from_(self.table_name).delete().eq("id", config_id).execute()

        except Exception as e:
            print(f"Error occurred while deleting architecture: {e}")
