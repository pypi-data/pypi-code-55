import numpy as np
import sympy as sp
from typing import List
import comms_utils.ak as ak

class RN():
    def __init__(self, ak):
        self.ak = ak
        self.N = ak.length[0]
        
    def __getitem__(self, key) -> float:
        if type(key) != int:
            raise IndexError("Can only index Rn type with int")
        return float(1/self.N * (sum(self.ak * self.ak.shift_left(key))))

if __name__ == "__main__":
    ak = ak.AK(data=[1,1,1,2,3,4,5,6,8])
    rn = RN(ak)
    print(rn[2])