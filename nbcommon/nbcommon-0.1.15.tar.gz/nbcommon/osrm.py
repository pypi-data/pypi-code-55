from typing import List, Tuple, Optional
from pydantic import BaseModel
from enum import Enum
from .geo import LatLng
from .aiorequests import http_get_json
from urllib.parse import urlencode


class Code(str, Enum):
    Ok = "Ok"
    InvalidUrl = "InvalidUrl"
    InvalidService = "InvalidService"
    InvalidVersion = "InvalidVersion"
    InvalidOptions = "InvalidOptions"
    InvalidQuery = "InvalidQuery"
    InvalidValue = "InvalidValue"
    NoSegment = "NoSegment"
    TooBig = "TooBig"


class Response(BaseModel):
    code: Code


LngLat = Tuple[float, float]  # format is: [lng, lat]


class WayPoint(BaseModel):
    hint: Optional[str]
    distance: float
    name: Optional[str]
    location: Optional[LngLat]
    nodes: Optional[List[int]]


class NearestResponse(Response):
    waypoints: List[WayPoint]


class Leg(BaseModel):
    distance: float
    duration: float


class Route(BaseModel):
    duration: Optional[float]
    distance: Optional[float]
    legs: List[Leg] = []


class RouteResponse(Response):
    routes: List[Route] = []
    waypoints: List[WayPoint] = []


class POI(BaseModel):
    name: str
    location: LngLat


class TableResponse(Response):
    sources: List[POI]
    destinations: List[POI]
    durations: List[List[float]]
    distances: List[List[float]]


class TracePoint(BaseModel):
    matchings_index: int
    location: LngLat


class MatchResponse(Response):
    tracepoints: List[TracePoint]
    matchings: List[Route]


class Gaps(str, Enum):
    """
    Allows the input track splitting based on huge timestamp gaps between points.
    """
    split = "split"
    ignore = "ignore"


class API:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def nearest(self, loc: LatLng, radius: Optional[float] = None, bearing: Optional[float] = None) -> NearestResponse:
        url = f'{self.base_url}/nearest/v1/driving/{loc.lng},{loc.lat}'
        params = {}
        if radius is not None:
            params['radiuses'] = radius
        if bearing is not None:
            params['bearings'] = bearing
        url += "?" + urlencode(params)
        return NearestResponse(** (await http_get_json(url)))

    async def route(self, coords: List[LatLng]) -> RouteResponse:
        coords_param = ';'.join([f'{c.lng},{c.lat}' for c in coords])
        url = f'{self.base_url}/route/v1/driving/{coords_param}.json?overview=full'
        return RouteResponse(** (await http_get_json(url)))

    async def table(self, coords: List[LatLng], sources: List[int], destinations: List[int]) -> TableResponse:
        coords_param = ';'.join([f'{c.lng},{c.lat}' for c in coords])
        sources_param = ';'.join(sources)
        destinations_param = ';'.join(destinations)
        url = f'{self.base_url}/table/v1/driving/{coords_param}.json?sources={sources_param}&destinations={destinations_param}&annotations=duration,distance'
        return TableResponse(** (await http_get_json(url)))

    async def match(self, coords: List[LatLng],
                    timestamps: Optional[List[int]] = None,
                    radiuses: Optional[List[float]] = None,
                    gaps: Gaps = Gaps.split,
                    tidy: bool = False) -> MatchResponse:
        coords_param = ';'.join([f'{c.lng},{c.lat}' for c in coords])
        url = f'{self.base_url}/match/v1/driving/{coords_param}.json'
        params = {}
        if timestamps is not None:
            params['timestamps'] = ";".join(timestamps)
        if radiuses is not None:
            params['radiuses'] = ";".join(radiuses)
        params['gaps'] = gaps.value
        if tidy:
            params['tidy'] = "true"
        url += "?" + urlencode(params)

        return MatchResponse(** (await http_get_json(url)))
