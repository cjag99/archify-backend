from fastapi import Depends, HTTPException, Security, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.domain.app_configs.services import AppConfigService
from app.domain.architectures.services import ArchitectureService
from app.domain.code_languages.services import CodeLanguagesService
from app.domain.images.services import ImageServices
from app.domain.patterns.services import PatternService
from app.domain.patterns_code.services import PatternCodeService
from app.domain.profile_settings.services import ProfileSettingService
from app.domain.settings.services import SettingsService
from app.domain.users.services import UserService
from app.infrastructure.supabase.adapters import SupabaseAuthAdapter
from app.infrastructure.supabase.app_configs_repository import SupabaseAppConfigService
from app.infrastructure.supabase.architecture_repository import SupabaseArchitectureRepository
from app.infrastructure.supabase.code_language_repository import SupabaseCodeLanguageRepository
from app.infrastructure.supabase.image_repository import SupabaseImageRepository
from app.infrastructure.supabase.pattern_code_repository import SupabasePatternCodeRepository
from app.infrastructure.supabase.pattern_repository import SupabasePatternRepository
from app.infrastructure.supabase.profile_setting_repository import SupabaseProfileSettingRepository
from app.infrastructure.supabase.setting_repository import SupabaseSettingsRepository
from app.infrastructure.supabase.user_repository import SupabaseUserRepository
from app.infrastructure.supabase.project_repository import SupabaseProjectRepository
from app.domain.auth.services import AuthService
from app.domain.users.models import UserProfile
from app.domain.projects.services import ProjectService

auth_service = AuthService(auth_port=SupabaseAuthAdapter(), user_port=SupabaseUserRepository())
project_service = ProjectService(port=SupabaseProjectRepository())
pattern_service = PatternService(port=SupabasePatternRepository())
user_service = UserService(user_port=SupabaseUserRepository())
architecture_service = ArchitectureService(port=SupabaseArchitectureRepository())
code_language_service = CodeLanguagesService(port=SupabaseCodeLanguageRepository())
pattern_code_service = PatternCodeService(port=SupabasePatternCodeRepository())
image_service = ImageServices(port=SupabaseImageRepository())
app_config_service = AppConfigService(port=SupabaseAppConfigService())
settings_service = SettingsService(port=SupabaseSettingsRepository())
profile_settings_service = ProfileSettingService(port=SupabaseProfileSettingRepository())

def get_auth_service() -> AuthService:
    """
    Dependency function to provide an instance of AuthService.
    
    This function can be used with FastAPI's Depends to inject the AuthService into API endpoints.

    Returns:
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
) -> tuple[UserProfile, str]:
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
    """
    Dependency function to check if the current user has admin privileges.

    Args:
        user_auth (tuple[UserProfile, str]): A tuple containing the UserProfile and token.

    Returns:
        tuple[UserProfile, str]: The authorized UserProfile and token.

    Raises:
        HTTPException: If the user is not authorized.
    """
    user, token = user_auth
    authorized = user.is_authorized[0] if isinstance(user.is_authorized, tuple) else user.is_authorized
    if not authorized:
        raise HTTPException(status_code=403, detail="User is not authorized to perform this action")
    return user, token

def get_pattern_service() -> PatternService:
    """
    Dependency function to provide an instance of PatternService.

    Returns:
        PatternService: An instance of the PatternService class.
    """
    return pattern_service

def get_user_service() -> UserService:
    """
    Dependency function to provide an instance of UserService.

    Returns:
        UserService: An instance of the UserService class.
    """
    return user_service

def get_architecture_service() -> ArchitectureService:
    """
    Dependency function to provide an instance of ArchitectureService.

    Returns:
        ArchitectureService: An instance of the ArchitectureService class.
    """
    return architecture_service

def get_code_language_service() -> CodeLanguagesService:
    """
    Dependency function to provide an instance of CodeLanguagesService.

    Returns:
        CodeLanguagesService: An instance of the CodeLanguagesService class.
    """
    return code_language_service

def get_pattern_code_service() -> PatternCodeService:
    """
    Dependency function to provide an instance of PatternCodeService.

    Returns:
        PatternCodeService: An instance of the PatternCodeService class.
    """
    return pattern_code_service

def get_image_service() -> ImageServices:
    """
    Dependency function to provide an instance of ImageServices.

    Returns:
        ImageServices: An instance of the ImageServices class.
    """
    return image_service

def get_app_config_service() -> AppConfigService:
    """
    Dependency function to provide an instance of AppConfigService.

    Returns:
        AppConfigService: An instance of the AppConfigService class.
    """
    return app_config_service

def get_settings_service() -> SettingsService:
    """
    Dependency function to provide an instance of SettingsService.

    Returns:
        SettingsService: An instance of the SettingsService class.
    """
    return settings_service

def get_profile_settings_service() -> ProfileSettingService:
    """
    Dependency function to provide an instance of ProfileSettingService.

    Returns:
        ProfileSettingService: An instance of the ProfileSettingService class.
    """
    return profile_settings_service
