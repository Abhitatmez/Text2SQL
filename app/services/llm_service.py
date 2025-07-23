"""
LLM Service for Text-to-SQL conversion using Gemini API
"""
import google.generativeai as genai
from typing import Optional, Tuple, Dict, Any
import json
import re
import time
from app.utils.config import get_settings
from app.database.connection import db_manager


class LLMService:
    """Service for integrating with Large Language Models for text-to-SQL conversion"""
    
    def __init__(self):
        self.settings = get_settings()
        self.model = None
        self._initialize_llm()
        self.schema_context = ""
        self._load_schema_context()
    
    def _initialize_llm(self):
        """Initialize the LLM (Gemini) with API key"""
        if self.settings.GEMINI_API_KEY:
            try:
                genai.configure(api_key=self.settings.GEMINI_API_KEY)
                
                # Try different model names in order of preference
                model_names = [
                    "gemini-1.5-flash",
                    "gemini-1.5-pro", 
                    "gemini-pro",
                    "models/gemini-1.5-flash",
                    "models/gemini-pro"
                ]
                
                for model_name in model_names:
                    try:
                        self.model = genai.GenerativeModel(model_name)
                        print(f"Gemini API initialized successfully with model: {model_name}")
                        return
                    except Exception as model_error:
                        print(f"Failed to initialize model {model_name}: {model_error}")
                        continue
                
                # If all models fail, set to None
                print("Failed to initialize any Gemini model")
                self.model = None
                
            except Exception as e:
                print(f"Failed to initialize Gemini API: {e}")
                self.model = None
        else:
            print("GEMINI_API_KEY not found. LLM functionality will be limited.")
    
    def _load_schema_context(self):
        """Load database schema context for prompt engineering"""
        try:
            # Get table information
            tables_info = []
            table_names = ['customers', 'products', 'orders', 'order_items']
            
            for table_name in table_names:
                try:
                    columns_info = db_manager.execute_sync_query(f"PRAGMA table_info({table_name})")
                    if columns_info:
                        columns = [f"{col['name']} ({col['type']})" for col in columns_info]
                        tables_info.append(f"Table: {table_name}\nColumns: {', '.join(columns)}")
                except:
                    continue
            
            # Create comprehensive schema context
            self.schema_context = f"""
DATABASE SCHEMA:
=================

{chr(10).join(tables_info)}

TABLE RELATIONSHIPS:
===================
- customers.customer_id -> orders.customer_id (One-to-Many)
- orders.order_id -> order_items.order_id (One-to-Many)  
- products.product_id -> order_items.product_id (One-to-Many)

KEY BUSINESS RULES:
==================
- All prices are in Indian Rupees (INR)
- Order status: pending, processing, shipped, delivered, cancelled
- Payment methods: credit_card, debit_card, upi, wallet, cod
- Payment status: pending, completed, failed, refunded
- Product categories include: Electronics, Clothing, Books, Home & Kitchen, Health & Fitness, Beauty & Personal Care, Toys & Games
- Customers are primarily from Indian cities
"""
        except Exception as e:
            print(f"Failed to load schema context: {e}")
            self.schema_context = "Schema context not available"
    
    def _create_text_to_sql_prompt(self, natural_query: str) -> str:
        """Create a comprehensive prompt for text-to-SQL conversion"""
        
        prompt = f"""
You are an expert SQL query generator for an e-commerce database. Your task is to convert natural language queries into valid SQL SELECT statements.

{self.schema_context}

IMPORTANT RULES:
===============
1. ONLY generate SELECT queries - no INSERT, UPDATE, DELETE, or DDL operations
2. Use proper JOIN syntax when multiple tables are involved
3. Always use table aliases for better readability
4. Include appropriate WHERE clauses for filtering
5. Use aggregate functions (SUM, COUNT, AVG, MAX, MIN) when appropriate
6. Format dates properly (YYYY-MM-DD for DATE, YYYY-MM-DD HH:MM:SS for DATETIME)
7. Use LIKE operator with wildcards for text searches
8. Include ORDER BY for better result presentation
9. Limit results with LIMIT when appropriate to avoid excessive output
10. All monetary values are in INR (Indian Rupees)

EXAMPLE QUERIES AND THEIR SQL:
==============================

Natural: "Show all customers from Mumbai"
SQL: SELECT customer_id, first_name, last_name, email, phone FROM customers WHERE city = 'Mumbai';

Natural: "What are the top 5 most expensive products?"
SQL: SELECT product_id, product_name, brand, price_inr, category FROM products ORDER BY price_inr DESC LIMIT 5;

Natural: "Show all orders from the last 30 days with customer details"
SQL: SELECT o.order_id, o.order_date, o.total_amount_inr, c.first_name, c.last_name, c.city 
     FROM orders o 
     JOIN customers c ON o.customer_id = c.customer_id 
     WHERE o.order_date >= datetime('now', '-30 days') 
     ORDER BY o.order_date DESC;

Natural: "Which products have never been ordered?"
SQL: SELECT p.product_id, p.product_name, p.brand, p.category, p.price_inr
     FROM products p
     LEFT JOIN order_items oi ON p.product_id = oi.product_id
     WHERE oi.product_id IS NULL;

Natural: "Show total sales by category"
SQL: SELECT p.category, COUNT(oi.order_item_id) as total_orders, SUM(oi.total_price_inr) as total_sales_inr
     FROM products p
     JOIN order_items oi ON p.product_id = oi.product_id
     JOIN orders o ON oi.order_id = o.order_id
     WHERE o.order_status = 'delivered'
     GROUP BY p.category
     ORDER BY total_sales_inr DESC;

Natural: "Find customers who spent more than 50000 INR"
SQL: SELECT c.customer_id, c.first_name, c.last_name, c.email, c.city, SUM(o.total_amount_inr) as total_spent_inr
     FROM customers c
     JOIN orders o ON c.customer_id = o.customer_id
     WHERE o.payment_status = 'completed'
     GROUP BY c.customer_id, c.first_name, c.last_name, c.email, c.city
     HAVING SUM(o.total_amount_inr) > 50000
     ORDER BY total_spent_inr DESC;

NOW CONVERT THIS NATURAL LANGUAGE QUERY TO SQL:
===============================================

Natural Query: "{natural_query}"

Generate ONLY the SQL query without any explanation, comments, or formatting. The query should be a single line that can be executed directly.

SQL:"""
        
        return prompt
    
    async def generate_sql(self, natural_query: str) -> Tuple[Optional[str], Optional[str], Optional[float]]:
        """
        Generate SQL query from natural language
        
        Returns:
            Tuple of (sql_query, explanation, confidence_score)
        """
        if not self.model:
            return None, "LLM not available. Please check GEMINI_API_KEY configuration.", 0.0
        
        try:
            start_time = time.time()
            
            # Create prompt with schema context
            prompt = self._create_text_to_sql_prompt(natural_query)
            
            # Generate SQL using Gemini
            response = self.model.generate_content(prompt)
            
            if not response.text:
                return None, "Failed to generate response from LLM", 0.0
            
            # Extract SQL query from response
            sql_query = self._extract_sql_from_response(response.text)
            
            if not sql_query:
                return None, "Could not extract valid SQL from LLM response", 0.0
            
            # Validate the generated SQL
            is_valid, validation_error = await db_manager.validate_sql(sql_query)
            
            if not is_valid:
                # Return the generated SQL even if invalid, so user can see what was generated
                explanation = f"Generated SQL is invalid: {validation_error}. Generated SQL was: {sql_query}"
                return sql_query, explanation, 0.1  # Low confidence since invalid
            
            # Calculate confidence based on response quality
            confidence = self._calculate_confidence(sql_query, natural_query)
            
            # Generate explanation
            explanation = self._generate_explanation(sql_query, natural_query)
            
            generation_time = time.time() - start_time
            print(f"SQL generated in {generation_time:.2f} seconds")
            
            return sql_query, explanation, confidence
            
        except Exception as e:
            print(f"Error generating SQL: {str(e)}")
            return None, f"Error during SQL generation: {str(e)}", 0.0
    
    def _extract_sql_from_response(self, response_text: str) -> Optional[str]:
        """Extract SQL query from LLM response"""
        try:
            # Clean up the response
            cleaned_response = response_text.strip()
            
            # Remove markdown code blocks if present
            if "```sql" in cleaned_response.lower():
                match = re.search(r'```sql\s*(.*?)\s*```', cleaned_response, re.IGNORECASE | re.DOTALL)
                if match:
                    cleaned_response = match.group(1).strip()
            elif "```" in cleaned_response:
                match = re.search(r'```\s*(.*?)\s*```', cleaned_response, re.DOTALL)
                if match:
                    cleaned_response = match.group(1).strip()
            
            # Remove "SQL:" prefix if present
            if cleaned_response.lower().startswith('sql:'):
                cleaned_response = cleaned_response[4:].strip()
            
            # Remove any trailing semicolon and whitespace
            cleaned_response = cleaned_response.rstrip(';').strip()
            
            # Basic validation - must start with SELECT (case insensitive)
            if not cleaned_response.upper().startswith('SELECT'):
                return None
            
            # Add semicolon if not present
            if not cleaned_response.endswith(';'):
                cleaned_response += ';'
                
            return cleaned_response
            
        except Exception as e:
            print(f"Error extracting SQL: {e}")
            return None
    
    def _calculate_confidence(self, sql_query: str, natural_query: str) -> float:
        """Calculate confidence score for generated SQL"""
        try:
            confidence = 0.7  # Base confidence
            
            # Increase confidence for specific patterns
            if 'JOIN' in sql_query.upper():
                confidence += 0.1
            if 'WHERE' in sql_query.upper():
                confidence += 0.1
            if any(agg in sql_query.upper() for agg in ['SUM', 'COUNT', 'AVG', 'MAX', 'MIN']):
                confidence += 0.05
            if 'ORDER BY' in sql_query.upper():
                confidence += 0.05
            
            # Check for common keywords in natural query
            natural_lower = natural_query.lower()
            if any(word in natural_lower for word in ['total', 'sum', 'count', 'average']):
                confidence += 0.05
            if any(word in natural_lower for word in ['top', 'best', 'highest', 'lowest']):
                confidence += 0.05
                
            return min(confidence, 1.0)
            
        except:
            return 0.7
    
    def _generate_explanation(self, sql_query: str, natural_query: str) -> str:
        """Generate human-readable explanation of the SQL query"""
        try:
            explanation_parts = []
            
            # Analyze query structure
            sql_upper = sql_query.upper()
            
            if 'JOIN' in sql_upper:
                explanation_parts.append("This query combines data from multiple tables")
            
            if 'WHERE' in sql_upper:
                explanation_parts.append("includes filtering conditions")
                
            if 'GROUP BY' in sql_upper:
                explanation_parts.append("groups results by specific columns")
                
            if 'ORDER BY' in sql_upper:
                explanation_parts.append("sorts the results")
                
            if any(agg in sql_upper for agg in ['SUM', 'COUNT', 'AVG', 'MAX', 'MIN']):
                explanation_parts.append("calculates aggregate values")
            
            if 'LIMIT' in sql_upper:
                explanation_parts.append("limits the number of results returned")
            
            base_explanation = f"This SQL query retrieves data from the e-commerce database to answer: '{natural_query}'"
            
            if explanation_parts:
                base_explanation += " and " + ", ".join(explanation_parts) + "."
            
            return base_explanation
            
        except:
            return f"SQL query generated to answer: '{natural_query}'"
    
    def is_available(self) -> bool:
        """Check if LLM service is available"""
        return self.model is not None
    
    def list_available_models(self):
        """List available Gemini models for debugging"""
        try:
            if self.settings.GEMINI_API_KEY:
                genai.configure(api_key=self.settings.GEMINI_API_KEY)
                models = genai.list_models()
                print("Available Gemini models:")
                for model in models:
                    if 'generateContent' in model.supported_generation_methods:
                        print(f"  - {model.name}")
                return models
        except Exception as e:
            print(f"Error listing models: {e}")
            return None


# Global LLM service instance
llm_service = LLMService() 