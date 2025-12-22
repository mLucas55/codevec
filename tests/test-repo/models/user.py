"""User model and related functions"""
from datetime import datetime
from typing import Optional, List

class User:
    def __init__(self, user_id, email, username):
        self.id = user_id
        self.email = email
        self.username = username
        self.created_at = datetime.utcnow()
        self.last_login = None
        self.is_active = True
        self.roles = []
        self.profile = {}
    
    def update_profile(self, **kwargs):
        """Update user profile information"""
        allowed_fields = ['first_name', 'last_name', 'phone', 'address', 'bio']
        
        for key, value in kwargs.items():
            if key in allowed_fields:
                self.profile[key] = value
    
    def add_role(self, role):
        """Add a role to user"""
        if role not in self.roles:
            self.roles.append(role)
    
    def remove_role(self, role):
        """Remove a role from user"""
        if role in self.roles:
            self.roles.remove(role)
    
    def has_permission(self, permission):
        """Check if user has specific permission"""
        role_permissions = {
            'admin': ['read', 'write', 'delete', 'manage_users'],
            'editor': ['read', 'write'],
            'viewer': ['read']
        }
        
        for role in self.roles:
            if permission in role_permissions.get(role, []):
                return True
        
        return False
    
    def deactivate_account(self):
        """Deactivate user account"""
        self.is_active = False
    
    def reactivate_account(self):
        """Reactivate user account"""
        self.is_active = True
    
    def update_last_login(self):
        """Record user's last login time"""
        self.last_login = datetime.utcnow()
    
    def get_full_name(self):
        """Get user's full name from profile"""
        first_name = self.profile.get('first_name', '')
        last_name = self.profile.get('last_name', '')
        return f"{first_name} {last_name}".strip()
    
    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active,
            'roles': self.roles,
            'profile': self.profile
        }

def find_users_by_role(users, role):
    """Filter users by role"""
    return [user for user in users if role in user.roles]

def get_active_users(users):
    """Get all active users"""
    return [user for user in users if user.is_active]

def search_users_by_email(users, email_query):
    """Search users by email pattern"""
    email_query = email_query.lower()
    return [user for user in users if email_query in user.email.lower()]
