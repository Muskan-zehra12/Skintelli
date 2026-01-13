"""
Authentication and User Management
Handles user registration, login, and session management.
"""
import json
import os
import hashlib
from typing import Dict, Tuple, Optional
from datetime import datetime


class UserManager:
    """Manages user accounts, login, and authentication."""
    
    def __init__(self, db_path: str = "users.json"):
        self.db_path = db_path
        self.current_user = None
        self.load_users()
    
    def load_users(self):
        """Load users from JSON database."""
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, 'r') as f:
                    self.users = json.load(f)
            except Exception:
                self.users = {}
        else:
            self.users = {}
    
    def save_users(self):
        """Save users to JSON database."""
        try:
            with open(self.db_path, 'w') as f:
                json.dump(self.users, f, indent=2)
        except Exception as e:
            raise Exception(f"Failed to save users: {e}")
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA256."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def signup(self, email: str, password: str, full_name: str) -> Tuple[bool, str]:
        """
        Register a new user.
        
        Returns:
            Tuple of (success, message)
        """
        # Validate input
        if not email or not password or not full_name:
            return False, "All fields are required."
        
        if "@" not in email:
            return False, "Invalid email format."
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters."
        
        # Check if user already exists
        if email in self.users:
            return False, "Email already registered."
        
        # Create user
        self.users[email] = {
            'full_name': full_name,
            'password': self.hash_password(password),
            'tier': 'free',
            'analyses_used': 0,
            'max_analyses': 15,
            'created_at': datetime.now().isoformat(),
            'last_login': None
        }
        
        self.save_users()
        return True, "Account created successfully! Please log in."
    
    def login(self, email: str, password: str) -> Tuple[bool, str]:
        """
        Authenticate user login.
        
        Returns:
            Tuple of (success, message)
        """
        if email not in self.users:
            return False, "Email not found. Please sign up first."
        
        user = self.users[email]
        if user['password'] != self.hash_password(password):
            return False, "Incorrect password."
        
        # Update last login
        user['last_login'] = datetime.now().isoformat()
        self.save_users()
        
        self.current_user = email
        return True, "Login successful!"
    
    def logout(self):
        """Logout current user."""
        self.current_user = None
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in."""
        return self.current_user is not None
    
    def get_current_user(self) -> Optional[Dict]:
        """Get current user data."""
        if not self.current_user or self.current_user not in self.users:
            return None
        return self.users[self.current_user]
    
    def get_user_info(self) -> Dict:
        """Get current user information."""
        if not self.is_logged_in():
            return {
                'email': 'Guest',
                'full_name': 'Unauthorized User',
                'tier': 'guest',
                'analyses_remaining': 3,
                'analyses_used': 0
            }
        
        user = self.get_current_user()
        return {
            'email': self.current_user,
            'full_name': user['full_name'],
            'tier': user['tier'],
            'analyses_remaining': user['max_analyses'] - user['analyses_used'],
            'analyses_used': user['analyses_used'],
            'max_analyses': user['max_analyses']
        }
    
    def increment_usage(self) -> Tuple[bool, str]:
        """
        Increment analysis usage counter.
        
        Returns:
            Tuple of (allowed, message)
        """
        if not self.is_logged_in():
            # Guest user - 3 attempts max
            return False, "Guest limit reached. Please sign up for free account."
        
        user = self.get_current_user()
        
        if user['tier'] == 'free':
            if user['analyses_used'] >= user['max_analyses']:
                return False, "Free tier limit reached. Upgrade to Pro for unlimited analyses."
            
            user['analyses_used'] += 1
            self.save_users()
            remaining = user['max_analyses'] - user['analyses_used']
            if remaining <= 0:
                return True, f"Analyses used: {user['analyses_used']}/{user['max_analyses']}. Upgrade to Pro for more!"
            return True, f"Analyses used: {user['analyses_used']}/{user['max_analyses']} (Remaining: {remaining})"
        
        else:  # Pro tier
            user['analyses_used'] += 1
            self.save_users()
            return True, "Analysis completed. Unlimited analyses with Pro!"
    
    def upgrade_to_pro(self, email: str, payment_id: str) -> Tuple[bool, str]:
        """
        Upgrade user to Pro tier.
        
        Args:
            email: User email
            payment_id: Payment transaction ID
        
        Returns:
            Tuple of (success, message)
        """
        if email not in self.users:
            return False, "User not found."
        
        user = self.users[email]
        user['tier'] = 'pro'
        user['max_analyses'] = 999999  # Unlimited
        user['upgraded_at'] = datetime.now().isoformat()
        user['payment_id'] = payment_id
        
        self.save_users()
        return True, "Successfully upgraded to Pro! Unlimited analyses activated."
    
    def reset_guest_attempts(self):
        """Reset guest attempt counter (for demo purposes)."""
        # Guest data stored in memory, reset on app restart
        pass
