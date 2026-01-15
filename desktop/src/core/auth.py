"""
Authentication Module
User login and signup functionality
"""

import json
import os
import hashlib
from typing import Tuple, Optional, Dict, Any
from datetime import datetime

# User database file
USERS_DB_FILE = "users.json"


class UserManager:
    """Manages user authentication and account management."""
    
    def __init__(self, db_file: str = USERS_DB_FILE):
        self.db_file = db_file
        self.current_user = None
        self.users = self._load_users()
    
    def _load_users(self) -> Dict[str, Dict]:
        """Load users from JSON file."""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading users: {e}")
                return {}
        return {}
    
    def _save_users(self) -> None:
        """Save users to JSON file."""
        try:
            with open(self.db_file, 'w') as f:
                json.dump(self.users, f, indent=2)
        except Exception as e:
            print(f"Error saving users: {e}")
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA256."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def signup(self, email: str, password: str, full_name: str) -> Tuple[bool, str]:
        """
        Register a new user.
        
        Args:
            email: User email
            password: User password (minimum 6 characters)
            full_name: User's full name
            
        Returns:
            (success, message)
        """
        # Validate input
        if not email or not password or not full_name:
            return False, "All fields are required."
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters."
        
        # Check if email already exists
        if email in self.users:
            return False, "Email already registered."
        
        # Create new user
        self.users[email] = {
            'full_name': full_name,
            'password_hash': self._hash_password(password),
            'tier': 'free',  # Default to free tier
            'analyses_used': 0,
            'max_analyses': 15,  # 15 analyses per month for free tier
            'created_at': datetime.now().isoformat(),
            'last_login': None
        }
        
        self._save_users()
        return True, f"Account created successfully for {full_name}!"
    
    def login(self, email: str, password: str) -> Tuple[bool, str]:
        """
        Authenticate user.
        
        Args:
            email: User email
            password: User password
            
        Returns:
            (success, message)
        """
        if not email or not password:
            return False, "Email and password are required."
        
        if email not in self.users:
            return False, "Email not found."
        
        user = self.users[email]
        if user['password_hash'] != self._hash_password(password):
            return False, "Incorrect password."
        
        # Update last login
        user['last_login'] = datetime.now().isoformat()
        self._save_users()
        
        self.current_user = email
        return True, f"Welcome back, {user['full_name']}!"
    
    def logout(self) -> None:
        """Logout current user."""
        self.current_user = None
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in."""
        return self.current_user is not None
    
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Get current logged-in user data."""
        if self.current_user and self.current_user in self.users:
            return self.users[self.current_user]
        return None
    
    def get_user_info(self) -> Dict[str, Any]:
        """Get user info for display."""
        user = self.get_current_user()
        if user:
            return {
                'full_name': user['full_name'],
                'email': self.current_user,
                'tier': user['tier'],
                'analyses_used': user['analyses_used'],
                'max_analyses': user['max_analyses']
            }
        return {}
    
    def increment_usage(self) -> Tuple[bool, str]:
        """
        Increment usage count for current user.
        
        Returns:
            (allowed, message)
        """
        if not self.is_logged_in():
            return False, "Guest limit reached. Please sign up."
        
        user = self.get_current_user()
        if user['tier'] == 'free':
            if user['analyses_used'] >= user['max_analyses']:
                return False, "Free tier limit reached. Upgrade to Pro."
            user['analyses_used'] += 1
            self._save_users()
            remaining = user['max_analyses'] - user['analyses_used']
            return True, f"Analysis recorded. {remaining} remaining this month."
        
        return True, "Analysis recorded."
    
    def upgrade_to_pro(self, email: str, payment_id: str = "") -> Tuple[bool, str]:
        """
        Upgrade user to Pro tier.
        
        Args:
            email: User email
            payment_id: Payment transaction ID (optional)
            
        Returns:
            (success, message)
        """
        if email not in self.users:
            return False, "User not found."
        
        user = self.users[email]
        user['tier'] = 'pro'
        user['max_analyses'] = float('inf')  # Unlimited
        self._save_users()
        
        return True, "Successfully upgraded to Pro!"


