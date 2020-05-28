import collections
import dataclasses
from typing import List, Mapping


Timings = Mapping[str, float]
PassedPhase = collections.namedtuple('PassedPhase', ['phase', 'entered_at'])


@dataclasses.dataclass
class Progress:
    expected_duration: float
    passed_phases: List[str]
    expected_phases: List[str]
    current_phase: str
    phase_progress: float
    duration: float
    progress: float
    is_stuck: bool
