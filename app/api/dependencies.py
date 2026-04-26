from app.infrastructure.supabase.adapters import SupabaseAuthAdapter
from app.infrastructure.supabase.user_repository import SupabaseUserRepository
from app.domain.auth.services import AuthService

auth_adapter = SupabaseAuthAdapter()
user_repository = SupabaseUserRepository()
auth_service = AuthService(auth_port=auth_adapter, user_repository=user_repository)
def get_auth_service() -> AuthService:
    """
    Dependency function to provide an instance of AuthService.
    
    This function can be used with FastAPI's Depends to inject the AuthService into API endpoints.
    
    Returns:
        AuthService: An instance of the AuthService class, initialized with the necessary adapters and repositories.
    """
    return auth_service