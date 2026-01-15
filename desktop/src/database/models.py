"""
Database Models for Skintelli Application
Handles User and Analysis data persistence
"""

import sqlite3
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
import hashlib

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages SQLite database operations"""
    
    def __init__(self, db_path: str = "./data/skintelli.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = None
        self._init_db()
    
    def _init_db(self):
        """Initialize database and create tables"""
        try:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row
            self._create_tables()
            logger.info(f"Database initialized at {self.db_path}")
        except sqlite3.Error as e:
            logger.error(f"Database initialization error: {e}")
            raise
    
    def _create_tables(self):
        """Create database tables"""
        cursor = self.connection.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL,
                email TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Analysis table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_username TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                input_image_path TEXT NOT NULL,
                heatmap_image_path TEXT,
                diagnosis TEXT,
                confidence REAL,
                explanation TEXT,
                FOREIGN KEY (user_username) REFERENCES users(username)
            )
        ''')
        
        self.connection.commit()
        logger.info("Database tables created successfully")
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _validate_username(self, username: str) -> tuple[bool, str]:
        """Validate username format"""
        if not username or len(username) < 3 or len(username) > 50:
            return False, "Username must be between 3 and 50 characters"
        return True, ""
    
    def _validate_password(self, password: str) -> tuple[bool, str]:
        """Validate password requirements"""
        if not password or len(password) < 8:
            return False, "Password must be at least 8 characters long"
        return True, ""


class UserManager(DatabaseManager):
    """Manage user operations"""
    
    def create_user(self, username: str, password: str, email: str = "") -> tuple[bool, str]:
        """
        Create a new user
        
        Returns:
            (success, message)
        """
        # Validate username
        valid, msg = self._validate_username(username)
        if not valid:
            return False, msg
        
        # Validate password
        valid, msg = self._validate_password(password)
        if not valid:
            return False, msg
        
        try:
            cursor = self.connection.cursor()
            password_hash = self._hash_password(password)
            
            cursor.execute('''
                INSERT INTO users (username, password_hash, email)
                VALUES (?, ?, ?)
            ''', (username, password_hash, email))
            
            self.connection.commit()
            logger.info(f"User created: {username}")
            return True, "User created successfully"
            
        except sqlite3.IntegrityError:
            logger.warning(f"Username already exists: {username}")
            return False, "Username already exists"
        except sqlite3.Error as e:
            logger.error(f"Error creating user: {e}")
            return False, f"Database error: {str(e)}"
    
    def authenticate_user(self, username: str, password: str) -> tuple[bool, str]:
        """
        Authenticate user with username and password
        
        Returns:
            (success, message)
        """
        try:
            cursor = self.connection.cursor()
            password_hash = self._hash_password(password)
            
            cursor.execute('''
                SELECT password_hash FROM users WHERE username = ?
            ''', (username,))
            
            row = cursor.fetchone()
            
            if row and row[0] == password_hash:
                logger.info(f"User authenticated: {username}")
                return True, "Authentication successful"
            else:
                logger.warning(f"Authentication failed for: {username}")
                return False, "Invalid username or password"
                
        except sqlite3.Error as e:
            logger.error(f"Error authenticating user: {e}")
            return False, f"Database error: {str(e)}"
    
    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user details"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            row = cursor.fetchone()
            
            if row:
                return dict(row)
            return None
            
        except sqlite3.Error as e:
            logger.error(f"Error fetching user: {e}")
            return None
    
    def user_exists(self, username: str) -> bool:
        """Check if user exists"""
        return self.get_user(username) is not None


class AnalysisManager(DatabaseManager):
    """Manage analysis operations"""
    
    def save_analysis(self,
                     user_username: str,
                     input_image_path: str,
                     diagnosis: str,
                     confidence: float = 0.0,
                     heatmap_image_path: Optional[str] = None,
                     explanation: str = "") -> tuple[bool, Optional[int]]:
        """
        Save analysis result to database
        
        Returns:
            (success, analysis_id)
        """
        try:
            cursor = self.connection.cursor()
            
            cursor.execute('''
                INSERT INTO analyses 
                (user_username, input_image_path, heatmap_image_path, diagnosis, confidence, explanation)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_username, input_image_path, heatmap_image_path, diagnosis, confidence, explanation))
            
            self.connection.commit()
            analysis_id = cursor.lastrowid
            
            logger.info(f"Analysis saved: {analysis_id} for user {user_username}")
            return True, analysis_id
            
        except sqlite3.Error as e:
            logger.error(f"Error saving analysis: {e}")
            return False, None
    
    def get_user_analyses(self, username: str) -> List[Dict[str, Any]]:
        """Get all analyses for a user"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT * FROM analyses WHERE user_username = ? ORDER BY timestamp DESC
            ''', (username,))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
            
        except sqlite3.Error as e:
            logger.error(f"Error fetching analyses: {e}")
            return []
    
    def get_analysis(self, analysis_id: int) -> Optional[Dict[str, Any]]:
        """Get specific analysis by ID"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM analyses WHERE id = ?', (analysis_id,))
            row = cursor.fetchone()
            
            if row:
                return dict(row)
            return None
            
        except sqlite3.Error as e:
            logger.error(f"Error fetching analysis: {e}")
            return None
    
    def update_analysis(self, analysis_id: int, **kwargs) -> bool:
        """Update analysis record"""
        try:
            allowed_fields = {'heatmap_image_path', 'diagnosis', 'confidence', 'explanation'}
            updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
            
            if not updates:
                return False
            
            cursor = self.connection.cursor()
            set_clause = ', '.join(f"{k} = ?" for k in updates.keys())
            values = list(updates.values()) + [analysis_id]
            
            cursor.execute(f'UPDATE analyses SET {set_clause} WHERE id = ?', values)
            self.connection.commit()
            
            logger.info(f"Analysis updated: {analysis_id}")
            return True
            
        except sqlite3.Error as e:
            logger.error(f"Error updating analysis: {e}")
            return False
    
    def delete_analysis(self, analysis_id: int) -> bool:
        """Delete analysis record"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('DELETE FROM analyses WHERE id = ?', (analysis_id,))
            self.connection.commit()
            
            logger.info(f"Analysis deleted: {analysis_id}")
            return True
            
        except sqlite3.Error as e:
            logger.error(f"Error deleting analysis: {e}")
            return False


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test database
    user_mgr = UserManager()
    
    # Create test user
    success, msg = user_mgr.create_user("testuser", "password123", "test@example.com")
    print(f"Create user: {success} - {msg}")
    
    # Authenticate user
    success, msg = user_mgr.authenticate_user("testuser", "password123")
    print(f"Authenticate: {success} - {msg}")
    
    # Save analysis
    analysis_mgr = AnalysisManager()
    success, analysis_id = analysis_mgr.save_analysis(
        "testuser",
        "./images/test.jpg",
        "Melanoma",
        0.92,
        "./images/test_heatmap.jpg",
        "The model detected irregular borders and dark coloration."
    )
    print(f"Save analysis: {success} - ID: {analysis_id}")
    
    # Get analyses
    analyses = analysis_mgr.get_user_analyses("testuser")
    print(f"User analyses: {len(analyses)} found")
    
    user_mgr.close()
