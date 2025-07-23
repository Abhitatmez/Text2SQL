"""
Basic API tests for Text2SQL Assistant
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Text2SQL Assistant" in data["message"]


def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "version" in data


def test_sample_queries_endpoint():
    """Test the sample queries endpoint"""
    response = client.get("/api/v1/sample-queries")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data
    assert len(data["data"]) > 0


def test_database_info_endpoint():
    """Test the database info endpoint"""
    response = client.get("/api/v1/database-info")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_generate_sql_endpoint():
    """Test the generate SQL endpoint"""
    test_query = {
        "query": "Show all customers from Mumbai"
    }
    
    response = client.post("/api/v1/generate-sql", json=test_query)
    
    # Should work even without API key (will return appropriate error)
    assert response.status_code == 200
    data = response.json()
    assert "sql_query" in data


def test_execute_sql_endpoint_invalid():
    """Test execute SQL endpoint with invalid query"""
    test_query = {
        "sql_query": "DROP TABLE customers;"
    }
    
    response = client.post("/api/v1/execute-sql", json=test_query)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False


def test_query_endpoint():
    """Test the main query endpoint"""
    test_query = {
        "query": "Show all customers",
        "include_sql": True
    }
    
    response = client.post("/api/v1/query", json=test_query)
    assert response.status_code == 200
    data = response.json()
    assert "success" in data


def test_invalid_endpoint():
    """Test 404 for invalid endpoint"""
    response = client.get("/invalid-endpoint")
    assert response.status_code == 404


def test_validation_error():
    """Test validation error"""
    # Empty query should fail validation
    response = client.post("/api/v1/generate-sql", json={"query": ""})
    assert response.status_code == 422


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 