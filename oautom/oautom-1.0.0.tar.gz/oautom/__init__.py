import json
from enum import Enum
from functools import partial
from typing import Dict

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import BaseScheduler
from apscheduler.schedulers.blocking import BlockingScheduler

from flow import Flow
from logger import get_logger
from vect import Vect


class OAutomMode(Enum):
    foreground = 'foreground'
    background = 'background'


class OAutom:

    def __init__(self, mode: OAutomMode = OAutomMode.foreground):
        self._logger = get_logger()
        self._flows = {}  # type: Dict[str, Flow]
        self._vects = {}  # type: Dict[str, Vect]
        self._logged_vects = []  # type: List[Vect]
        self._scheduler = self._event_loop(mode)

    def flows(self):
        return [flow.name() for flow in self._flows.values()]

    def logs(self):
        return [vect.status() for vect in self._logged_vects]

    def register_flow(self, flow: 'Flow'):
        self._flows[flow.name()] = flow

    def run(self):
        self._scheduler.start()

    def start(self, flow_name: str) -> bool:
        result = False
        vects = self._vects
        if flow_name not in vects or vects[flow_name].ended():
            vect = self._flows[flow_name].vect()
            vects[flow_name] = vect
            self._logged_vects.insert(0, vect)
            self._logger.info(f"run a new vect for {flow_name}")
            result = True

        return result

    def plan(self, flow_name: str, days: int = 0, hours: int = 0, minutes: int = 0):
        flow_vect = partial(self.start, flow_name)
        self._scheduler.add_job(flow_vect,
                                trigger="interval",
                                days=days,
                                hours=hours,
                                minutes=minutes)

    def status(self, flow_name: str):
        result = {}
        if flow_name in self._vects:
            result = self._vects[flow_name].status()

        return result

    def _event_loop(self, mode: OAutomMode) -> BaseScheduler:
        if mode == OAutomMode.background:
            scheduler = BackgroundScheduler()
        else:
            scheduler = BlockingScheduler()

        self._job = scheduler.add_job(func=self._move_vects_if_ready,
                                      trigger="interval",
                                      seconds=10)
        return scheduler

    def _move_vects_if_ready(self):
        for vect in self._vects.values():
            vect.run_if_ready()
