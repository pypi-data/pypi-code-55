import numpy as np

from scipy import signal
from .tools import index_of_x, integrate, read_csvs, smooth_curve, y_at_x


class Scan:
    def __init__(self, temps, heat_flows, name=''):
        """
        A Scan on a differential calorimeter.

        :param temps: temperatures (°C)
        :param heat_flow: heat flow (mW)
        """
        assert isinstance(temps, np.ndarray)
        assert isinstance(heat_flows, np.ndarray)

        assert temps.shape == heat_flows.shape

        self.temps = temps
        self.heat_flows = heat_flows
        self.name = name if name is not None else ''

    def __iter__(self):
        """
        Iterate over all of the temperatures and heat_flows in the Scan.

        :yield: temp, heat_flow
        """
        yield from zip(self.temps, self.heat_flows)

    def __eq__(self, other):
        return all(s_t == o_t and s_hf == o_hf for (s_t, s_hf), (o_t, o_hf) in zip(self, other))

    def __len__(self):
        return len(self.temps)

    def __str__(self):
        return 'Scan:\n' + '\n'.join(f'{temp:>5.2f} {heat_flow:>6.4f}' for temp, heat_flow in self)

    def __rsub__(self, other):
        return self.__class__(other - self.temps, other - self.heat_flows, f'{self.name}')

    def __sub__(self, other):
        """
        Subtract a Scan from another Scan, or value(s) from the heat_flows.
        """
        if isinstance(other, Scan):
            if self.temps.shape != other.temps.shape:
                raise NotImplementedError(f'Cannot subtract {self.__class__.__name__} with different shapes.')
            elif any(self.temps != other.temps):
                raise NotImplementedError(f'Cannot subtract {self.__class__.__name__} with different temperatures.')
            return self.__class__(self.temps[:], self.heat_flows - other.heat_flows, f'{self.name} – {other.name}', )
        return self.__class__(self.temps[:], self.heat_flows - other, f'{self.name}')

    def __radd__(self, other):
        return self.__add__(other)

    def __add__(self, other):
        """
        Add a Scan to another Scan, or value(s) to the heat_flows.
        """
        if isinstance(other, Scan):
            if self.temps.shape != other.temps.shape:
                raise NotImplementedError(f'Cannot add {self.__class__.__name__} with different shapes.')
            elif any(self.temps != other.temps):
                raise NotImplementedError(f'Cannot add {self.__class__.__name__} with different temps.')
            return self.__class__(self.temps[:], self.heat_flows + other.heat_flows, f'{self.name} + {other.name}')
        return self.__class__(self.temps[:], self.heat_flows + other, f'{self.name}')

    def __abs__(self):
        """
        Take the absolute values of the heat flows.
        """
        return self.__class__(self.temps[:], abs(self.heat_flows), f'{self.name}')

    def __rtruediv__(self, other):
        return self.__class__(self.temps[:], other/self.heat_flows, f'{other.name} + {self.name}')

    def __truediv__(self, other):
        """
        Divide Scan heat_flows by another Scan heat_flows or value.
        """
        if type(self) == type(other):
            if self.temps.shape != other.temps.shape:
                raise NotImplementedError(f'Cannot divide {self.__class__.__name__} with different shapes.')
            elif any(self.temps != other.temps):
                raise NotImplementedError(f'Cannot divide {self.__class__.__name__} with different temps.')
            return self.__class__(self.temps[:], self.heat_flows/other.heat_flows, f'{self.name} / {other.name}')
        return self.__class__(self.temps[:], self.heat_flows/other, f'{self.name}')

    def __rmul__(self, other):
        return self.__mul__(other)

    def __mul__(self, other):
        """
        Multiply Scan heat_flows by another Scan heat_flows or value.
        """
        if type(self) == type(other):
            if self.temps.shape != other.temps.shape:
                raise NotImplementedError(f'Cannot multiply {self.__class__.__name__} with different shapes.')
            elif any(self.temps != other.temps):
                raise NotImplementedError(f'Cannot multiply {self.__class__.__name__} with different temps.')
            return self.__class__(self.temps[:], self.heat_flows * other.heat_flows, f'{self.name} * {other.name}')
        return self.__class__(self.temps[:], self.heat_flows * other, f'{self.name}')

    def _heat_flows(self, temp, temp2=None):
        """
        Directly access the heat_flow-value(s) at temp to temp2.

        :param temp: temp-value at which to evaluate (or start).
        :param temp2: temp-value at which to end, if None, only the value at temp is returned.
        :return: heat_flow or np.array of heat_flows
        """
        if temp2 is None:
            return y_at_x(temp, self.temps, self.heat_flows)
        return self.heat_flows[index_of_x(temp, self.temps):index_of_x(temp2, self.temps)]

    def copy(self):
        """
        Create a copy of the Scan.

        :return: duplicate Scan
        """
        return self.__class__(self.temps[:], self.heat_flows[:], f'{self.name}')

    @property
    def min(self):
        """
        Determine the min heat_flow and coordinate temp.

        :return: temp, min_heat_flow
        """
        min_idx = np.argmin(self.heat_flows)
        return self.temps[min_idx], self.heat_flows[min_idx]

    @property
    def max(self):
        """
        Determine the max heat_flow and coordinate temp.

        :return: temp, max_heat_flow
        """
        max_idx = np.argmax(self.heat_flows)
        return self.temps[max_idx], self.heat_flows[max_idx]

    @property
    def domain(self):
        """
        Domain of the Scan (range of temp-values).

        :return: first temp, last temp
        """
        return min(self.temps), max(self.temps)

    def correlation(self, other):
        """
        Determine the correlation between two Scans.

        :return: correlation score in [-1, 1]
        """
        if len(self.temps) != len(other.temps) or any(self.temps != other.temps):
            raise NotImplementedError('Cannot determine the correlation of Scan with different temp-values.')

        return sum(self.heat_flows * other.heat_flows)/(self.norm*other.norm)

    def smoothed(self, box_pts=True):
        """
        Return a smoothed version of the Scan.

        :param box_pts: number of data points to convolve, if True, use 3
        :return: smoothed Scan
        """
        return self.__class__(self.temps[:], smooth_curve(self.heat_flows, box_pts), f'{self.name}')

    def baseline_subtracted(self, val=None):
        """
        Return a new Scan with the baseline heat_flow subtracted.

        :param val: amount to subtract, if None, use the lowest value
        :return: Scan with the baseline heat_flow subtracted
        """
        if val is None:
            val = self.heat_flows.min()
        return self.__class__(self.temps[:], self.heat_flows - val, f'{self.name}')

    def set_zero(self, temp, temp2=None):
        """
        Set temp (or range of temps) at which heat_flow (or heat_flow average) is set to 0.

        :param temp: value at which heat_flow is set to zero
        :param temp2: end of range (unless None)
        :return: zeroed Scan
        """
        if temp2 is None:
            delta = self._heat_flows(temp)
        else:
            delta = np.mean(self._heat_flows(temp, temp2))

        return self.baseline_subtracted(delta)

    def sliced(self, start=None, end=None):
        """
        Return a new Scan that is a slice of self.

        :param start: the start of the slice
        :param end: the end of the slice
        :return: a new Scan
        """
        temps, heat_flows = self.temps, self.heat_flows

        start_i = index_of_x(start, temps) if start is not None else None
        end_i = index_of_x(end, temps) if end is not None else None

        return self.__class__(temps[start_i:end_i], heat_flows[start_i:end_i], f'{self.name}')

    @property
    def norm(self):
        """
        Determine the Frobenius norm of the heat_flows.
        """
        return np.linalg.norm(self.heat_flows)

    def normed(self, target='area', target_value=1):
        """
        Return a normalized Scan.

        :param target:
            'area' - normalize using total area
            'max' - normalize based on max value
            temp-value - normalize based on the heat_flow-value at this temp-value
            (start, end) - normalize based on integration from start to end
        :param target_value: what to normalize the target to
        :return: normalized Scan
        """
        if target == 'area':
            norm = integrate(self.temps, self.heat_flows)
        elif target == 'max':
            norm = max(self.heat_flows)
        else:
            # if a number
            try:
                float(target)
            except TypeError:
                # if an iterable of length 2
                try:
                    a, b = target
                    a, b = float(a), float(b)
                except ValueError:
                    raise ValueError(f'Could not normalize a Scan with target={target}.')
                else:
                    norm = integrate(self.temps, self.heat_flows, target)
            else:
                norm = self._heat_flows(target)

        return self.__class__(self.temps[:], self.heat_flows/norm*target_value, f'{self.name}')

    def peaks(self, indices=False, height=None, threshold=None, distance=None, prominence=None, width=None, wlen=None,
              rel_height=0.5, plateau_size=None):
        """
        Find the indices of peaks.

        Note: Utilizes scipy.signal.find_peaks and the parameters therein.

        :param indices: return peak indices instead of temp-values
        :return: peak temp-values (or peak indices if indices == True), properties
        """
        peaks, properties = signal.find_peaks(
            self.heat_flows, height, threshold, distance, prominence,
            width, wlen, rel_height, plateau_size
        )

        if indices:
            return peaks, properties

        return self.temps[peaks], properties


def scans_from_csvs(*inps, names=None):
    """
    Read from csvs.

    :param inps: file names of the csvs
    :param names: names of the Scans
    :return: list of Scans
    """
    ns, temp_vals, heat_flow_vals = read_csvs(inps)
    names = ns if names is None else names
    return [Scan(*vals) for vals in zip(temp_vals, heat_flow_vals, names)]
