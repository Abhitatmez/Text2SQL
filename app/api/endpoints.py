"""
FastAPI endpoints for Text2SQL Assistant - Core Requirements Only
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    GenerateSQLRequest, GenerateSQLResponse,
    ExecuteSQLRequest, ExecuteSQLResponse,
    QueryRequest, QueryResponse
)
from app.services.text2sql_service import text2sql_service
from app.database.connection import db_manager

# Create API router
router = APIRouter()


@router.post("/generate-sql", response_model=GenerateSQLResponse)
async def generate_sql(request: GenerateSQLRequest) -> GenerateSQLResponse:
    """
    Convert natural language query to SQL
    
    Takes a natural language query and converts it to a valid SQL query
    using the configured LLM (Gemini API). The generated SQL is validated but not executed.
    """
    try:
        result = await text2sql_service.generate_sql_from_text(request.query)
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate SQL: {str(e)}"
        )


@router.post("/execute-sql", response_model=ExecuteSQLResponse)
async def execute_sql(request: ExecuteSQLRequest) -> ExecuteSQLResponse:
    """
    Execute SQL query safely
    
    Executes a SQL query against the database with safety validations.
    Only SELECT queries are allowed, and results are limited to prevent resource exhaustion.
    """
    try:
        result = await text2sql_service.execute_sql_query(request.sql_query)
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to execute SQL: {str(e)}"
        )


@router.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest) -> QueryResponse:
    """
    Complete Text-to-SQL Pipeline - Main Endpoint
    
    Takes a natural language query, converts it to SQL using AI, executes the query,
    and returns the results with comprehensive metadata.
    """
    try:
        result = await text2sql_service.process_natural_language_query(
            natural_query=request.query,
            include_sql_in_response=request.include_sql
        )
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process query: {str(e)}"
        )


# Debug endpoint to check database status
@router.get("/debug/database-status")
async def check_database_status():
    """Check if database tables exist and have data"""
    try:
        tables = await db_manager.get_table_names()
        status = {
            "database_file_exists": True,
            "tables_found": tables,
            "table_count": len(tables),
            "expected_tables": ["customers", "products", "orders", "order_items"]
        }
        
        # Check if expected tables exist
        expected = {"customers", "products", "orders", "order_items"}
        found = set(tables)
        status["missing_tables"] = list(expected - found)
        status["database_ready"] = len(status["missing_tables"]) == 0
        
        # Check data counts if tables exist
        if status["database_ready"]:
            try:
                customers = await db_manager.execute_query("SELECT COUNT(*) as count FROM customers")
                products = await db_manager.execute_query("SELECT COUNT(*) as count FROM products")
                orders = await db_manager.execute_query("SELECT COUNT(*) as count FROM orders")
                order_items = await db_manager.execute_query("SELECT COUNT(*) as count FROM order_items")
                
                status["data_counts"] = {
                    "customers": customers[0]["count"] if customers else 0,
                    "products": products[0]["count"] if products else 0,
                    "orders": orders[0]["count"] if orders else 0,
                    "order_items": order_items[0]["count"] if order_items else 0
                }
                
                # Check if we have sample data
                sample_customers = await db_manager.execute_query("SELECT * FROM customers LIMIT 3")
                status["sample_data"] = {
                    "customers": [dict(c) for c in sample_customers]
                }
                
            except Exception as e:
                status["data_error"] = str(e)
        
        return status
    except Exception as e:
        return {
            "database_file_exists": False,
            "error": str(e),
            "database_ready": False
        }


# Manual database initialization endpoint
@router.post("/debug/init-database")
async def initialize_database():
    """Manually initialize the database with schema and data"""
    try:
        success = db_manager.initialize_database()
        if success:
            tables = await db_manager.get_table_names()
            return {
                "success": True,
                "message": "Database initialized successfully",
                "tables_created": tables
            }
        else:
            return {
                "success": False,
                "message": "Database initialization failed"
            }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to initialize database: {str(e)}"
        ) 