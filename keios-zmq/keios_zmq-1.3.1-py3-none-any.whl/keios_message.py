from dataclasses import dataclass
from typing import Dict


@dataclass
class KeiosMessage:
    header: Dict[str, str]
    payload: bytes
