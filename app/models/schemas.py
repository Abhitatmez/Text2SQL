"""
Pydantic models for API request/response schemas
"""
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field, validator
from datetime import datetime


# Request Models
class GenerateSQLRequest(BaseModel):
    """Request model for /generate-sql endpoint"""
    query: str = Field(..., min_length=1, max_length=1000, description="Natural language query")
    
    @validator('query')
    def validate_query(cls, v):
        if not v.strip():
            raise ValueError('Query cannot be empty')
        return v.strip()


class ExecuteSQLRequest(BaseModel):
    """Request model for /execute-sql endpoint"""
    sql_query: str = Field(..., min_length=1, max_length=5000, description="SQL query to execute")
    
    @validator('sql_query')
    def validate_sql_query(cls, v):
        if not v.strip():
            raise ValueError('SQL query cannot be empty')
        # Basic SQL injection prevention
        dangerous_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE', 'TRUNCATE']
        query_upper = v.upper()
        for keyword in dangerous_keywords:
            if keyword in query_upper and not query_upper.strip().startswith('SELECT'):
                raise ValueError(f'Only SELECT queries are allowed')
        return v.strip()


class QueryRequest(BaseModel):
    """Request model for /query endpoint (combined)"""
    query: str = Field(..., min_length=1, max_length=1000, description="Natural language query")
    include_sql: bool = Field(False, description="Whether to include generated SQL in response")
    
    @validator('query')
    def validate_query(cls, v):
        if not v.strip():
            raise ValueError('Query cannot be empty')
        return v.strip()


# Response Models
class GenerateSQLResponse(BaseModel):
    """Response model for /generate-sql endpoint"""
    sql_query: str = Field(..., description="Generated SQL query")
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence score of generation")
    explanation: Optional[str] = Field(None, description="Explanation of the SQL query")
    estimated_rows: Optional[int] = Field(None, ge=0, description="Estimated number of result rows")


class ExecuteSQLResponse(BaseModel):
    """Response model for /execute-sql endpoint"""
    success: bool = Field(..., description="Whether query executed successfully")
    data: List[Dict[str, Any]] = Field(default=[], description="Query result data")
    row_count: int = Field(..., ge=0, description="Number of rows returned")
    execution_time_ms: Optional[float] = Field(None, ge=0, description="Query execution time in milliseconds")
    error_message: Optional[str] = Field(None, description="Error message if query failed")


class QueryResponse(BaseModel):
    """Response model for /query endpoint (combined)"""
    success: bool = Field(..., description="Whether the complete process succeeded")
    data: List[Dict[str, Any]] = Field(default=[], description="Final query result data")
    row_count: int = Field(..., ge=0, description="Number of rows returned")
    sql_query: Optional[str] = Field(None, description="Generated SQL query (if requested)")
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence score of SQL generation")
    explanation: Optional[str] = Field(None, description="Explanation of the query and results")
    execution_time_ms: Optional[float] = Field(None, ge=0, description="Total execution time in milliseconds")
    error_message: Optional[str] = Field(None, description="Error message if process failed")


# Database Schema Models (for context sharing)
class TableInfo(BaseModel):
    """Model for database table information"""
    table_name: str
    columns: List[Dict[str, str]]
    sample_data: Optional[List[Dict[str, Any]]] = None


class DatabaseSchema(BaseModel):
    """Model for complete database schema information"""
    tables: List[TableInfo]
    relationships: List[Dict[str, str]]


# Error Response Models
class ErrorResponse(BaseModel):
    """Standard error response model"""
    success: bool = False
    error_message: str
    error_code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class ValidationErrorResponse(BaseModel):
    """Validation error response model"""
    success: bool = False
    error_message: str = "Validation failed"
    validation_errors: List[Dict[str, Union[str, List[str]]]]


# Health Check Models
class HealthResponse(BaseModel):
    """Health check response model"""
    status: str = "healthy"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str
    database_status: str
    llm_status: str
    uptime_seconds: Optional[float] = None


# Analytics Models (for future enhancement)
class QueryAnalytics(BaseModel):
    """Model for query analytics and metrics"""
    total_queries: int = 0
    successful_queries: int = 0
    failed_queries: int = 0
    average_execution_time_ms: float = 0.0
    most_common_categories: List[str] = []
    popular_tables: List[str] = []


class APIUsageStats(BaseModel):
    """Model for API usage statistics"""
    endpoint_stats: Dict[str, int] = {}
    daily_requests: int = 0
    total_requests: int = 0
    error_rate: float = 0.0 