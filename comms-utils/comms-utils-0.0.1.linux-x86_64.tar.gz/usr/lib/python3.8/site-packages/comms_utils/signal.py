import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from typing import List, Tuple
from comms_utils.pulse import Pulse

class Signal():
    def __init__(self, data: np.ndarray, time: np.ndarray, levels: int=4, pulse: Pulse=None):
        self.data = data
        self.original_data = data
        self.pulse = pulse
        self.levels = levels
        self.time = time
        self.noise_db = None
        self.noise = np.random.normal(0, 1, len(data))
        self.length = len(data)
        self.max_signal = ((levels/2)+1)
        self.min_signal = -((levels/2)+1)

    def add_noise(self, eb2n: float):
        eb2n = 10 ** (eb2n/10)
        var = 1/(2*eb2n)
        noise = np.sqrt(var)
        awgn = noise * self.noise
        
        data_noise = np.array(self.data) + awgn
        self.data = data_noise
        
        self.noise_db = eb2n

    def get_levels(self) -> int:
        return self.levels

    def regen_noise(self):
        self.noise = self.noise = np.random.normal(0, 1, len(self.data))

    def get_pulse(self) -> Pulse:
        return self.pulse
    
    def remove_noise(self):
        self.data = self.original_data

    def get_snr_db(self) -> float:
        return self.noise_db

    def get_data(self):
        return self.data, self.time

    def plot(self, title: str=None, pgf_plot: str=None):
        x = list(range(len(self.data)))
        plot = plt.plot(self.time, self.data)
        if(title == None):
            plt.title("Signal")
        else:
            plt.title(title)
            
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        if pgf_plot == None:
            plt.show()
        else:
            plt.savefig(pgf_plot)
    
    def plot_psd(self, title: str=None, pgf_plot: str=None):
        dt = (self.time[-1] - self.time[0]) / len(self.time)
        fig = plt.figure(constrained_layout=True)
        gs = gridspec.GridSpec(2, 1, figure=fig)
        ax = fig.add_subplot(gs[0, :])
        ax.plot(self.time, self.data, '-b')
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")
        
        if(title == None):
            plt.title("Signal")
        else:
            plt.title(title)

        ax2 = fig.add_subplot(gs[1, :])
        ax2.psd(self.data, 512, 1 / dt)
        ax2.set_xlabel("Frequency (f)")
        ax2.set_ylabel("Power Spectral Density (dB/Hz)")

        if pgf_plot == None:
            plt.show()
        else:
            plt.savefig(pgf_plot)

    def convolve(self, pulse: Pulse):
        self.pulse = pulse
        pulse_data = np.array([pulse[float(t-pulse.get_peak_delay()*self.time[-1])] for t in self.time], dtype=np.float32)
        convoled = np.convolve(pulse_data, self.data)
        
        period = (self.time[-1]-self.time[0]) / len(self.time)
        conv_time = np.arange(self.time[0], (self.time[-1]-self.time[0])*2, period)

        if len(conv_time) < len(convoled):
            for _ in range(len(convoled) - len(conv_time)):
                conv_time.append(conv_time[-1]+period)
        if len(conv_time) > len(convoled):
            conv_time = conv_time[:len(convoled)-len(conv_time)]  
        
        return Signal(convoled, conv_time, self.levels, pulse=self.pulse)

    def __mul__(self, other) -> List[float]:
        if type(other) != list:
            raise TypeError("Must multiply by a list")
        if len(other) != len(self.data):
            raise IndexError("Lists must be the same length")
        other_arr = np.array(other, dtype=np.float32)
        data_arr = np.array(self.data, dtype=np.float32)
        result = other_arr * data_arr
        
        return result.tolist()

    def __getitem__(self, key) -> float:
        if type(key) != int and type(key) != float:
            raise KeyError("Key must be either int or float")
        i = self.time.index(min(self.time, key=lambda x:abs(x-key)))
        return self.data[i]

    def __len__(self) -> int:
        return abs(self.length)
