from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200 and r.json().get("status") == "ok"

def test_predict_single():
    r = client.post("/predict", json={"features":[0.1,0.2,0.3]})
    assert r.status_code == 200
    assert "reusability_probability" in r.json()

def test_predict_batch():
    r = client.post("/predict-batch", json={"batch":[[0.1,0.2,0.3],[0.9,1.0,0.8]]})
    assert r.status_code == 200
    out = r.json().get("reusability_probabilities")
    assert isinstance(out, list) and len(out) == 2
