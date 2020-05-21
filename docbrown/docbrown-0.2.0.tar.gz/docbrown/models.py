import collections
import dataclasses
from typing import Mapping


Timings = Mapping[str, float]
PassedPhase = collections.namedtuple('PassedPhase', ['phase', 'entered_at'])


@dataclasses.dataclass
class Progress:
    expected_duration: float
    passed_phases: int
    expected_phases: int
    current_phase: str
    duration: float
    progress: float
    is_stuck: bool
