__all__ = ["PmcMotor"]

import asyncio
from typing import Dict, Any, List

from yaqd_core import ContinuousHardware

from .__version__ import __branch__
from . import mcapi


class PmcMotor(ContinuousHardware):
    _kind = "pmc"
    _version = "0.1.0" + f"+{__branch__}" if __branch__ else ""
    defaults = {
        "counts_per_mm": 58200,
        "controller": 0,
        "axis": 0,
        "tolerance": 20,
        "acceleration": 70000.0,
        "gain": 2211.0,
        "velocity": 11000.0,
        "integral_gain": 0,
        "integration_limit": 0,
        "integration_option": 0,
        "derivative_gain": 6000.0,
        "derivative_sample": 0.001364,
        "following_error": 0.0,
        "velocity_gain": 0.0,
        "accel_gain": 0.0,
        "decel_gain": 0.0,
        "encoder_scaling": 0.0,
        "update_rate": 0.0,
        "position_deadband": 0.0,
        "delay_at_target": 0.0,
        "output_offset": 0.0,
        "output_deadband": 0.0,
        "units": "mm",
        # "enable_backlash_correction": False,
        # "backlash": 1000,
    }

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        self.controller = mcapi.Mcapi()
        self.axis = config["axis"]
        self.controller.Open(config["controller"], 1)
        self.controller.EnableAxis(self.axis, True)

        self.counts_per_mm = config["counts_per_mm"]
        self.tolerance = config["tolerance"]
        # self.backlash_enabled = config["enable_backlash_correction"]
        # self.backlash = config["backlash"]
        # self.backlashing = False

        self.filter = self._get_filter(config)
        self.controller.SetFilterConfigEx(self.axis, self.filter)
        self.controller.SetAcceleration(self.axis, config["acceleration"])
        self.controller.SetGain(self.axis, config["gain"])
        self.controller.SetVelocity(self.axis, config["velocity"])

    def _get_filter(self, config):
        filt = mcapi.MCFILTEREX()
        filt.Gain = config["gain"]
        filt.IntegralGain = config["integral_gain"]
        filt.IntegrationLimit = config["integration_limit"]
        filt.IntegralOption = config["integration_option"]
        filt.DerivativeGain = config["derivative_gain"]
        filt.DerSamplePeriod = config["derivative_sample"]
        filt.FollowingError = config["following_error"]
        filt.VelocityGain = config["velocity_gain"]
        filt.AccelGain = config["accel_gain"]
        filt.DecelGain = config["decel_gain"]
        filt.EncoderScaling = config["encoder_scaling"]
        filt.UpdateRate = int(config["update_rate"])
        filt.PositionDeadband = config["position_deadband"]
        filt.DelayAtTarget = config["delay_at_target"]
        filt.OutputOffset = config["output_offset"]
        filt.OutputDeadband = config["output_deadband"]
        return filt

    def _set_position(self, position):
        self.controller.MoveAbsolute(self.axis, self.mm_to_steps(position))

    async def update_state(self):
        overflow = b""
        while True:
            self._position = self.steps_to_mm(self.controller.GetPositionEx(self.axis))
            self._busy = (
                abs(self.mm_to_steps(self._position) - self.mm_to_steps(self._destination))
                > self.tolerance
            )
            # _, _, lo, hi = self.controller.GetLimits(self.axis)
            # a = self.controller.GetLimits(self.axis)
            # print(a)
            # self._limits = [(lo, hi)]
            try:
                await asyncio.wait_for(self._busy_sig.wait(), 0.1)
            except asyncio.TimeoutError:
                pass

    def stop(self):
        self.ctrl.Stop(self.axis)

    def steps_to_mm(self, steps):
        return 50 - steps / self.counts_per_mm

    def mm_to_steps(self, mm):
        return round((50 - mm) * self.counts_per_mm)

    def reset_to_known_position(self, position):
        self.controller.SetPosition(self.axis, self.mm_to_steps(position))
        self._destination = position

    # Are the following even useful??
    def get_following_error(self):
        return self.controller.GetFollowingError(self.axis)

    def get_target(self):
        return self.steps_to_mm(self.controller.GetTargetEx(self.axis))

    def at_target(self):
        return self.controller.IsAtTarget(self.axis, 3)
