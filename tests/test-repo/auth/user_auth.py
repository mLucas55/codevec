"""User authentication and authorization module"""
import hashlib
import jwt
from datetime import datetime, timedelta

class UserAuth:
    def __init__(self, secret_key):
        self.secret_key = secret_key
        self.failed_attempts = {}
    
    def hash_password(self, password, salt):
        """Hash a password with salt using SHA-256"""
        combined = password + salt
        return hashlib.sha256(combined.encode()).hexdigest()
    
    def verify_password(self, password, hashed_password, salt):
        """Verify if provided password matches the stored hash"""
        return self.hash_password(password, salt) == hashed_password
    
    def create_jwt_token(self, user_id, email, expires_in_hours=24):
        """Generate a JWT token for authenticated user"""
        payload = {
            'user_id': user_id,
            'email': email,
            'exp': datetime.utcnow() + timedelta(hours=expires_in_hours),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def validate_token(self, token):
        """Validate and decode a JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def check_login_attempts(self, email):
        """Check if user has exceeded maximum login attempts"""
        if email not in self.failed_attempts:
            return True
        
        attempts, last_attempt = self.failed_attempts[email]
        
        # Reset after 15 minutes
        if datetime.utcnow() - last_attempt > timedelta(minutes=15):
            del self.failed_attempts[email]
            return True
        
        return attempts < 5
    
    def record_failed_login(self, email):
        """Record a failed login attempt"""
        if email in self.failed_attempts:
            attempts, _ = self.failed_attempts[email]
            self.failed_attempts[email] = (attempts + 1, datetime.utcnow())
        else:
            self.failed_attempts[email] = (1, datetime.utcnow())
    
    def reset_login_attempts(self, email):
        """Clear failed login attempts after successful login"""
        if email in self.failed_attempts:
            del self.failed_attempts[email]
    
    def require_password_reset(self, last_password_change):
        """Check if user needs to reset password (90 days)"""
        if not last_password_change:
            return True
        
        days_since_change = (datetime.utcnow() - last_password_change).days
        return days_since_change > 90
