"""
Test Authentication System
Quick test to verify signup and login work correctly
"""

import sys
import logging
from pathlib import Path

# Setup path
sys.path.insert(0, str(Path(__file__).parent / "src"))

logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')

from core.auth import AuthenticationService

def test_authentication():
    """Test signup and login"""
    print("\n" + "="*60)
    print("TESTING AUTHENTICATION SYSTEM")
    print("="*60 + "\n")
    
    # Initialize auth service
    auth = AuthenticationService()
    
    # Test 1: Signup
    print("TEST 1: User Signup")
    print("-" * 40)
    username = "testuser123"
    password = "SecurePassword123"
    email = "test@example.com"
    
    success, msg = auth.signup(username, password, email)
    print(f"Signup Result: {success}")
    print(f"Message: {msg}")
    
    if success:
        print("✅ SIGNUP SUCCESSFUL\n")
    else:
        print("❌ SIGNUP FAILED\n")
        auth.close()
        return False
    
    # Test 2: Login with correct credentials
    print("TEST 2: Login with Correct Credentials")
    print("-" * 40)
    success, msg = auth.login(username, password)
    print(f"Login Result: {success}")
    print(f"Message: {msg}")
    print(f"Current User: {auth.get_current_user()}")
    print(f"Is Authenticated: {auth.is_authenticated()}")
    
    if success:
        print("✅ LOGIN SUCCESSFUL\n")
    else:
        print("❌ LOGIN FAILED\n")
        print("DEBUGGING INFO:")
        # Try to debug
        from database.models import UserManager
        um = UserManager()
        user = um.get_user(username)
        print(f"User found in DB: {user is not None}")
        if user:
            print(f"Username: {user['username']}")
            print(f"Email: {user['email']}")
        um.close()
        auth.close()
        return False
    
    # Test 3: Logout
    print("TEST 3: Logout")
    print("-" * 40)
    auth.logout()
    print(f"Current User after logout: {auth.get_current_user()}")
    print(f"Is Authenticated: {auth.is_authenticated()}")
    print("✅ LOGOUT SUCCESSFUL\n")
    
    # Test 4: Login again
    print("TEST 4: Login Again")
    print("-" * 40)
    success, msg = auth.login(username, password)
    print(f"Login Result: {success}")
    print(f"Message: {msg}")
    
    if success:
        print("✅ RE-LOGIN SUCCESSFUL\n")
    else:
        print("❌ RE-LOGIN FAILED\n")
        auth.close()
        return False
    
    # Test 5: Wrong password
    print("TEST 5: Login with Wrong Password")
    print("-" * 40)
    auth.logout()
    success, msg = auth.login(username, "WrongPassword")
    print(f"Login Result: {success}")
    print(f"Message: {msg}")
    
    if not success:
        print("✅ CORRECTLY REJECTED WRONG PASSWORD\n")
    else:
        print("❌ ERROR: ACCEPTED WRONG PASSWORD\n")
        auth.close()
        return False
    
    # Test 6: Nonexistent user
    print("TEST 6: Login with Nonexistent User")
    print("-" * 40)
    success, msg = auth.login("nonexistent_user", "AnyPassword")
    print(f"Login Result: {success}")
    print(f"Message: {msg}")
    
    if not success:
        print("✅ CORRECTLY REJECTED NONEXISTENT USER\n")
    else:
        print("❌ ERROR: ACCEPTED NONEXISTENT USER\n")
        auth.close()
        return False
    
    auth.close()
    
    # Summary
    print("="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60 + "\n")
    
    return True


if __name__ == "__main__":
    success = test_authentication()
    sys.exit(0 if success else 1)
