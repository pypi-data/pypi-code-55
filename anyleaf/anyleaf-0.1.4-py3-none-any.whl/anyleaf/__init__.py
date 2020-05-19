# Driver for the Anyleaf pH module

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Compensate for temperature diff between readings and calibration.
PH_TEMP_C = -0.05694  # pH/(V*T);


class Smoothing(Enum):
    NoSmoothing = auto()
    Little = auto()
    Lot = auto()


class CalSlot(Enum):
    """Keeps our calibration organized, so we track when to overwrite."""
    ONE = auto()
    TWO = auto()
    THREE = auto()


@dataclass
class CalPt:
    V: float
    pH: float
    T: float


@dataclass
class PhSensor:
    adc: ADS
    smoothing: Smoothing
    cal_1: CalPt
    cal_2: CalPt
    cal_3: Optional[CalPt]

    def __init__(self, i2c):
        adc = ADS.ADS1115(i2c)
        adc.gain = 2
        self.adc = adc
        self.smoothing = Smoothing.Little
        self.cal_1 = CalPt(0, 7.0, 23)
        self.cal_2 = CalPt(0.18, 4.0, 23)
        self.cal_3 = None

    def read(self) -> float:
        T = temp_from_voltage(AnalogIn(self.adc, ADS.P2).voltage)

        chan_ph = AnalogIn(self.adc, ADS.P0, ADS.P1)
        return ph_from_voltage(chan_ph.voltage, T, self.cal_1, self.cal_2, self.cal_3)

    def read_voltage(self) -> float:
        """Useful for getting calibration data"""
        return AnalogIn(self.adc, ADS.P0, ADS.P1).voltage

    def read_temp(self) -> float:
        """Useful for getting calibration data"""
        return temp_from_voltage(AnalogIn(self.adc, ADS.P2).voltage)

    def calibrate(self, slot: CalSlot, pH: float):
        T = temp_from_voltage(AnalogIn(self.adc, ADS.P2).voltage)
        pt = CalPt(AnalogIn(self.adc, ADS.P0, ADS.P1).voltage, pH, T)

        if slot == CalSlot.ONE:
            self.cal_1 = pt
        elif slot == CalSlot.TWO:
            self.cal_2 = pt
        elif slot == CalSlot.THREE:
            self.cal_3 = pt
        else:
            raise AttributeError("Invalid Calibration slot. Must be `CalSlot.One` etc")

    def calibrate_all(self, pt0: CalPt, pt1: CalPt, pt2: Optional[CalPt] = None):
        self.cal_1 = pt0
        self.cal_2 = pt1
        self.cal_3 = pt2

    def reset_calibration(self):
        self.cal_1 = CalPt(0.0, 7.0, 25.0)
        self.cal_2 = CalPt(0.18, 4.0, 25.0)
        self.cal_3 = None


def lg(
    pt0: (float, float), pt1: (float, float), pt2: (float, float), X: float
) -> float:
    """Compute the result of a Lagrange polynomial of order 3.
Algorithm created from the `P(x)` eq
[here](https://mathworld.wolfram.com/LagrangeInterpolatingPolynomial.html)."""
    result = 0.0

    x = [pt0[0], pt1[0], pt2[0]]
    y = [pt0[1], pt1[1], pt2[1]]

    for j in range(3):
        c = 1.0
        for i in range(3):
            if j == i:
                continue
            c *= X - x[i] / (x[j] - x[i])
        result += y[j] * c

    return result


def ph_from_voltage(
    V: float, T: float, cal_0: CalPt, cal_1: CalPt, cal_2: Optional[CalPt],
) -> float:
    """Convert voltage to pH
    We model the relationship between sensor voltage and pH linearly
    using 2-pt calibration, or quadratically using 3-pt. Temperature
    compensated. Input `temp` is in Celsius."""

    # We infer a -.05694 pH/(V*T) sensitivity linear relationship
    # (higher temp means higher pH/V ratio)
    T_diff = T - cal_0.T
    T_comp = PH_TEMP_C * T_diff  # pH / V

    if cal_2:
        result = lg((cal_0.V, cal_0.pH), (cal_1.V, cal_1.pH), (cal_2.V, cal_2.pH), V)
        return result + T_comp * V
    else:
        a = (cal_1.pH - cal_0.pH) / (cal_1.V - cal_0.V)
        b = cal_1.pH - a * cal_1.V
        return (a + T_comp) * V + b


def temp_from_voltage(V: float) -> float:
    """Map voltage to temperature for the TI LM61, in °C
    Datasheet: https://datasheet.lcsc.com/szlcsc/Texas-Instruments-
    TI-LM61BIM3-NOPB_C132073.pdf"""
    return 100.0 * V - 60.0
