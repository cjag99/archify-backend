from uuid import UUID

from app.domain.images.models import ImageModel, ImageUsage
from app.domain.images.ports import ImagePort
from .client import supabase_client
from .user_repository import SupabaseUserRepository


class SupabaseImageRepository(ImagePort):
    def __init__(self):
        self.client = supabase_client
        self.table_name = "images"

    def upload_image(self, image: ImageModel, token: str) -> None:
        try:
            image_dict = image.model_dump(exclude_none=True)
            if image_dict.get("id") is not None:
                image_dict["id"] = str(image_dict["id"])

            if image_dict.get("user_id") is not None:
                image_dict["user_id"] = str(image_dict["user_id"])

            if image_dict.get("created_at") is not None:
                image_dict["created_at"] = image_dict["created_at"].isoformat()
                
            self.client.postgrest.auth(token)
            response = self.client.from_(self.table_name).insert(image_dict).execute()

            if hasattr(response, 'error') and response.error:
                print(f"Database unexpected erro5: {response.error}")
                raise Exception(response.error['message'])
    
            if getattr(response, "data", None):
                res_data = response.data[0]
                if not image.id and res_data.get("id"):
                    image.id = UUID(res_data["id"])
                if not image.created_at and res_data.get("created_at"):
                    from datetime import datetime
                    image.created_at = datetime.fromisoformat(res_data["created_at"].replace("Z", "+00:00"))

        except Exception as e:
            print(f"Error occurred while saving: {e}")

    def get_image_by_id(self, user_id: UUID, image_id: UUID, token: str) -> ImageModel | None:
        try:
            user = SupabaseUserRepository().get_user_by_id(user_id, token)
            if not user:
                return None

            self.client.postgrest.auth(token)
            response = (
                self.client.from_(self.table_name)
                .select("*")
                .eq("id", str(image_id))
                .execute()
            )

            if not getattr(response, "data", None):
                return None

            image = ImageModel(**response.data[0])
            shared_usage = {
                ImageUsage.CODE_LOGO,
                ImageUsage.PATTERN_GRAPHIC,
            }
            if user.is_authorized or image.user_id == user_id or image.usage_type in shared_usage:
                return image

            return None

        except Exception as e:
            print(f"Error occurred while retrieving image: {e}")
            return None

    def get_all_images(self, token: str) -> list[ImageModel] | None:
        try:
            self.client.postgrest.auth(token)
            response = self.client.from_(self.table_name).select("*").execute()
            if not getattr(response, "data", None):
                return None

            return [ImageModel(**row) for row in response.data]

        except Exception as e:
            print(f"Error occurred while showing all images: {e}")
            return None

    def get_user_images(self, user_id: UUID, token: str) -> list[ImageModel] | None:
        try:
            self.client.postgrest.auth(token)
            response = self.client.from_(self.table_name).select("*").eq("user_id", str(user_id)).execute()
            if not getattr(response, "data", None):
                return None

            return [ImageModel(**row) for row in response.data]

        except Exception as e:
            print(f"Error occurred while showing user images: {e}")
            return None

    def delete_image(self, image_id: UUID, token: str) -> None:
        try:
            self.client.postgrest.auth(token)
            self.client.from_(self.table_name).delete().eq("id", str(image_id)).execute()

        except Exception as e:
            print(f"Error occurred while deleting image: {e}")
