from fastapi import APIRouter
from circlepacker.domain.contracts import SimpleSolve, ServiceSolve, ServiceOutput
from circlepacker.optimization.solver import cost, create_bounds
import scipy.optimize
from typing import Text
import numpy as np

router = APIRouter()


@router.post("/simple_solve")
async def solves_simple(simple_input: SimpleSolve) -> Text:
    bounds = simple_input.bounds  # type: ignore
    radii = simple_input.radii  # type: ignore

    res = scipy.optimize.differential_evolution(cost, bounds, args=(*radii,))
    output = f"{res.x.tolist()}, {res.fun}"
    return output


@router.post("/solve_configuration")
async def solves_configuration(service_input: ServiceSolve) -> ServiceOutput:
    bounds, radii = create_bounds(service_input)

    res = scipy.optimize.differential_evolution(cost, bounds, args=(*radii,))
    xy_res = np.reshape(res.x, (-1, 2))
    return ServiceOutput(x=xy_res[:, 0].tolist(), y=xy_res[:, 1].tolist(), radii=radii)
