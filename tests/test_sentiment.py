from fastapi.testclient import TestClient
from app.main import app
import pytest
import os
import time

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_app_state():
    """Fixture to reset app state before each test"""
    # Initialize required state
    if not hasattr(app.state, 'metrics'):
        app.state.metrics = {"total_requests": 0, "avg_time": 0.0}
    else:
        app.state.metrics["total_requests"] = 0
        app.state.metrics["avg_time"] = 0.0
    
    # Ensure LLM client exists
    if not hasattr(app.state, 'llm'):
        from app.llm import OpenAIService
        app.state.llm = OpenAIService()
    
    yield

def test_sentiment_analysis():
    """Test sentiment analysis with existing config"""
    test_cases = [
        {"text": "This movie was fantastic!", "expected": ["positive", "negative"]},
        {"text": "I hated every minute", "expected": ["positive", "negative"]}
    ]
    
    for case in test_cases:
        response = client.post(
            "/classify",
            params={"text": case["text"], "config_name": "sentiment"}
        )
        assert response.status_code == 200
        result = response.json()
        assert result["classification"] in case["expected"]
        assert "processing_time" in result

def test_product_categorization():
    """Test product categorization with existing config"""
    test_cases = [
        {"text": "High quality wireless headphones", "expected": ["Electronics"]},
        {"text": "Stainless steel kitchen knives", "expected": ["Home & Kitchen"]}
    ]
    
    for case in test_cases:
        response = client.post(
            "/classify",
            params={"text": case["text"], "config_name": "categories"}
        )
        assert response.status_code == 200
        result = response.json()
        assert result["classification"] in case["expected"]

def test_error_handling():
    """Test error scenarios with existing config"""
    # Empty text
    response = client.post(
        "/classify",
        params={"text": "", "config_name": "sentiment"}
    )
    assert response.status_code == 400
    error_detail = response.json()["detail"]  # Get the detail field
    assert "error" in error_detail  # Now check inside detail
    assert "message" in error_detail
    
    # Invalid config
    response = client.post(
        "/classify",
        params={"text": "test", "config_name": "invalid_config"}
    )
    assert response.status_code == 400
    error_detail = response.json()["detail"]
    assert "error" in error_detail
    assert "available_configs" in error_detail

def test_health_check():
    """Test health endpoint with existing metrics"""
    # Make sample request to populate metrics
    client.post(
        "/classify",
        params={"text": "test", "config_name": "sentiment"}
    )
    
    response = client.get("/health")
    assert response.status_code == 200
    health = response.json()
    assert health["status"] == "healthy"
    assert health["requests_handled"] >= 1
    assert "avg_response_time" in health