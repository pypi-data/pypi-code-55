from pydantic import BaseModel
from typing import Text, List, Tuple


class Health(BaseModel):
    status: Text = "Healthy"
    version: Text = ""


class SimpleSolve(BaseModel):
    bounds: List[Tuple[float, float]]
    radii: List[float]
