from app.domain.auth.dtos import UserLoginRequest, UserRegistrationRequest
from uuid import UUID

from app.domain.auth.ports import AuthException, AuthPort
from .client import supabase_client

class SupabaseAuthAdapter(AuthPort):
    """
    Adapter class to interact with the Supabase client.
    This class serves as a bridge between the application and the Supabase client, providing methods to perform various operations such as user registration, login, and token verification.
    """
    def __init__(self):
        self.client = supabase_client

    def register_user(self, registration_request: UserRegistrationRequest) -> UUID:
        """
        Registers a new user with the provided email and password.
        Args:
            registration_request (UserRegistrationRequest): The registration request containing email and password.
        Returns:
            UUID: The unique identifier of the newly registered user.
        Raises:
            Exception: If registration fails due to any reason.
        """
        try:
            response = self.client.auth.sign_up({
                "email": registration_request.email, 
                "password": registration_request.password
            })

            if not response.user:
                raise AuthException("No user data returned from Supabase.")

            return UUID(response.user.id)

        except Exception as e:
            raise AuthException(f"User registration failed: {str(e)}")
        
    def login_user(self, login_request: UserLoginRequest) -> str:
        """
        Authenticates a user with the provided email and password.
        Args:
            login_request (UserLoginRequest): The login request containing email and password.
        Returns:
            str: The authentication token for the authenticated user.
        Raises:
            Exception: If login fails due to any reason.
        """
        try:
            response = self.client.auth.sign_in_with_password({
                "email": login_request.email, 
                "password": login_request.password
            })

            if not response.session or not response.session.access_token:
                raise AuthException("Authentication failed: No session or access token returned.")

            return response.session.access_token

        except Exception as e:
            raise AuthException(f"User login failed: {str(e)}")
        
    def logout_user(self, token: str) -> None:
        """
        Logs out the user associated with the provided authentication token.
        Args:
            token (str): The authentication token of the user to log out.
        Raises:
            Exception: If logout fails due to any reason.
        """
        try:
            self.client.auth.sign_out()
        except Exception as e:
            raise AuthException(f"User logout failed: {str(e)}")
        
    def verify_token(self, token: str) -> UUID:
        """
        Verifies the provided authentication token and retrieves the associated user's unique identifier.
        Args:
            token (str): The authentication token to verify.
        Returns:
            UUID: The unique identifier of the user associated with the provided token.
        Raises:
            Exception: If token verification fails due to any reason.
        """
        try:
            response = self.client.auth.get_user(token)

            if not response.user or not response.user.id:
                raise AuthException("Token verification failed: No user data returned.")

            return UUID(response.user.id)

        except Exception as e:
            raise AuthException(f"Token verification failed: {str(e)}")