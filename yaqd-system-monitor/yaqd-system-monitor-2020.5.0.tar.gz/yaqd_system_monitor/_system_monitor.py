__all__ = ["SystemMonitor"]

import asyncio
from typing import Dict, Any, List

import psutil  #  type: ignore
from uptime import uptime  # type: ignore

from yaqd_core import Sensor, logging

from .__version__ import __branch__


def diskio():
    """
    https://stackoverflow.com/a/49359851
    """
    p = psutil.Process()
    io_counters = p.io_counters()
    disk_usage_process = io_counters[2] + io_counters[3]  # read_bytes + write_bytes
    disk_io_counter = psutil.disk_io_counters()
    disk_total = disk_io_counter[2] + disk_io_counter[3]  # read_bytes + write_bytes
    return disk_usage_process / disk_total * 100


class SystemMonitor(Sensor):
    _kind = "system-monitor"
    _version = "1.0.0" + f"+{__branch__}" if __branch__ else ""
    traits: List[str] = []
    defaults: Dict[str, Any] = {}

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        self.channel_names = ["cpu", "memory", "diskio", "uptime"]
        self.channel_units = {"cpu": "%", "memory": "%", "diskio": "%", "uptime": "s"}

    async def _measure(self):
        out = dict()
        out["cpu"] = psutil.cpu_percent()
        out["memory"] = 100 - dict(psutil.virtual_memory()._asdict())["percent"]
        out["diskio"] = diskio()
        out["uptime"] = uptime()
        if self.looping:
            await asyncio.sleep(1)
        return out
