import logging
import time
from locust.env import Environment
from locust import events, runners
from typing import Optional
from locust import constant_pacing
from locust.event import EventHook
from typing import Any

_last_run = 0.0
_warning_emitted = False
_target_missed = False


@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument(
        "--ips-limit",
        type=float,
        default=-1,
        help="maximum number of iterations per second. used in combination with wait_time = constant_total_ips",
        env_var="LOCUST_IPS_LIMIT",
    )


@events.quitting.add_listener
def quitting(**_kwargs: Any):
    if _warning_emitted:
        print(
            "Failed to reach targeted number of iterations per second (at some point during the test). Probably caused by target system overload or too few clients"
        )


def constant_ips(ips):
    return constant_pacing(1.0 / ips)


def constant_total_ips():
    def wait_time_func(locust):
        global _warning_emitted, _target_missed, _last_run
        runner = locust.environment.runner
        if runner is None or runner.target_user_count is None:
            return 0
        ips = runner.environment.parsed_options.ips_limit / runner.environment.parsed_options.expect_workers
        current_time = time.time()
        delay = runner.target_user_count / ips
        next_time = _last_run + delay
        if current_time > next_time:
            if runner.state == runners.STATE_RUNNING and _target_missed and not _warning_emitted:
                logging.warning("Failed to reach target ips, even after rampup has finished")
                _warning_emitted = True  # stop logging
            _target_missed = True
            _last_run = current_time
            return 0
        _target_missed = False
        _last_run = next_time
        return delay

    return wait_time_func


_previous_time = 0.0
_rps_fail = False


def rps_sleep(self):
    global _previous_time, _rps_fail
    current_time = float(time.time())
    if runners.locust_runner is None:  # this happens when debugging (running a single locust)
        return
    next_time = self._previous_time + runners.locust_runner.user_count / rps
    if current_time > next_time:
        if runners.locust_runner.state == runners.STATE_RUNNING and not TaskSetRPS._failed_to_reach_rps_target:
            logging.warning("Failed to reach target rps, even after rampup has finished")
            TaskSetRPS._failed_to_reach_rps_target = True  # stop logging
        self._previous_time = current_time
        return

    self._previous_time = next_time
    gevent.sleep(next_time - current_time)
