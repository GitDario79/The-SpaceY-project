from pydantic import BaseModel
from typing import List

class Features(BaseModel):
    features: List[float]

class BatchFeatures(BaseModel):
    batch: list[list[float]]
