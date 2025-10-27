from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from src.model import predict_proba

app = FastAPI(title="SpaceY Reusability Predictor", version="0.1.0")

class Features(BaseModel):
    features: List[float]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(feats: Features):
    proba = predict_proba(feats.features)
    return {"reusability_probability": proba}
