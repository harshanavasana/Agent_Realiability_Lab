from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_get_runs_endpoint():
    response = client.get("/api/v1/runs")
    assert response.status_code == 200
    assert "runs" in response.json()