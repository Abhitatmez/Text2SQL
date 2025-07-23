"""
SQL Service for safe execution of SQL queries
"""
import time
import re
from typing import List, Dict, Any, Optional, Tuple
from app.database.connection import db_manager


class SQLService:
    """Service for safe SQL query execution with validation and monitoring"""
    
    def __init__(self):
        self.max_result_rows = 1000  # Prevent excessive memory usage
        self.query_timeout = 30  # seconds
        self.allowed_functions = {
            'SUM', 'COUNT', 'AVG', 'MAX', 'MIN', 'UPPER', 'LOWER', 
            'SUBSTR', 'LENGTH', 'ROUND', 'ABS', 'COALESCE', 'NULLIF',
            'DATE', 'DATETIME', 'STRFTIME', 'JULIANDAY'
        }
    
    async def execute_sql_query(self, sql_query: str) -> Tuple[bool, List[Dict[str, Any]], Optional[str], float]:
        """
        Execute SQL query safely with validation and monitoring
        
        Returns:
            Tuple of (success, data, error_message, execution_time_ms)
        """
        start_time = time.time()
        
        try:
            # Validate query safety
            is_safe, safety_error = self._validate_query_safety(sql_query)
            if not is_safe:
                return False, [], safety_error, 0.0
            
            # Execute the query
            results = await db_manager.execute_query(sql_query)
            
            # Check result size limits
            if len(results) > self.max_result_rows:
                limited_results = results[:self.max_result_rows]
                warning_message = f"Results limited to {self.max_result_rows} rows (total: {len(results)} rows)"
                execution_time = (time.time() - start_time) * 1000
                return True, limited_results, warning_message, execution_time
            
            execution_time = (time.time() - start_time) * 1000
            return True, results, None, execution_time
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            error_message = f"Query execution failed: {str(e)}"
            print(error_message)
            return False, [], error_message, execution_time
    
    def _validate_query_safety(self, sql_query: str) -> Tuple[bool, Optional[str]]:
        """Validate SQL query for safety and security"""
        
        # Remove comments and normalize whitespace
        cleaned_query = self._clean_sql_query(sql_query)
        
        if not cleaned_query:
            return False, "Empty or invalid SQL query"
        
        # Convert to uppercase for validation
        query_upper = cleaned_query.upper()
        
        # 1. Must be SELECT query only
        if not query_upper.strip().startswith('SELECT'):
            return False, "Only SELECT queries are allowed"
        
        # 2. Check for dangerous SQL operations
        dangerous_operations = [
            'INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE', 'ALTER', 
            'TRUNCATE', 'REPLACE', 'MERGE', 'GRANT', 'REVOKE',
            'EXEC', 'EXECUTE', 'PRAGMA', 'ATTACH', 'DETACH'
        ]
        
        for operation in dangerous_operations:
            # Use word boundaries to avoid false positives
            pattern = r'\b' + operation + r'\b'
            if re.search(pattern, query_upper):
                return False, f"Operation '{operation}' is not allowed"
        
        # 3. Check for suspicious patterns
        suspicious_patterns = [
            r';\s*(DROP|DELETE|UPDATE|INSERT)',  # Multiple statements
            r'--\s*\w',  # SQL injection comments
            r'/\*.*?\*/',  # Block comments (potential injection)
            r'\bUNION\b.*\bSELECT\b',  # Union-based injection attempts
            r'\bOR\b.*\b1\s*=\s*1\b',  # OR 1=1 injection
            r'\bAND\b.*\b1\s*=\s*0\b',  # AND 1=0 injection
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, query_upper, re.IGNORECASE | re.DOTALL):
                return False, "Query contains suspicious patterns"
        
        # 4. Validate function usage
        used_functions = re.findall(r'\b(\w+)\s*\(', query_upper)
        for func in used_functions:
            if func not in self.allowed_functions and func not in ['SELECT', 'FROM', 'WHERE', 'GROUP', 'ORDER', 'HAVING', 'LIMIT']:
                # Allow table names and column names
                if not self._is_table_or_column_reference(func):
                    return False, f"Function '{func}' is not allowed"
        
        # 5. Check query complexity (prevent infinite loops/excessive resource usage)
        if self._is_query_too_complex(cleaned_query):
            return False, "Query is too complex or potentially resource-intensive"
        
        return True, None
    
    def _clean_sql_query(self, sql_query: str) -> str:
        """Clean and normalize SQL query"""
        try:
            # Remove leading/trailing whitespace
            cleaned = sql_query.strip()
            
            # Remove SQL comments (-- style)
            cleaned = re.sub(r'--.*$', '', cleaned, flags=re.MULTILINE)
            
            # Remove block comments but be careful with /* */
            cleaned = re.sub(r'/\*.*?\*/', '', cleaned, flags=re.DOTALL)
            
            # Normalize whitespace
            cleaned = re.sub(r'\s+', ' ', cleaned)
            
            # Remove trailing semicolon for processing (will be added back if needed)
            cleaned = cleaned.rstrip(';').strip()
            
            return cleaned
            
        except Exception:
            return ""
    
    def _is_table_or_column_reference(self, identifier: str) -> bool:
        """Check if identifier is a likely table or column name"""
        # Known table names in our schema
        table_names = {'CUSTOMERS', 'PRODUCTS', 'ORDERS', 'ORDER_ITEMS'}
        
        # Common column patterns
        column_patterns = [
            r'.*_ID$', r'.*_NAME$', r'.*_DATE$', r'.*_TIME$', 
            r'.*_STATUS$', r'.*_TYPE$', r'.*_CODE$', r'.*_INR$'
        ]
        
        if identifier in table_names:
            return True
            
        for pattern in column_patterns:
            if re.match(pattern, identifier):
                return True
        
        return False
    
    def _is_query_too_complex(self, sql_query: str) -> bool:
        """Check if query is too complex"""
        query_upper = sql_query.upper()
        
        # Count subqueries
        subquery_count = query_upper.count('(SELECT')
        if subquery_count > 3:
            return True
        
        # Count JOINs (too many joins can be expensive)
        join_count = len(re.findall(r'\bJOIN\b', query_upper))
        if join_count > 5:
            return True
        
        # Check for potentially expensive operations
        expensive_patterns = [
            r'\bCROSS\s+JOIN\b',  # Cross joins can be expensive
            r'\bUNION\s+ALL\b.*\bUNION\s+ALL\b',  # Multiple unions
        ]
        
        for pattern in expensive_patterns:
            if re.search(pattern, query_upper):
                return True
        
        return False
    
    async def validate_sql_syntax(self, sql_query: str) -> Tuple[bool, Optional[str]]:
        """Validate SQL syntax without executing"""
        try:
            is_valid, error = await db_manager.validate_sql(sql_query)
            return is_valid, error
        except Exception as e:
            return False, str(e)
    
    async def get_query_plan(self, sql_query: str) -> Optional[List[Dict[str, Any]]]:
        """Get query execution plan for analysis"""
        try:
            plan_query = f"EXPLAIN QUERY PLAN {sql_query}"
            return await db_manager.execute_query(plan_query)
        except Exception as e:
            print(f"Failed to get query plan: {e}")
            return None
    
    def format_sql_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format SQL results for better presentation"""
        if not results:
            return []
        
        formatted_results = []
        for row in results:
            formatted_row = {}
            for key, value in row.items():
                # Format currency values
                if key.endswith('_inr') or key.endswith('_price') or 'amount' in key.lower():
                    if isinstance(value, (int, float)):
                        formatted_row[key] = value
                        formatted_row[f"{key}_formatted"] = f"₹{value:,.2f}"
                    else:
                        formatted_row[key] = value
                else:
                    formatted_row[key] = value
            
            formatted_results.append(formatted_row)
        
        return formatted_results
    
    def get_result_summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary statistics for query results"""
        if not results:
            return {"row_count": 0, "columns": [], "has_numeric_data": False}
        
        summary = {
            "row_count": len(results),
            "columns": list(results[0].keys()) if results else [],
            "has_numeric_data": False,
            "numeric_columns": [],
            "currency_columns": []
        }
        
        # Analyze column types
        if results:
            first_row = results[0]
            for key, value in first_row.items():
                if isinstance(value, (int, float)):
                    summary["has_numeric_data"] = True
                    summary["numeric_columns"].append(key)
                    
                if key.endswith('_inr') or 'amount' in key.lower() or 'price' in key.lower():
                    summary["currency_columns"].append(key)
        
        return summary


# Global SQL service instance
sql_service = SQLService() 