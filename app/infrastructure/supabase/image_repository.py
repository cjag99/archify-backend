from uuid import UUID

from app.domain.images.models import ImageModel, ImageUsage
from app.domain.images.ports import ImagePort
from .client import supabase_client, supabase_admin_client
from .user_repository import SupabaseUserRepository
from .storage import (
    build_storage_object_path,
    create_storage_object_url,
    extract_storage_path_from_url,
    get_storage_bucket,
    refresh_storage_url,
)


class SupabaseImageRepository(ImagePort):
    """
    Repository class to manage images in the Supabase database.
    This class implements the ImagePort interface, providing methods to upload and retrieve images using the Supabase client.
    """
    def __init__(self):
        """
        Initializes the SupabaseImageRepository with the Supabase client and sets the table name.
        """
        self.client = supabase_client
        self.table_name = "images"

    def upload_image(self, file_bytes: bytes, file_name: str, content_type: str, usage_type: ImageUsage, user_id: UUID, token: str) -> ImageModel:
        """
        Uploads an image file to Supabase storage and creates an image record in the database.
        Args:
            file_bytes (bytes): The raw bytes of the image file.
            file_name (str): The name of the file.
            content_type (str): The MIME type of the file.
            usage_type (ImageUsage): The intended usage of the image.
            user_id (UUID): The ID of the user uploading the image.
            token (str): The authentication token for the request.
        Returns:
            ImageModel: The saved image record.
        Raises:
            Exception: If storage upload or database insert fails.
        """
        try:
            image_path, display_file_name = build_storage_object_path(
                str(user_id),
                file_name,
                content_type,
            )

            self.client.auth(token)
            bucket = get_storage_bucket()
            storage_response = self.client.storage.from_(bucket).upload(
                path=image_path,
                file=file_bytes,
                file_options={"contentType": content_type},
            )

            if getattr(storage_response, "error", None):
                raise Exception(f"Storage upload failed: {storage_response.error}")

            image_url = create_storage_object_url(image_path)

            image = ImageModel(
                file_name=display_file_name,
                url=image_url,
                usage_type=usage_type,
                user_id=user_id
            )
            image_dict = image.model_dump(exclude_none=True)
            if image_dict.get("id") is not None:
                image_dict["id"] = str(image_dict["id"])

            if image_dict.get("user_id") is not None:
                image_dict["user_id"] = str(image_dict["user_id"])

            if image_dict.get("created_at") is not None:
                image_dict["created_at"] = image_dict["created_at"].isoformat()
                
            # Use admin client to bypass RLS policies for table insert
            response = supabase_admin_client.from_(self.table_name).insert(image_dict).execute()

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
            return image

        except Exception as e:
            print(f"Error occurred while saving: {e}")
            raise

    def get_image_by_id(self, user_id: UUID, image_id: UUID, token: str) -> ImageModel | None:
        """
        Retrieves an image by its unique identifier from the Supabase database.
        Args:
            user_id (UUID): The ID of the user requesting the image.
            image_id (UUID): The unique identifier of the image to retrieve.
            token (str): The authentication token for the request.
        Returns:
            ImageModel | None: The image associated with the provided ID, or None if not found or unauthorized.
        """
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
            image.url = refresh_storage_url(image.url)
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
        """
        Retrieves all images from the Supabase database.
        Args:
            token (str): The authentication token for the request.
        Returns:
            list[ImageModel] | None: The list of all images, or None if not found.
        """
        try:
            self.client.postgrest.auth(token)
            response = self.client.from_(self.table_name).select("*").execute()
            if not getattr(response, "data", None):
                return None

            images = [ImageModel(**row) for row in response.data]
            for img in images:
                img.url = refresh_storage_url(img.url)
            return images

        except Exception as e:
            print(f"Error occurred while showing all images: {e}")
            return None

    def get_user_images(self, user_id: UUID, token: str) -> list[ImageModel] | None:
        """
        Retrieves all images belonging to a specific user from the Supabase database.
        Args:
            user_id (UUID): The unique identifier of the user.
            token (str): The authentication token for the request.
        Returns:
            list[ImageModel] | None: The list of images associated with the user, or None if not found.
        """
        try:
            self.client.postgrest.auth(token)
            response = self.client.from_(self.table_name).select("*").eq("user_id", str(user_id)).execute()
            if not getattr(response, "data", None):
                return None

            images = [ImageModel(**row) for row in response.data]
            for img in images:
                img.url = refresh_storage_url(img.url)
            return images

        except Exception as e:
            print(f"Error occurred while showing user images: {e}")
            return None

    def delete_image(self, image_id: UUID, token: str) -> None:
        """
        Deletes an image from Supabase storage and its corresponding record in the database.
        Args:
            image_id (UUID): The unique identifier of the image to delete.
            token (str): The authentication token for the request.
        Raises:
            Exception: If deleting the image fails for any reason.
        """
        try:
            self.client.postgrest.auth(token)
            response = self.client.from_(self.table_name).select("*").eq("id", str(image_id)).execute()
            
            if getattr(response, "data", None):
                image_url = response.data[0]["url"]
                bucket_name = get_storage_bucket()
                file_path = extract_storage_path_from_url(image_url, bucket_name)
                
                if file_path:
                    self.client.storage.from_(bucket_name).remove([file_path])
            
            # Use admin client to bypass RLS policies for table delete
            supabase_admin_client.from_(self.table_name).delete().eq("id", str(image_id)).execute()

        except Exception as e:
            print(f"Error occurred while deleting image: {e}")
            raise
