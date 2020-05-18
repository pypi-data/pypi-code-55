from typing import Dict, List, TypeVar, Union

from starlette.responses import Response

APIResponse = Union[str, bytes, Response, Dict, List]
UserPredictorClass = TypeVar("UserPredictorClass")
