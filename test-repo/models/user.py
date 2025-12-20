from datetime import datetime
from typing import Optional, List

class User:
    def __init__(self, user_id: int, username: str, email: str):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.created_at = datetime.now()
        self.is_active = True
        self.roles: List[str] = []
    
    def deactivate_account(self):
        """Deactivate the user's account"""
        self.is_active = False
        print(f"Account {self.username} has been deactivated")
    
    def add_role(self, role: str):
        """Add a role to the user"""
        if role not in self.roles:
            self.roles.append(role)
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has a specific permission based on roles"""
        admin_permissions = ['read', 'write', 'delete', 'admin']
        moderator_permissions = ['read', 'write', 'moderate']
        
        if 'admin' in self.roles:
            return permission in admin_permissions
        elif 'moderator' in self.roles:
            return permission in moderator_permissions
        
        return permission == 'read'
    
    def update_email(self, new_email: str) -> bool:
        """Update the user's email address"""
        if '@' not in new_email:
            return False
        self.email = new_email
        return True

class UserProfile:
    def __init__(self, user: User):
        self.user = user
        self.bio: Optional[str] = None
        self.avatar_url: Optional[str] = None
        self.location: Optional[str] = None
    
    def set_biography(self, bio_text: str):
        """Set or update the user's biography"""
        self.bio = bio_text
    
    def get_display_name(self) -> str:
        """Get the user's display name"""
        return self.user.username
