# Driver for the Anyleaf pH module

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, List

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from filterpy.kalman import KalmanFilter

from . import filter

# Compensate for temperature diff between readings and calibration.
PH_TEMP_C = -0.05694  # pH/(V*T);


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
    filter: KalmanFilter
    cal_1: CalPt
    cal_2: CalPt
    cal_3: Optional[CalPt]

    def __init__(self, i2c, dt: float):
        # `dt` is in seconds.
        adc = ADS.ADS1115(i2c)
        adc.gain = 2  # Set the ADC's voltage range to be +-2.048V.
        self.adc = adc
        self.filter = filter.create(dt)
        self.cal_1 = CalPt(0, 7.0, 23)
        self.cal_2 = CalPt(0.18, 4.0, 23)
        self.cal_3 = None

    def predict(self) -> None:
        """Make a prediction using the Kalman filter. Not generally used
        directly."""
        self.filter.predict()

    def update(self) -> None:
        """Update the Kalman filter with a pH reading. Not generally used
        directly."""
        raw = self.read_raw()  # todo remove this intermed var.
        print("Raw", raw)
        self.filter.update(raw)

    def read(self) -> float:
        """Take a pH reading, using the Kalman filter. This reduces sensor 
        noise, and provides a more accurate reading."""
        self.predict()
        self.update()
        # self.filter.x is mean, variance. We only care about the mean
        return self.filter.x[0][0]

    def read_raw(self) -> float:
        """Take a pH reading, without using the Kalman filter"""
        T = temp_from_voltage(AnalogIn(self.adc, ADS.P2).voltage)

        chan_ph = AnalogIn(self.adc, ADS.P0, ADS.P1)
        return ph_from_voltage(chan_ph.voltage, T, self.cal_1, self.cal_2, self.cal_3)

    def read_voltage(self) -> float:
        """Useful for getting calibration data"""
        return AnalogIn(self.adc, ADS.P0, ADS.P1).voltage

    def read_temp(self) -> float:
        """Useful for getting calibration data"""
        return temp_from_voltage(AnalogIn(self.adc, ADS.P2).voltage)

    def calibrate(self, slot: CalSlot, pH: float) -> (float, float):
        """Calibrate by measuring voltage and temp at a given pH. Set the
        calibration, and return (Voltage, Temp)."""
        T = temp_from_voltage(AnalogIn(self.adc, ADS.P2).voltage)
        V = AnalogIn(self.adc, ADS.P0, ADS.P1).voltage
        pt = CalPt(V, pH, T)

        if slot == CalSlot.ONE:
            self.cal_1 = pt
        elif slot == CalSlot.TWO:
            self.cal_2 = pt
        else:
            self.cal_3 = pt

        return V, T

    def calibrate_all(
        self, pt0: CalPt, pt1: CalPt, pt2: Optional[CalPt] = None
    ) -> None:
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
    return 100. * V - 60.
