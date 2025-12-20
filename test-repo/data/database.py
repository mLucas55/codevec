import sqlite3
from typing import List, Dict, Optional

class DatabaseConnection:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = None
    
    def connect(self):
        """Establish connection to the database"""
        self.connection = sqlite3.connect(self.db_path)
        return self.connection
    
    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None

def query_users_by_email(email: str) -> Optional[Dict]:
    """Query the database to find a user by their email address"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()
    return result

def insert_new_user(username: str, email: str, password_hash: str) -> int:
    """Insert a new user into the database and return the user ID"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
        (username, email, password_hash)
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id

def batch_update_users(user_updates: List[Dict]) -> int:
    """Update multiple users in a single transaction"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    updated_count = 0
    
    for update in user_updates:
        cursor.execute(
            "UPDATE users SET email = ?, username = ? WHERE id = ?",
            (update['email'], update['username'], update['id'])
        )
        updated_count += cursor.rowcount
    
    conn.commit()
    conn.close()
    return updated_count
