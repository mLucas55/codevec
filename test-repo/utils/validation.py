import re
from typing import Optional

def validate_email_format(email: str) -> bool:
    """Validate that an email address has the correct format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password_strength(password: str) -> tuple[bool, Optional[str]]:
    """Validate password strength and return result with error message"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    return True, None

def validate_phone_number(phone: str) -> bool:
    """Validate US phone number format"""
    pattern = r'^\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})$'
    return re.match(pattern, phone) is not None

def sanitize_user_input(user_input: str) -> str:
    """Sanitize user input to prevent SQL injection and XSS"""
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>\"\'%;()&+]', '', user_input)
    return sanitized.strip()

def validate_credit_card(card_number: str) -> bool:
    """Validate credit card number using Luhn algorithm"""
    # Remove spaces and dashes
    card_number = card_number.replace(' ', '').replace('-', '')
    
    if not card_number.isdigit() or len(card_number) < 13 or len(card_number) > 19:
        return False
    
    # Luhn algorithm
    total = 0
    reverse_digits = card_number[::-1]
    
    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    
    return total % 10 == 0
