from fastapi import APIRouter
from circlepacker.domain.contracts import SimpleSolve
from circlepacker.optimization.solver import cost
import scipy.optimize
from typing import Text
import json

router = APIRouter()


@router.post("/")
async def solves(simple_input: SimpleSolve = None) -> Text:
    bounds = simple_input.bounds  # type: ignore
    radii = simple_input.radii  # type: ignore

    res = scipy.optimize.differential_evolution(cost, bounds, args=(*radii,))
    output = f"{res.x.tolist()}, {res.fun}"
    return output
