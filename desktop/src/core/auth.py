"""
Authentication Module
User login and signup functionality
"""

import logging
from typing import Tuple, Optional, Dict, Any
from database.models import UserManager as DatabaseUserManager

logger = logging.getLogger(__name__)


class AuthenticationService:
    """Handles user authentication"""
    
    def __init__(self, db_path: str = "./data/skintelli.db"):
        self.user_manager = DatabaseUserManager(db_path)
        self.current_user = None
    
    def signup(self, username: str, password: str, email: str = "") -> Tuple[bool, str]:
        """
        Register a new user
        
        Returns:
            (success, message)
        """
        if not username or not password:
            return False, "Username and password are required"
        
        success, msg = self.user_manager.create_user(username, password, email)
        
        if success:
            logger.info(f"User signed up: {username}")
        else:
            logger.warning(f"Signup failed: {msg}")
        
        return success, msg
    
    def login(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Authenticate user
        
        Returns:
            (success, message)
        """
        if not username or not password:
            return False, "Username and password are required"
        
        success, msg = self.user_manager.authenticate_user(username, password)
        
        if success:
            self.current_user = username
            logger.info(f"User logged in: {username}")
        else:
            logger.warning(f"Login failed for user: {username}")
        
        return success, msg
    
    def logout(self):
        """Logout current user"""
        if self.current_user:
            logger.info(f"User logged out: {self.current_user}")
            self.current_user = None
    
    def get_current_user(self) -> str:
        """Get currently logged in user"""
        return self.current_user
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return self.current_user is not None
    
    def user_exists(self, username: str) -> bool:
        """Check if user exists"""
        return self.user_manager.user_exists(username)
    
    def close(self):
        """Close database connection"""
        self.user_manager.close()

