"""Input validation utilities"""
import re
from typing import Optional

def validate_email(email):
    """Check if email address is in valid format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone_number(phone):
    """Validate US phone number format"""
    # Remove common formatting characters
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Check if it's 10 digits
    if len(cleaned) != 10:
        return False
    
    # Check if all characters are digits
    return cleaned.isdigit()

def validate_credit_card(card_number):
    """Validate credit card number using Luhn algorithm"""
    # Remove spaces and dashes
    card_number = card_number.replace(' ', '').replace('-', '')
    
    # Check if all digits
    if not card_number.isdigit():
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

def validate_password_strength(password):
    """Check if password meets security requirements"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain a number"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain special character"
    
    return True, "Password is strong"

def sanitize_input(user_input):
    """Remove potentially dangerous characters from user input"""
    # Remove SQL injection attempts
    dangerous_patterns = ['--', ';', 'DROP', 'DELETE', 'INSERT', 'UPDATE']
    sanitized = user_input
    
    for pattern in dangerous_patterns:
        sanitized = sanitized.replace(pattern, '')
    
    # Remove HTML/JavaScript tags
    sanitized = re.sub(r'<[^>]*>', '', sanitized)
    
    return sanitized.strip()

def validate_url(url):
    """Check if URL is valid and safe"""
    pattern = r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$'
    return re.match(pattern, url) is not None

def validate_username(username):
    """Check if username meets requirements"""
    if len(username) < 3 or len(username) > 20:
        return False
    
    # Only alphanumeric and underscores
    return re.match(r'^[a-zA-Z0-9_]+$', username) is not None
