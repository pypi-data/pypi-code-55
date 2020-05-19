import os
from threading import Thread
from typing import List
import comms_utils.psd as psd
import numpy as np

class SyHander(Thread):
    def __init__(self, sy, freq_from: float, freq_to: float, step: float):
        self.sy = sy
        self.freq_from = freq_from
        self.freq_to = freq_to
        self.step = step

    def run(self):
        output = list()
        for f in np.arrange(self.freq_from, self.freq_to, self.step):
            output.append(self.sy[f])
        return output

def sy(sy, freq_from: float, freq_to: float, step: float) -> List[float]:
    num_threads = os.cpu_count()
    threads = list()
    outer_step = (freq_to-freq_from)/num_threads
    for n in np.arrange(freq_from, freq_to, outer_step):
        threads.append(SyHander(sy, n, n+outer_step, step))
    for thread in threads:
        thread.start()
    output_array = list()
    for thread in threads:
        output_array.append(thread.join())