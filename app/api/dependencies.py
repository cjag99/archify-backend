from fastapi import Depends, HTTPException, Security, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.domain.patterns.services import PatternService
from app.infrastructure.supabase.adapters import SupabaseAuthAdapter
from app.infrastructure.supabase.pattern_repository import SupabasePatternRepository
from app.infrastructure.supabase.user_repository import SupabaseUserRepository
from app.infrastructure.supabase.project_repository import SupabaseProjectRepository
from app.domain.auth.services import AuthService
from app.domain.users.models import UserProfile
from app.domain.projects.services import ProjectService

auth_service = AuthService(auth_port=SupabaseAuthAdapter(), user_repository=SupabaseUserRepository())
project_service = ProjectService(project_repository=SupabaseProjectRepository())
pattern_service = PatternService(port=SupabasePatternRepository())

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
) -> tuple[UserProfile, str] :
    """
    Dependency function to extract and verify the JWT token from the Authorization header.
    Returns the authenticated UserProfile.
    """
    try:
        user = auth_service.get_user_by_token(credentials.credentials)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        return (user, credentials.credentials)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

def is_user_admin(user_auth: tuple[UserProfile, str] = Depends(get_current_user)) -> tuple[UserProfile, str]:
    user, token = user_auth
    authorized = user.is_authorized[0] if isinstance(user.is_authorized, tuple) else user.is_authorized
    if not authorized:
        raise HTTPException(status_code=403, detail="User is not authorized to perform this action")
    return user, token

def get_pattern_service() -> PatternService:
    return pattern_service

def get_token_from_header(request: Request) -> str:
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid Authorization header"
        )
    token = auth_header.split(" ")[1]
    return token