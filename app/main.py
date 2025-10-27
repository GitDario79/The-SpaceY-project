from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.schemas import Features, BatchFeatures
from src.model import predict_proba_single, predict_proba_batch, load_model

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    load_model()  # fail fast if artifact is missing
    yield
    # shutdown (nothing to clean up yet)

app = FastAPI(title="SpaceY Reusability Predictor", version="0.2.1", lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(feats: Features):
    proba = predict_proba_single(feats.features)
    return {"reusability_probability": round(proba, 3)}

@app.post("/predict-batch")
def predict_batch(payload: BatchFeatures):
    probs = predict_proba_batch(payload.batch)
    return {"reusability_probabilities": [round(p, 3) for p in probs]}


