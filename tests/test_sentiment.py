from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Test data
sentiment_test_cases = [
    {"text": "This movie was life-changing!", "expected": "positive"},
    {"text": "Terrible acting and boring plot.", "expected": "negative"},
    {"text": "The cinematography saved an otherwise mediocre script.", "expected": "negative"},
]

def test_sentiment_analysis():
    """Test sentiment classification endpoint"""
    for case in sentiment_test_cases:
        response = client.post(
            "/classify",
            json={"text": case["text"], "config_name": "sentiment"}
        )
        assert response.status_code == 200
        result = response.json()
        assert result["classification"].lower() in ["positive", "negative"]
        assert result["config_used"] == "sentiment"