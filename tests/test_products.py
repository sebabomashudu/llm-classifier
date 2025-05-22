from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

product_test_cases = [
    {"text": "This 4K monitor has amazing color accuracy", "expected": "Electronics"},
    {"text": "Kitchen knife set stays sharp after months", "expected": "Home & Kitchen"},
]

def test_product_categorization():
    """Test product classification endpoint""" 
    for case in product_test_cases:
        response = client.post(
            "/classify",
            json={"text": case["text"], "config_name": "categories"}
        )
        assert response.status_code == 200
        result = response.json()
        assert result["classification"] in result["available_classes"]