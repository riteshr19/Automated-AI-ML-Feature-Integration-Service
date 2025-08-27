import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert data["service"] == "AI/ML Feature Integration Service"
    assert "version" in data
    assert "endpoints" in data

def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

def test_text_analysis_endpoint():
    """Test text analysis endpoint"""
    test_data = {
        "text": "This is a great product! I love it.",
        "analysis_type": "sentiment"
    }
    
    response = client.post("/api/v1/analyze/text", json=test_data)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "data" in data
    assert "sentiment" in data["data"]

def test_text_analysis_comprehensive():
    """Test comprehensive text analysis"""
    test_data = {
        "text": "This is a sample text for comprehensive analysis. It has multiple sentences.",
        "analysis_type": "comprehensive"
    }
    
    response = client.post("/api/v1/analyze/text", json=test_data)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "word_count" in data["data"]
    assert "character_count" in data["data"]
    assert "sentiment" in data["data"]

def test_batch_analysis():
    """Test batch analysis endpoint"""
    test_data = {
        "texts": [
            "This is great!",
            "This is terrible.",
            "This is neutral."
        ],
        "analysis_type": "sentiment"
    }
    
    response = client.post("/api/v1/analyze/batch", json=test_data)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert data["total_items"] == 3
    assert len(data["results"]) == 3
    assert "summary" in data

def test_model_info_endpoint():
    """Test model info endpoint"""
    response = client.get("/api/v1/models/info")
    assert response.status_code == 200
    data = response.json()
    assert "available_models" in data
    assert "supported_formats" in data
    assert "analysis_types" in data

def test_invalid_text_analysis():
    """Test text analysis with invalid input"""
    test_data = {
        "text": "",  # Empty text should cause validation error
        "analysis_type": "sentiment"
    }
    
    response = client.post("/api/v1/analyze/text", json=test_data)
    assert response.status_code == 422  # Validation error

def test_file_analysis_endpoint():
    """Test file analysis endpoint with text file"""
    test_content = "This is a test file content for analysis."
    
    files = {"file": ("test.txt", test_content, "text/plain")}
    data = {"format_type": "text", "analysis_type": "sentiment"}
    
    response = client.post("/api/v1/analyze/file", files=files, data=data)
    assert response.status_code == 200
    result = response.json()
    assert result["success"] == True
    assert "data" in result
    assert result["metadata"]["filename"] == "test.txt"