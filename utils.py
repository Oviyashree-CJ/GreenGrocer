import re


def validate_password(password):
    """
    Validate password according to requirements:
    - Minimum 4 characters
    - Exactly 2 numbers
    - No special characters
    """
    if len(password) < 4:
        return False
    
    # Count digits
    digit_count = sum(1 for char in password if char.isdigit())
    if digit_count != 2:
        return False
    
    # Check for special characters (anything that's not alphanumeric)
    if not password.isalnum():
        return False
    
    return True