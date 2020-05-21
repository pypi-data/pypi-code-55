import datetime
from typing import Any, Optional, Sequence

from docbrown.models import PassedPhase, Progress, Timings


def _calculate_progress(
        passed_phases: Sequence[PassedPhase],
        timings: Timings,
        now: datetime.datetime) -> Progress:
    current_phase = passed_phases[-1]
    current_phase_duration = (now - current_phase.entered_at).total_seconds()
    current_duration = (now - passed_phases[0].entered_at).total_seconds()
    empirical_total_duration = sum(timings.values())
    passed_phase_names = [phase.phase for phase in passed_phases]

    # we calculate the expected duration as the total of
    #  * the time it took for previous phases to complete
    #  * the time that passed since the current phase was triggered
    #  * the time of each phase that was not triggered yet, based on empirical data.
    expected_total_duration = 0
    for index, phase in enumerate(passed_phases):
        try:
            next_phase = passed_phases[index + 1]
        except IndexError:
            break
        expected_total_duration += (next_phase.entered_at - phase.entered_at).total_seconds()
    expected_total_duration += max(current_phase_duration, timings[current_phase.phase])
    for phase_name in timings.keys():
        if phase_name not in passed_phase_names:
            expected_total_duration += timings[phase_name]

    # calculate the progress as the total of
    #  * the time it took to complete passed phases as ratio
    #    in relation to the empirical total duration
    #  * the time spent in the current phase or the empirical time spent in the current phase
    #    as ratio in relation to the empirical total duration (whichever is smaller)
    total_progress = 0
    for phase in passed_phase_names:
        if phase != current_phase.phase:
            total_progress += (timings[phase] / empirical_total_duration)
    empirical_phase_ratio = timings[current_phase.phase] / empirical_total_duration
    current_phase_ratio = current_phase_duration / empirical_total_duration
    # Use the minimum of both values because more time spent in this phase
    # does not mean that following phases will take less time. This will
    # cause the progress to get stuck in place, but avoids progress that
    # goes backwards or stays at 100% for prolonged periods of time.
    total_progress += min(empirical_phase_ratio, current_phase_ratio)

    # define a phase as stuck if it took 1.5 × the amount of time it usually does
    is_phase_stuck = current_phase_ratio / empirical_phase_ratio >= 1.5

    return Progress(
        expected_duration=expected_total_duration,
        passed_phases=len(passed_phases),
        expected_phases=len(timings) - 1,
        current_phase=current_phase.phase,
        duration=current_duration,
        progress=min(100, max(0, total_progress * 100)),
        is_stuck=is_phase_stuck,
    )


class StorageBackend:
    def store_timings(self, ident, aggregator_key: str, timings: Timings) -> None:
        raise NotImplementedError()

    def store_progress(self, ident: str, aggregator_key: str, phase: str,
                       entered_at: datetime.datetime) -> None:
        raise NotImplementedError()

    def clear_progress(self, ident: str) -> None:
        raise NotImplementedError()

    def get_progress(self, ident: str, aggregator_func: Any) -> Optional[Progress]:
        raise NotImplementedError()
