"""
Text2SQL Service - Main orchestrator for natural language to SQL conversion and execution
"""
import time
from typing import Dict, Any, Optional, Tuple, List
from app.services.llm_service import llm_service
from app.services.sql_service import sql_service
from app.models.schemas import (
    GenerateSQLResponse, ExecuteSQLResponse, QueryResponse
)


class Text2SQLService:
    """Main service that orchestrates text-to-SQL conversion and execution"""
    
    def __init__(self):
        self.llm = llm_service
        self.sql = sql_service
        self.query_history = []  # Store recent queries for analytics
        self.max_history = 100
    
    async def generate_sql_from_text(self, natural_query: str) -> GenerateSQLResponse:
        """
        Generate SQL query from natural language text
        
        Args:
            natural_query: Natural language query string
            
        Returns:
            GenerateSQLResponse with generated SQL and metadata
        """
        try:
            # Check if LLM service is available
            if not self.llm.is_available():
                return GenerateSQLResponse(
                    sql_query="",
                    confidence=0.0,
                    explanation="LLM service is not available. Please check configuration.",
                    estimated_rows=0
                )
            
            # Generate SQL using LLM service
            sql_query, explanation, confidence = await self.llm.generate_sql(natural_query)
            
            if not sql_query:
                return GenerateSQLResponse(
                    sql_query="",
                    confidence=0.0,
                    explanation=explanation or "Failed to generate SQL query",
                    estimated_rows=0
                )
            
            # Estimate result rows (simple heuristic)
            estimated_rows = self._estimate_result_rows(sql_query)
            
            # Store in history for analytics
            self._add_to_history({
                "type": "generate_sql",
                "natural_query": natural_query,
                "sql_query": sql_query,
                "confidence": confidence,
                "timestamp": time.time()
            })
            
            return GenerateSQLResponse(
                sql_query=sql_query,
                confidence=confidence,
                explanation=explanation,
                estimated_rows=estimated_rows
            )
            
        except Exception as e:
            return GenerateSQLResponse(
                sql_query="",
                confidence=0.0,
                explanation=f"Error generating SQL: {str(e)}",
                estimated_rows=0
            )
    
    async def execute_sql_query(self, sql_query: str) -> ExecuteSQLResponse:
        """
        Execute SQL query safely and return results
        
        Args:
            sql_query: SQL query string to execute
            
        Returns:
            ExecuteSQLResponse with query results and metadata
        """
        try:
            # Execute SQL query
            success, data, error_message, execution_time = await self.sql.execute_sql_query(sql_query)
            
            if not success:
                response = ExecuteSQLResponse(
                    success=False,
                    data=[],
                    row_count=0,
                    execution_time_ms=execution_time,
                    error_message=error_message
                )
            else:
                # Format results for better presentation
                formatted_data = self.sql.format_sql_results(data)
                
                response = ExecuteSQLResponse(
                    success=True,
                    data=formatted_data,
                    row_count=len(data),
                    execution_time_ms=execution_time,
                    error_message=error_message  # May contain warnings
                )
            
            # Store in history
            self._add_to_history({
                "type": "execute_sql",
                "sql_query": sql_query,
                "success": success,
                "row_count": len(data) if success else 0,
                "execution_time_ms": execution_time,
                "timestamp": time.time()
            })
            
            return response
            
        except Exception as e:
            return ExecuteSQLResponse(
                success=False,
                data=[],
                row_count=0,
                execution_time_ms=0.0,
                error_message=f"Error executing SQL: {str(e)}"
            )
    
    async def process_natural_language_query(
        self, 
        natural_query: str, 
        include_sql_in_response: bool = False
    ) -> QueryResponse:
        """
        Complete pipeline: Convert natural language to SQL and execute
        
        Args:
            natural_query: Natural language query string
            include_sql_in_response: Whether to include generated SQL in response
            
        Returns:
            QueryResponse with final results and metadata
        """
        start_time = time.time()
        
        try:
            # Step 1: Generate SQL from natural language
            sql_generation_result = await self.generate_sql_from_text(natural_query)
            
            if not sql_generation_result.sql_query:
                return QueryResponse(
                    success=False,
                    data=[],
                    row_count=0,
                    sql_query=sql_generation_result.sql_query if include_sql_in_response else None,
                    confidence=sql_generation_result.confidence,
                    explanation=sql_generation_result.explanation,
                    execution_time_ms=(time.time() - start_time) * 1000,
                    error_message="Failed to generate SQL query"
                )
            
            # Step 2: Execute the generated SQL
            execution_result = await self.execute_sql_query(sql_generation_result.sql_query)
            
            # Step 3: Prepare final response
            total_time = (time.time() - start_time) * 1000
            
            # Generate comprehensive explanation
            final_explanation = self._generate_comprehensive_explanation(
                natural_query, 
                sql_generation_result.sql_query,
                execution_result.data,
                sql_generation_result.explanation
            )
            
            response = QueryResponse(
                success=execution_result.success,
                data=execution_result.data,
                row_count=execution_result.row_count,
                sql_query=sql_generation_result.sql_query if include_sql_in_response else None,
                confidence=sql_generation_result.confidence,
                explanation=final_explanation,
                execution_time_ms=total_time,
                error_message=execution_result.error_message
            )
            
            # Store complete pipeline result in history
            self._add_to_history({
                "type": "complete_query",
                "natural_query": natural_query,
                "sql_query": sql_generation_result.sql_query,
                "success": execution_result.success,
                "row_count": execution_result.row_count,
                "confidence": sql_generation_result.confidence,
                "total_time_ms": total_time,
                "timestamp": time.time()
            })
            
            return response
            
        except Exception as e:
            total_time = (time.time() - start_time) * 1000
            return QueryResponse(
                success=False,
                data=[],
                row_count=0,
                sql_query=None,
                confidence=0.0,
                explanation=f"Error processing query: {str(e)}",
                execution_time_ms=total_time,
                error_message=str(e)
            )
    
    def _estimate_result_rows(self, sql_query: str) -> int:
        """Estimate number of rows the query might return (simple heuristic)"""
        query_upper = sql_query.upper()
        
        # Base estimation
        if 'LIMIT' in query_upper:
            # Extract LIMIT value
            import re
            limit_match = re.search(r'LIMIT\s+(\d+)', query_upper)
            if limit_match:
                return min(int(limit_match.group(1)), 100)
        
        # Heuristic based on query type
        if 'GROUP BY' in query_upper:
            return 20  # Aggregated results usually have fewer rows
        elif 'JOIN' in query_upper:
            return 50  # Joined results can vary
        elif 'COUNT' in query_upper or 'SUM' in query_upper:
            return 1   # Aggregate functions typically return single values
        else:
            return 25  # Default estimate
    
    def _generate_comprehensive_explanation(
        self, 
        natural_query: str, 
        sql_query: str, 
        results: List[Dict[str, Any]], 
        base_explanation: Optional[str]
    ) -> str:
        """Generate comprehensive explanation including results summary"""
        
        explanation_parts = []
        
        # Add base explanation
        if base_explanation:
            explanation_parts.append(base_explanation)
        else:
            explanation_parts.append(f"Processed query: '{natural_query}'")
        
        # Add results summary
        if results:
            row_count = len(results)
            if row_count == 1:
                explanation_parts.append("Returned 1 result row.")
            else:
                explanation_parts.append(f"Returned {row_count} result rows.")
            
            # Analyze result content
            if results:
                first_row = results[0]
                columns = list(first_row.keys())
                explanation_parts.append(f"Result columns: {', '.join(columns[:5])}" + 
                                       ("..." if len(columns) > 5 else ""))
                
                # Mention currency columns
                currency_cols = [col for col in columns if 'inr' in col.lower() or 'amount' in col.lower()]
                if currency_cols:
                    explanation_parts.append("Results include monetary values in Indian Rupees (INR).")
        else:
            explanation_parts.append("No results found matching the criteria.")
        
        return " ".join(explanation_parts)
    
    def _add_to_history(self, entry: Dict[str, Any]):
        """Add entry to query history for analytics"""
        try:
            self.query_history.append(entry)
            
            # Keep only recent entries
            if len(self.query_history) > self.max_history:
                self.query_history = self.query_history[-self.max_history:]
                
        except Exception as e:
            print(f"Error adding to history: {e}")
    
    def get_query_analytics(self) -> Dict[str, Any]:
        """Get analytics from query history"""
        if not self.query_history:
            return {"total_queries": 0}
        
        total_queries = len(self.query_history)
        successful_queries = sum(1 for entry in self.query_history 
                               if entry.get("success", True))
        failed_queries = total_queries - successful_queries
        
        # Calculate average execution time
        execution_times = [entry.get("total_time_ms", 0) 
                          for entry in self.query_history 
                          if "total_time_ms" in entry]
        avg_execution_time = sum(execution_times) / len(execution_times) if execution_times else 0
        
        # Most common query patterns
        complete_queries = [entry for entry in self.query_history if entry.get("type") == "complete_query"]
        
        return {
            "total_queries": total_queries,
            "successful_queries": successful_queries,
            "failed_queries": failed_queries,
            "success_rate": successful_queries / total_queries if total_queries > 0 else 0,
            "average_execution_time_ms": avg_execution_time,
            "recent_activity": len([entry for entry in self.query_history 
                                  if time.time() - entry.get("timestamp", 0) < 3600])  # Last hour
        }
    
    async def get_database_info(self) -> Dict[str, Any]:
        """Get database schema information"""
        try:
            from app.database.connection import db_manager
            
            table_names = await db_manager.get_table_names()
            table_info = {}
            
            for table in table_names:
                columns = await db_manager.get_table_info(table)
                table_info[table] = {
                    "columns": [{"name": col["name"], "type": col["type"]} for col in columns],
                    "column_count": len(columns)
                }
            
            return {
                "tables": table_info,
                "table_count": len(table_names),
                "total_columns": sum(info["column_count"] for info in table_info.values())
            }
            
        except Exception as e:
            return {"error": f"Failed to get database info: {str(e)}"}


# Global Text2SQL service instance
text2sql_service = Text2SQLService() 