import os
from pathlib import Path
from urllib.parse import unquote, urlparse
from uuid import uuid4

from app.infrastructure.supabase.client import supabase_client

DEFAULT_STORAGE_BUCKET = "archify"
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg"}
DEFAULT_SIGNED_URL_EXPIRES_SECONDS = 60 * 60 * 24 * 7  # 7 days


def get_storage_bucket() -> str:
    """Supabase Storage bucket id used for image uploads."""
    return os.getenv("SUPABASE_STORAGE_BUCKET", DEFAULT_STORAGE_BUCKET)


def is_public_storage_bucket() -> bool:
    return os.getenv("SUPABASE_STORAGE_PUBLIC", "").lower() in ("1", "true", "yes")


def extract_storage_path_from_url(url: str, bucket: str | None = None) -> str | None:
    """Extract object path inside the bucket from a Supabase storage URL."""
    bucket = bucket or get_storage_bucket()
    parsed = urlparse(url)
    path = unquote(parsed.path)

    markers = (
        f"/object/public/{bucket}/",
        f"/object/sign/{bucket}/",
        f"/{bucket}/",
    )
    for marker in markers:
        if marker in path:
            return path.split(marker, 1)[1]

    return None


def create_storage_object_url(storage_path: str) -> str:
    """
    Return a browser-usable URL for a storage object.
    Private buckets need signed URLs (what Supabase UI copies with 'Copy URL').
    Public buckets can use /object/public/... URLs.
    """
    bucket = get_storage_bucket()

    if is_public_storage_bucket():
        return supabase_client.storage.from_(bucket).get_public_url(storage_path)

    expires_in = int(
        os.getenv("SUPABASE_SIGNED_URL_EXPIRES", str(DEFAULT_SIGNED_URL_EXPIRES_SECONDS))
    )
    result = supabase_client.storage.from_(bucket).create_signed_url(
        storage_path,
        expires_in,
    )

    if isinstance(result, dict):
        signed = (
            result.get("signedURL")
            or result.get("signedUrl")
            or result.get("signed_url")
        )
        if signed:
            return signed

    raise ValueError(f"Could not create signed URL for storage path: {storage_path}")


def refresh_storage_url(stored_url: str) -> str:
    """Rebuild a working URL from any previously stored Supabase storage link."""
    storage_path = extract_storage_path_from_url(stored_url)
    if not storage_path:
        return stored_url
    return create_storage_object_url(storage_path)


def build_storage_object_path(user_id: str, original_filename: str | None, content_type: str) -> tuple[str, str]:
    """
    Build a storage-safe object path (no spaces or special chars) and keep the
    original filename for display in the database.

    Returns:
        (storage_path, display_file_name)
    """
    display_name = (original_filename or "image").replace("\\", "/").split("/")[-1].strip() or "image"
    path = Path(display_name)
    ext = path.suffix.lower()

    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        guessed = {
            "image/jpeg": ".jpg",
            "image/png": ".png",
            "image/webp": ".webp",
            "image/gif": ".gif",
            "image/svg+xml": ".svg",
        }.get(content_type)
        ext = guessed or ".bin"

    safe_filename = f"{uuid4()}{ext}"
    storage_path = f"{user_id}/{safe_filename}"
    return storage_path, display_name