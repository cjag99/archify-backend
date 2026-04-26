import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

class SupabaseClient:
    """
    Singleton class to manage the Supabase client instance.
    Ensures that only one instance of the Supabase client is created and reused throughout the application"""
    _instance = None

    @classmethod
    def get_instance(cls) -> Client:
        """
        Retrieves the singleton instance of the Supabase client.
        If the instance does not exist, it initializes it using the URL and Key from environment variables.
        Returns:
            Client: The Supabase client instance.
        Raises:
            ValueError: If the Supabase URL or Key is not set in environment variables.
        """
        if cls._instance is None:
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_KEY")
            if not url or not key:
                raise ValueError("Supabase URL and Key must be set in environment variables.")
            
            cls._instance = create_client(url, key)
        
        return cls._instance
    
    
supabase_client = SupabaseClient.get_instance()