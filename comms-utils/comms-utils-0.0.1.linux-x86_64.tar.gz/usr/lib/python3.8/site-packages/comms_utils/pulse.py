import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from typing import List

class Pulse():
    def __init__(self, period: float):
        self.period = period
        self.peak_delay = 0
        self.max_pulses = -1

    def get_period(self) -> float:
        return self.period

    def time_domain(self, t: float) -> float:
        if self.max_pulses != -1:
            if abs(t/self.period) >= self.max_pulses:
                return 0
        return 1
    
    def freq_domain(self, f: float) -> float:
        return 1

    def apply_conv_delay(self, conv_len: int, signal: List[float]) -> List[float]:
        output = signal.copy()
        for _ in range(int(int(conv_len/2)*self.get_peak_delay())):
            output.insert(0,0.0)
        for _ in range(int(int(conv_len/2)*(1-self.get_peak_delay()))):
            output.append(0.0)

        if conv_len > len(output):
            output.append(0)
        return output

    def get_peak_delay(self) -> float:
        return self.peak_delay

    def plot(self, num_periods: int, samples: int=50):
        time = self.get_pulse_times(samples, num_periods)
        data = self.get_num_pulses(samples, num_periods)
        plt.plot(time, data)
        plt.show()

    def get_max_pulses(self) -> int:
        return self.max_pulses

    def set_max_pulses(self, max_pulses: int):
        self.max_pulses = max_pulses

    def get_num_pulses(self, samples: int, num_periods: int) -> List[float]:
        return [self[float(val)] for val in np.arange(0, self.get_period()*num_periods, self.get_period()*num_periods/samples)]

    def get_pulse_times(self, samples: int, num_periods: int) -> List[float]:
        return [float(val) for val in np.arange(0, self.get_period()*num_periods, self.get_period()*num_periods/samples)]

    def __getitem__(self, key) -> float:
        if type(key) != int and type(key) != float:
            raise KeyError("Key must be either int or float")
        return self.time_domain(key)


class Rect(Pulse):
    def __init__(self, period: float):
        super().__init__(period)
        self.peak_delay = 1/2
        self.max_pulses = 1
        

    def time_domain(self, t: float) -> float:
        if self.max_pulses != -1:
            if abs(t/self.period) >= self.max_pulses:
                return 0
        if (abs(t) % self.period) < (self.period-self.period/2):
            return 1
        return 0
    
    def freq_domain(self, f: float) -> float:
        return np.sinc((np.pi*(f-self.period/2)/self.period))
    

class Sinc(Pulse):
    def __init__(self, period: float):
        super().__init__(period)
        self.peak_delay = 1/2
    
    def time_domain(self, t: float) -> float:
        if t == 0:
            return 1
        if self.max_pulses != -1:
            if abs(t/self.period) >= self.max_pulses/2:
                return 0
        return np.sin(t*2*np.pi/(self.period))/(t*2*np.pi/(self.period))

    def get_num_pulses(self, samples: int, num_periods: int) -> List[float]:
        return [self[float(val)] for val in np.arange(-(self.get_period()/2)*num_periods, (self.get_period()/2)*num_periods, self.get_period()/(samples))]

    def get_pulse_times(self, samples: int, num_periods: int) -> List[float]:
        return [float(val) for val in np.arange(-(self.get_period()/2)*num_periods, (self.get_period()/2)*num_periods, self.get_period()/(samples))]

    
class Sin(Pulse):
    def __init__(self, period: float):
        self.peak_delay = 1/2
        super().__init__(period)

    def time_domain(self, t: float):
        if self.max_pulses != -1:
            if abs(t/self.period) >= self.max_pulses:
                return 0
        return np.sin((t)*np.pi/self.period)


class RCos(Pulse):
    def __init__(self, period: float, alpha: float):
        super().__init__(period)
        self.alpha = alpha
        self.peak_delay = 1/2
        # self.bitrate = bitrate
        # self.w = bitrate / 2

    def time_domain(self, t: float) -> float:
        if self.max_pulses != -1:
            if abs(t/self.period) >= self.max_pulses/2:
                return 0
        if abs(t) == (self.period/(2*self.alpha)):
            return (np.pi/(4*self.period))*np.sinc(1/(2*self.alpha))
        return (1/self.period)*np.sinc(t/self.period)*((np.cos((np.pi*self.alpha*t)/self.period))/(1-((2*self.alpha*t)/self.period)**2))
        

    def freq_domain(self, f: float) -> float:
        pass

    def get_num_pulses(self, samples: int, num_periods: int) -> List[float]:
        return [self[float(val)] for val in np.arange(-(self.get_period()/2)*num_periods, (self.get_period()/2)*num_periods, self.get_period()/(samples))]

    def get_pulse_times(self, samples: int, num_periods: int) -> List[float]:
        return [float(val) for val in np.arange(-(self.get_period()/2)*num_periods, (self.get_period()/2)*num_periods, self.get_period()/(samples))]


class RRCos(Pulse):
    def __init__(self, period: float, alpha: float):
        super().__init__(period)
        self.alpha = alpha
        self.peak_delay = 1/2

    def time_domain(self, t: float) -> float:
        if self.max_pulses != -1:
            if abs(t/self.period) >= self.max_pulses/2:
                return 0
        numerator = np.cos((1+self.alpha)*np.pi*t/self.period) + (np.sin((1-self.alpha)*np.pi*t/self.period))/(4*self.alpha*t/self.period)
        return (2*self.alpha/(np.pi*np.sqrt(self.period)))*(numerator/(1-(4*self.alpha * t / self.period)**2))

    def freq_domain(self, f: float) -> float:
        if abs(f) > (1+self.alpha)/(2*self.period):
            return 0
        elif 0 <= abs(f) <= (1-self.alpha)/(2*self.period):
            return np.sqrt(self.period)
        elif (1-self.alpha)/(2*self.period) <= abs(f) <= (1+self.alpha)/(2*self.period):
            return np.sqrt((self.period/2)*(1+np.cos((np.pi*self.period)/self.alpha*(abs(f)-((1-self.alpha)/(2*self.period))))))

        else:
            return None

    def get_num_pulses(self, samples: int, num_periods: int) -> List[float]:
        return [self[float(val)] for val in np.arange(-(self.get_period()/2)*num_periods, (self.get_period()/2)*num_periods, self.get_period()/(samples))]

    def get_pulse_times(self, samples: int, num_periods: int) -> List[float]:
        return [float(val) for val in np.arange(-(self.get_period()/2)*num_periods, (self.get_period()/2)*num_periods, self.get_period()/(samples))]
    