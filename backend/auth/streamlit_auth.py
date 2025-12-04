"""
Streamlit authentication helper
Handles login, signup, and session management
"""

import streamlit as st
import requests
from typing import Optional, Dict


class StreamlitAuth:
    def __init__(self, api_url: str = "http://localhost:8000"):
        self.api_url = api_url
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in"""
        return 'access_token' in st.session_state and st.session_state.access_token is not None
    
    def login(self, email: str, password: str) -> Dict:
        """Login user and store token"""
        try:
            response = requests.post(
                f"{self.api_url}/auth/login",
                json={"email": email, "password": password},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                st.session_state.access_token = data['session']['access_token']
                st.session_state.user_email = data['user']['email']
                st.session_state.user_id = data['user']['id']
                return {"success": True}
            else:
                return {"success": False, "error": response.json().get('error', 'Login failed')}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def signup(self, email: str, password: str) -> Dict:
        """Signup new user"""
        try:
            response = requests.post(
                f"{self.api_url}/auth/signup",
                json={"email": email, "password": password},
                timeout=10
            )
            
            if response.status_code == 200:
                return {"success": True}
            else:
                return {"success": False, "error": response.json().get('error', 'Signup failed')}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def logout(self):
        """Logout user and clear session"""
        st.session_state.access_token = None
        st.session_state.user_email = None
        st.session_state.user_id = None
    
    def get_token(self) -> Optional[str]:
        """Get current access token"""
        return st.session_state.get('access_token')
    
    def get_user_email(self) -> Optional[str]:
        """Get current user email"""
        return st.session_state.get('user_email')
