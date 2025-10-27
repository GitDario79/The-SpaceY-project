import joblib, os
from typing import List

_MODEL = None

def load_model(path: str = "models/model.joblib"):
    global _MODEL
    if _MODEL is None:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Model not found at {path}. Train or provide an artifact.")
        _MODEL = joblib.load(path)
    return _MODEL

def predict_proba_single(features: List[float]) -> float:
    import numpy as np
    model = load_model()
    X = np.array(features, dtype=float).reshape(1, -1)
    return float(model.predict_proba(X)[0, 1])

def predict_proba_batch(batch: list[list[float]]) -> list[float]:
    import numpy as np
    model = load_model()
    X = np.array(batch, dtype=float)
    return model.predict_proba(X)[:, 1].astype(float).tolist()
