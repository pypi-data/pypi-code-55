import numpy as np
import scipy.optimize
import scipy.spatial
from circlepacker.domain.contracts import ServiceSolve
import warnings
from typing import List, Tuple


def create_bounds(
    service_input: ServiceSolve,
) -> Tuple[List[Tuple[float, float]], List[float]]:

    n_dvs = 2 * sum(service_input.count)
    bound_size = sum(
        [a * b for a, b in zip(service_input.diameters, service_input.count)]
    )
    bounds = [(-1 * bound_size, bound_size) for _ in range(n_dvs)]

    radii = [
        d / 2.0
        for i, d in enumerate(service_input.diameters)
        for _ in range(service_input.count[i])
    ]

    return bounds, radii


def overlapping_area(xy_array, radii):
    dist = scipy.spatial.distance.cdist(xy_array, xy_array)
    r1 = np.repeat(radii[:, np.newaxis], len(radii), axis=1)
    r2 = r1.T
    r_scale = r1 + r2
    # TODO: Log warnings, don't surpress.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        d1 = (np.power(r1, 2.0) - np.power(r2, 2.0) + np.power(dist, 2.0)) / (
            2.0 * dist
        )
    d2 = dist - d1

    overlap_map = dist <= r1 - r2
    non_diag = ~np.eye(overlap_map.shape[0], dtype=bool)
    scaling_map = np.logical_and(overlap_map, non_diag)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        a_p1 = np.power(r1, 2.0) * np.arccos(d1 / r1)
        a_p2 = -1.0 * d1 * np.sqrt(np.power(r1, 2.0) - np.power(d1, 2.0))
        a_p3 = np.power(r2, 2.0) * np.arccos(d2 / r2)
        a_p4 = -1.0 * d2 * np.sqrt(np.power(r2, 2.0) - np.power(d2, 2.0))
    total_area = np.nan_to_num(a_p1 + a_p2 + a_p3 + a_p4)
    total_area[scaling_map] += r_scale[scaling_map]
    return total_area


def max_distance(xy_array, radii):
    return np.nanmax(scipy.spatial.distance.cdist(xy_array, np.zeros_like(xy_array)))


def cost(xy_pairs, *args) -> float:
    xy_array = np.reshape(xy_pairs, (-1, 2))
    radii = np.array([args]).flatten()
    if np.any(radii <= 0):
        raise AssertionError(f"One of your radii is less than zero: {radii}")

    def final_cost():
        return np.max(overlapping_area(xy_array, radii)) + np.max(
            max_distance(xy_array, radii)
        )

    return final_cost()


def direct_solver(service_input: ServiceSolve) -> np.array:
    bounds, radii = create_bounds(service_input)

    res = scipy.optimize.differential_evolution(cost, bounds, args=(*radii,))
    return res.x
