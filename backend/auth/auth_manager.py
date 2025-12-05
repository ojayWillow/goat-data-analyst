"""
Authentication Manager for GOAT Data Analyst
Handles user signup, login, token verification, and logout using Supabase Auth
"""

import os
from typing import Dict, Optional
from dotenv import load_dotenv
from supabase import create_client, Client
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuthManager:
    """Manages authentication operations using Supabase"""
    
    def __init__(self):
        """Initialize Supabase client"""
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
        
        self.client: Client = create_client(supabase_url, supabase_key)
        logger.info("AuthManager initialized successfully")
    
    def signup(self, email: str, password: str) -> Dict:
        """
        Register a new user
        
        Args:
            email: User's email address
            password: User's password (min 6 characters)
            
        Returns:
            Dict with user data and session info
            
        Raises:
            Exception: If signup fails
        """
        try:
            response = self.client.auth.sign_up({
                "email": email,
                "password": password
            })
            
            if response.user:
                logger.info(f"User signed up successfully: {email}")
                
                # === DAY 34: TRACK SIGNUP EVENT ===
                from backend.utils.analytics import track_event, identify_user
                user_id = response.user.id
                track_event(user_id, 'user_signup', {'email': email})
                identify_user(user_id, email, {'signup_date': response.user.created_at})
                # === END DAY 34 ===
                
                return {
                    "success": True,
                    "user": {
                        "id": response.user.id,
                        "email": response.user.email,
                        "created_at": response.user.created_at
                    },
                    "session": {
                        "access_token": response.session.access_token if response.session else None,
                        "refresh_token": response.session.refresh_token if response.session else None
                    }
                }
            else:
                logger.error(f"Signup failed for {email}")
                return {"success": False, "error": "Signup failed"}
                
        except Exception as e:
            logger.error(f"Signup error for {email}: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def login(self, email: str, password: str) -> Dict:
        """
        Authenticate an existing user
        
        Args:
            email: User's email address
            password: User's password
            
        Returns:
            Dict with user data and session tokens
            
        Raises:
            Exception: If login fails
        """
        try:
            response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if response.user:
                logger.info(f"User logged in successfully: {email}")
                
                # === DAY 34: TRACK LOGIN EVENT ===
                from backend.utils.analytics import track_event
                track_event(response.user.id, 'user_login', {'email': email})
                # === END DAY 34 ===
                
                return {
                    "success": True,
                    "user": {
                        "id": response.user.id,
                        "email": response.user.email
                    },
                    "session": {
                        "access_token": response.session.access_token,
                        "refresh_token": response.session.refresh_token,
                        "expires_at": response.session.expires_at
                    }
                }
            else:
                logger.error(f"Login failed for {email}")
                return {"success": False, "error": "Invalid credentials"}
                
        except Exception as e:
            logger.error(f"Login error for {email}: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def verify_token(self, token: str) -> Dict:
        """
        Verify if a JWT token is valid
        
        Args:
            token: JWT access token
            
        Returns:
            Dict with user data if valid, error otherwise
        """
        try:
            # Set the token in the client's auth context
            self.client.auth.set_session(token, token)
            
            # Get the user associated with this token
            user = self.client.auth.get_user()
            
            if user and user.user:
                logger.info(f"Token verified for user: {user.user.email}")
                return {
                    "success": True,
                    "user": {
                        "id": user.user.id,
                        "email": user.user.email
                    }
                }
            else:
                logger.error("Token verification failed - no user found")
                return {"success": False, "error": "Invalid token"}
                
        except Exception as e:
            logger.error(f"Token verification error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def logout(self, token: str) -> Dict:
        """
        Sign out a user (invalidates token)
        
        Args:
            token: JWT access token
            
        Returns:
            Dict indicating success or failure
        """
        try:
            # Set the session for the client
            self.client.auth.set_session(token, token)
            
            # Sign out
            response = self.client.auth.sign_out()
            
            logger.info("User logged out successfully")
            return {"success": True, "message": "Logged out successfully"}
            
        except Exception as e:
            logger.error(f"Logout error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def refresh_session(self, refresh_token: str) -> Dict:
        """
        Refresh an expired access token
        
        Args:
            refresh_token: Refresh token from login
            
        Returns:
            Dict with new access token
        """
        try:
            response = self.client.auth.refresh_session(refresh_token)
            
            if response.session:
                logger.info("Session refreshed successfully")
                return {
                    "success": True,
                    "session": {
                        "access_token": response.session.access_token,
                        "refresh_token": response.session.refresh_token,
                        "expires_at": response.session.expires_at
                    }
                }
            else:
                return {"success": False, "error": "Failed to refresh session"}
                
        except Exception as e:
            logger.error(f"Session refresh error: {str(e)}")
            return {"success": False, "error": str(e)}

# Quick test function
def test_auth():
    """Test authentication functions"""
    try:
        auth = AuthManager()
        print("✅ AuthManager initialized")
        return auth
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    # Run test
    auth = test_auth()
    if auth:
        print("\n🎯 Ready to test signup/login")
        print("Example:")
        print('result = auth.signup("test@example.com", "password123")')
        print('print(result)')
