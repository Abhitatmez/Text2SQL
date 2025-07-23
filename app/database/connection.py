"""
Database connection and management for Text2SQL Assistant
"""
import aiosqlite
import sqlite3
from typing import Optional, Dict, List, Any
from contextlib import asynccontextmanager
from pathlib import Path
import os
from app.utils.config import get_settings


class DatabaseManager:
    """Database connection and query manager"""
    
    def __init__(self):
        self.settings = get_settings()
        self.db_path = self._get_db_path()
        self._ensure_db_directory()
    
    def _get_db_path(self) -> str:
        """Extract database file path from DATABASE_URL"""
        url = self.settings.DATABASE_URL
        if url.startswith("sqlite:///"):
            return url.replace("sqlite:///", "")
        return "text2sql_assistant.db"
    
    def _ensure_db_directory(self):
        """Ensure database directory exists"""
        db_dir = os.path.dirname(self.db_path)
        if db_dir:
            Path(db_dir).mkdir(parents=True, exist_ok=True)
    
    @asynccontextmanager
    async def get_connection(self):
        """Async context manager for database connections"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            yield db
    
    async def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """Execute a SELECT query and return results as list of dictionaries"""
        async with self.get_connection() as db:
            try:
                if params:
                    cursor = await db.execute(query, params)
                else:
                    cursor = await db.execute(query)
                
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]
            
            except Exception as e:
                raise Exception(f"Query execution failed: {str(e)}")
    
    async def execute_script(self, script: str) -> bool:
        """Execute a SQL script (multiple statements)"""
        async with self.get_connection() as db:
            try:
                await db.executescript(script)
                await db.commit()
                return True
            except Exception as e:
                print(f"Script execution failed: {str(e)}")
                return False
    
    def execute_sync_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """Synchronous query execution for initialization"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            try:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
            
            except Exception as e:
                raise Exception(f"Query execution failed: {str(e)}")
    
    def execute_sync_script(self, script: str) -> bool:
        """Synchronous script execution for initialization"""
        with sqlite3.connect(self.db_path) as conn:
            try:
                conn.executescript(script)
                conn.commit()
                return True
            except Exception as e:
                print(f"Script execution failed: {str(e)}")
                return False
    
    async def validate_sql(self, sql_query: str) -> tuple[bool, Optional[str]]:
        """Validate SQL query without executing it"""
        async with self.get_connection() as db:
            try:
                # Use EXPLAIN to validate query without executing
                await db.execute(f"EXPLAIN QUERY PLAN {sql_query}")
                return True, None
            except Exception as e:
                return False, str(e)
    
    async def get_table_info(self, table_name: str) -> List[Dict[str, Any]]:
        """Get column information for a table"""
        query = f"PRAGMA table_info({table_name})"
        return await self.execute_query(query)
    
    async def get_table_names(self) -> List[str]:
        """Get all table names in the database"""
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        rows = await self.execute_query(query)
        return [row['name'] for row in rows]
    
    def initialize_database(self) -> bool:
        """Initialize database with schema and seed data"""
        try:
            # Check if database already has data
            try:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT COUNT(*) FROM customers")
                    customer_count = cursor.fetchone()[0]
                    if customer_count > 0:
                        print(f"Database already has {customer_count} customers. Skipping initialization.")
                        return True
            except:
                # Table doesn't exist, proceed with initialization
                pass
            
            # Read and execute schema
            schema_path = Path(__file__).parent / "schema.sql"
            print(f"Looking for schema at: {schema_path}")
            
            if schema_path.exists():
                print("Schema file found, reading...")
                with open(schema_path, 'r') as f:
                    schema_script = f.read()
                print(f"Schema script length: {len(schema_script)} characters")
                
                if not self.execute_sync_script(schema_script):
                    print("Schema execution failed!")
                    return False
                print("Schema executed successfully!")
            else:
                print("Schema file not found!")
                return False
            
            # Read and execute seed data
            seed_path = Path(__file__).parent / "seed_data.sql"
            print(f"Looking for seed data at: {seed_path}")
            
            if seed_path.exists():
                print("Seed data file found, reading...")
                with open(seed_path, 'r') as f:
                    seed_script = f.read()
                print(f"Seed script length: {len(seed_script)} characters")
                
                if not self.execute_sync_script(seed_script):
                    print("Seed data execution failed!")
                    return False
                print("Seed data executed successfully!")
                
                # Verify data was inserted
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT COUNT(*) FROM customers")
                    customer_count = cursor.fetchone()[0]
                    print(f"✅ Database now has {customer_count} customers")
                    
                    cursor.execute("SELECT COUNT(*) FROM products")
                    product_count = cursor.fetchone()[0]
                    print(f"✅ Database now has {product_count} products")
                    
                    cursor.execute("SELECT COUNT(*) FROM orders")
                    order_count = cursor.fetchone()[0]
                    print(f"✅ Database now has {order_count} orders")
            else:
                print("Seed data file not found!")
            
            print("Database initialized successfully!")
            return True
            
        except Exception as e:
            print(f"Database initialization failed: {str(e)}")
            return False


# Global database instance
db_manager = DatabaseManager() 