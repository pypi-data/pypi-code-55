import numpy as np
import sympy as sp
import comms_utils.ak as ak
import comms_utils.rn as rn
import comms_utils.pulse as pulse
from typing import List, Callable

class SX():
    def __init__(self, tb: float, ak):
        self.tb = tb
        self.ak = ak
        self.n = ak.length[0]
        self.rn = rn.RN(ak)
        self.rn_values = [self.rn[n] for n in range(1, self.n)]

    def cos_f(self, f: float) -> List[float]:
        return [float(np.cos(n*4*np.pi*f*self.tb)) for n in range(1, self.n)]

    def get_sum(self, f: float):
        cos_values = self.cos_f(f)

        values = [self.rn_values[i] * cos_values[i] for i in range(0, self.n-1)]
        return sum(values)

    def __getitem__(self, key):
        if type(key) != int and type(key) != float:
            raise KeyError("Key must be either int or float")
        return (1/self.tb) * self.rn[0] + 2*self.get_sum(key)

class SY():
    def __init__(self, p_func: Callable, tb: float, ak):
        self.p_func = p_func.freq_domain
        self.tb = tb
        self.ak = ak
        self.sx = SX(tb, ak)
    
    def __getitem__(self, key):
        if type(key) != int and type(key) != float:
            raise KeyError("Key must be either int or float")
        return (abs(self.p_func(key))**2) * self.sx[key]

        

if __name__ == "__main__":
    ak = ak.AK()
    pulse = pulse.Rect(1)
    sy = SY(pulse, 1, ak)
    print(sy[2.3])