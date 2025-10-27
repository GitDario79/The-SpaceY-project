from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200 and r.json().get("status") == "ok"

def test_predict():
    r = client.post("/predict", json={"features":[0.1,0.2,0.3]})
    assert r.status_code == 200
    assert "reusability_probability" in r.json()
