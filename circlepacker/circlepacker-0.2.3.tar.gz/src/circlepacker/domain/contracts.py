from pydantic import BaseModel
from typing import Text, List, Tuple


class Health(BaseModel):
    status: Text = "Healthy"
    version: Text = ""


class SimpleSolve(BaseModel):
    bounds: List[List[float]] = [[-10.0, 10.0], [-10.0, 10.0]]
    radii: List[float] = [10.0, 10.0]


class ServiceSolve(BaseModel):
    diameters: List[float] = [1.0, 1.0]
    count: List[int] = [1, 1]


class ServiceOutput(BaseModel):
    x: List[float]
    y: List[float]
    radii: List[float]
