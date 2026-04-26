from .ports import AuthPort, AuthException
from .dtos import UserLoginRequest, UserRegistrationRequest
from ..users.ports import UserRepositoryPort
from ..users.models import UserProfile

class AuthService:
    """
    Application Service that orchestrates authentication and profile creation.
    
    This service acts as a facade, coordinating the AuthPort (identity) 
    and the UserRepository (domain data).
    """

    def __init__(self, auth_port: AuthPort, user_repository: UserRepositoryPort):
        self.auth_port = auth_port
        self.user_repository = user_repository

    def register_user(self, registration_request: UserRegistrationRequest) -> UserProfile:
        """
        Registers a new user and creates their profile.
        
        This method first registers the user through the AuthPort, then creates
        a corresponding UserProfile in the domain layer.
        
        Args:
            registration_request (UserRegistrationRequest): The registration details.
        Returns:
            UserProfile: The created user profile.
        Raises:
            AuthException: If registration fails at any step.
        """
        try:
            # Register the user through the AuthPort
            user_uuid = self.auth_port.register_user(registration_request)
            
            # Create a UserProfile in the domain layer
            user_profile = UserProfile(
                id=user_uuid,
                username=registration_request.username,
                email=registration_request.email,
                first_name=registration_request.first_name,
                last_name=registration_request.last_name
            )
            self.user_repository.save(user_profile)
            
            return user_profile
        except Exception as e:
            raise AuthException(f"Registration failed: {str(e)}")
        
    def login_user(self, login_request: UserLoginRequest) -> str:      
        """
        Authenticates a user and returns their token.
        
        This method delegates authentication to the AuthPort, which handles
        credential verification and token generation.
        
        Args:
            login_request (UserLoginRequest): The login details.
        Returns:
            str: The authentication token for the authenticated user.
        Raises:
            AuthException: If login fails at any step.
        """
        try:
            token = self.auth_port.login_user(login_request)
            return token
        except Exception as e:
            raise AuthException(f"Login failed: {str(e)}")
        
    def logout_user(self, token: str) -> None:
        """
        Logs out a user based on their authentication token.
        
        This method delegates the logout process to the AuthPort, which handles
        token invalidation and session management.
        
        Args:
            token (str): The authentication token of the user to log out.
        Raises:
            AuthException: If logout fails at any step.
        """
        try:
            self.auth_port.logout_user(token)
        except Exception as e:
            raise AuthException(f"Logout failed: {str(e)}")
        
    def get_user_by_token(self, token: str) -> UserProfile:
        """
        Retrieves a user's profile based on their authentication token.
        
        This method first verifies the token through the AuthPort to get the
        user's UUID, then retrieves the corresponding UserProfile from the domain layer.
        
        Args:
            token (str): The authentication token of the user.
        Returns:
            UserProfile: The user profile associated with the provided token.
        Raises:
            AuthException: If token verification or profile retrieval fails at any step.
        """
        try:
            user_uuid = self.auth_port.verify_token(token)
            user_profile = self.user_repository.get_by_id(user_uuid)
            if not user_profile:
                raise AuthException("User profile not found for the provided token.")
            
            return user_profile
        except Exception as e:
            raise AuthException(f"Token verification failed: {str(e)}")