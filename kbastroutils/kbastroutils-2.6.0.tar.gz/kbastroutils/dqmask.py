from itertools import combinations
import numpy as np
import copy,sys
class DQMask:
    """
    Example1 (if values are base classes):
    data = [16, 4, 2, 1, 0, 5]
    value = [0,1,4]
    x = DQMask(value)
    x.make_class()
    x.make_mask(data)
    x.value >>> [0,1,4]
    x.combine >>> [0,1,4,5]
    x.data >>> [16, 4, 2, 1, 0, 5]
    x.mask >>> [False, True, False, True, True, True]
    -----------
    Example2 (if values are summed of base classes):
    value = [5]
    x = DQMask(value)
    x.value >>> [5]
    x.make_declass()
    x.value >>> [0,1,4] 
    Then, follow Example1
    Note: x = DQMask(value, declass=True, makeclass=True) gives the same result.
    -----------
    value = list of DQ base classes to be set to True (default: value=[0])
            if this is the case, call x.make_class() to combine all possible classes
            or,
          = a number of the sum of base classes
            if this is the case, call x.make_declass() to declass to base classes. Continue with x.make_class() to combine. Note that x.value is replaced.
    -----------
    DQ Classes:
    From the WFC3 Instrument Handbook (accessed Oct 2019), DQ classes are --
        0 # OK
        1 # Reed Solomon decoding error
        2 # Data missing and replaced by fill value
        4 # Bad detector pixel
        8 # Deviant zero read (bias) value
        16 # Hot pixel
        32 # Unstable response
        64 # Warm pixel
        128 # Bad reference pixel
        256 # Full well saturation
        512 # Bad or uncertain flat value, including 'blobs'
        1024 # (Reserved)
        2048 # Signal in zero read
        4096 # cosmic ray detected by Astrodrizzle
        8192 # Cosmic ray detected during calwf3 up the ramp fitting
        16384 # Pixel affected by ghost/crosstalk
    -----------
    """
    def __init__(self,value=[0],declass=False,makeclass=False):
        self.value = np.array(value)
        if declass:
            self.make_declass()
        if makeclass:
            self.make_class()
        self.data = None
        self.mask = None
    def make_declass(self):
        """
        Example:
        x.value = [5]
        x.make_declass()
        x.value >>> [0,1,4]
        ----------
        make_declass takes sum of classes and calculates back to the original classes from x.value.
        """        
        out = []
        val = int(copy.deepcopy(self.value[0]))
        sentinel = True
        while sentinel:
            tmp = int(np.log2(val))
            tmpp = int(2 ** tmp)
            out.append(tmpp)
            val -= tmpp
            if val==0:
                out.append(0)
                sentinel = False
            elif val<0:
                print('Error: DQ class must be non-negative. Terminate')
                sys.exit()
        self.value = copy.deepcopy(np.array(out))
    def make_class(self):
        """
        Example:
        x.value = [0,1,4]
        x.combine = x.make_class()
        x.combine >>> [0,1,4,5]
        ----------
        make_class combines all possible combine classes from base classes specified in x.value.
        """
        out = []
        n = len(self.value)
        for i in np.arange(n):
            x = i+1
            a = combinations(self.value,x)
            for j in list(a):
                y = np.sum(j)
                if y not in out:
                    out.append(y)
        if 0 not in out:
            out.append(0)
        self.combine = copy.deepcopy(np.array(out))
    def make_mask(self,data):
        """
        Example:
        data = [16, 4, 2, 1, 0]
        x.value = [0,1,4]
        x.mask = x.make_mask(data)
        x.mask >>> [False, True, False, True, True]
        ----------
        make_mask takes self.value and data, and returns self.mask as a bool array parallel to data with 
        x.mask[i] = True if data[i] in x.value, and x.mask[i] = False otherwise.
        """
        self.data = np.array(data)
        self.mask = np.full_like(self.data,fill_value=False,dtype=bool)
        for i in self.value:
            self.mask[np.where(self.data == i)] = True