from app.infrastructure.supabase.adapters import SupabaseAuthAdapter
from app.infrastructure.supabase.user_repository import SupabaseUserRepository
from app.infrastructure.supabase.project_repository import SupabaseProjectRepository
from app.domain.auth.services import AuthService
from app.domain.projects.services import ProjectService
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.domain.users.models import UserProfile
from app.domain.projects.services import ProjectService

auth_adapter = SupabaseAuthAdapter()
user_repository = SupabaseUserRepository()
auth_service = AuthService(auth_port=auth_adapter, user_repository=user_repository)

project_repository = SupabaseProjectRepository()
project_service = ProjectService(project_repository=project_repository)
def get_auth_service() -> AuthService:
    """
    Dependency function to provide an instance of AuthService.
    
    This function can be used with FastAPI's Depends to inject the AuthService into API endpoints.
    
        AuthService: An instance of the AuthService class, initialized with the necessary adapters and repositories.
    """
    return auth_service

def get_project_service() -> ProjectService:
    """
    Dependency function to provide an instance of ProjectService.
    
    This function can be used with FastAPI's Depends to inject the ProjectService into API endpoints.
    
    Returns:
        ProjectService: An instance of the ProjectService class, initialized with the necessary repositories.
    """
    return project_service

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    auth_service: AuthService = Depends(get_auth_service)
) -> UserProfile:
    """
    Dependency function to extract and verify the JWT token from the Authorization header.
    Returns the authenticated UserProfile.
    """
    try:
        user = auth_service.get_user_by_token(credentials.credentials)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))