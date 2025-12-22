"""Database connection and query utilities"""
import sqlite3
from typing import List, Dict, Any, Optional

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None
    
    def connect(self):
        """Establish connection to SQLite database"""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def execute_query(self, query, params=None):
        """Execute a SELECT query and return results"""
        cursor = self.connection.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def execute_update(self, query, params=None):
        """Execute INSERT, UPDATE, or DELETE query"""
        cursor = self.connection.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        self.connection.commit()
        return cursor.rowcount
    
    def insert_record(self, table, data):
        """Insert a new record into table"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        cursor = self.connection.cursor()
        cursor.execute(query, list(data.values()))
        self.connection.commit()
        
        return cursor.lastrowid
    
    def update_record(self, table, record_id, data):
        """Update existing record by ID"""
        set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE id = ?"
        
        params = list(data.values()) + [record_id]
        return self.execute_update(query, params)
    
    def delete_record(self, table, record_id):
        """Delete record by ID"""
        query = f"DELETE FROM {table} WHERE id = ?"
        return self.execute_update(query, [record_id])
    
    def find_by_id(self, table, record_id):
        """Find a single record by ID"""
        query = f"SELECT * FROM {table} WHERE id = ?"
        results = self.execute_query(query, [record_id])
        return results[0] if results else None
    
    def find_all(self, table, where_clause=None, params=None):
        """Find all records matching criteria"""
        query = f"SELECT * FROM {table}"
        
        if where_clause:
            query += f" WHERE {where_clause}"
        
        return self.execute_query(query, params)
    
    def batch_insert(self, table, records):
        """Insert multiple records efficiently"""
        if not records:
            return 0
        
        columns = ', '.join(records[0].keys())
        placeholders = ', '.join(['?' for _ in records[0]])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        cursor = self.connection.cursor()
        cursor.executemany(query, [list(record.values()) for record in records])
        self.connection.commit()
        
        return cursor.rowcount
    
    def create_table(self, table_name, schema):
        """Create a new table with given schema"""
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})"
        self.execute_update(query)
