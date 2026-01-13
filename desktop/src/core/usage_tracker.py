"""
Usage Tracker for Free Tier
Tracks guest user attempts and free tier analysis limit.
"""
from typing import Tuple


class GuestUsageTracker:
    """Tracks guest user attempts during current session."""
    
    def __init__(self, max_attempts: int = 3):
        self.max_attempts = max_attempts
        self.attempts_used = 0
    
    def get_remaining_attempts(self) -> int:
        """Get remaining guest attempts."""
        return max(0, self.max_attempts - self.attempts_used)
    
    def attempt_analysis(self) -> Tuple[bool, str]:
        """
        Use one guest attempt.
        
        Returns:
            Tuple of (allowed, message)
        """
        if self.attempts_used >= self.max_attempts:
            return False, "Guest limit (3 attempts) reached. Please sign up to continue."
        
        self.attempts_used += 1
        remaining = self.get_remaining_attempts()
        
        if remaining == 0:
            return True, f"Last guest attempt used. Sign up now for 15 free analyses!"
        
        return True, f"Guest attempt {self.attempts_used}/{self.max_attempts} used. (Remaining: {remaining})"
    
    def reset(self):
        """Reset attempts (for demo purposes)."""
        self.attempts_used = 0
    
    def is_limit_reached(self) -> bool:
        """Check if guest limit is reached."""
        return self.attempts_used >= self.max_attempts
