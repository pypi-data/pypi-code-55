from dataclasses import dataclass, field
from typing import List

from .areas import As_layer

@dataclass
class LongReinforcementLayer:
    ns: List[float]# = field(default_factory=list)
    dias: List[float]# = field(default_factory=list)

    @classmethod
    def from_string(cls, reinf_string, units_input='mm', units_output='mm', dia_symbol = 'Φ'):
        # Πχ reinf_string='2Φ18+2Φ16'

        # Μετατρέπω σε mm (συνηθέστερο) για να γίνουν οι πράξεις
        if units_input == 'm':
            length_multiplier_input = 1000.
        elif units_input == 'cm':
            length_multiplier_input = 10.
        else:
            length_multiplier_input = 1.

        ns_and_dias = [x.split(dia_symbol) for x in reinf_string.split('+')]
        ns = [float(y[0]) for y in ns_and_dias]
        dias = [float(y[1]) * length_multiplier_input for y in ns_and_dias]

        if units_output == 'm':
            length_multiplier_output = 0.001
        elif units_output == 'cm':
            length_multiplier_output = 0.1
        else:
            length_multiplier_output = 1.0

        return cls(ns, [d*length_multiplier_output for d in dias])

    @property
    def As(self):
        return As_layer(self.ns, self.dias)

    @property
    def ntot(self):
        return sum(self.ns)

    @property
    def dia_max(self):
        return max(self.dias)

    @property
    def dia_min(self):
        return min(self.dias)




@dataclass
class TransReinforcementLayer:
    n: int
    dia: float
    s: float

    @classmethod
    def from_string(cls, reinf_string, units_input='mm', units_output='mm', dia_symbol = 'Φ'):
        # Πχ reinf_string='Φ8/140(3)'

        # Μετατρέπω σε mm (συνηθέστερο) για να γίνουν οι πράξεις
        if units_input == 'm':
            length_multiplier_input = 1000.
        elif units_input == 'cm':
            length_multiplier_input = 10.
        else:
            length_multiplier_input = 1.

        n = int(reinf_string[reinf_string.find("(")+1:reinf_string.find(")")])
        dia = float(reinf_string[reinf_string.find(dia_symbol)+1:reinf_string.find("/")]) * length_multiplier_input
        s = float(reinf_string[reinf_string.find("/")+1:reinf_string.find("(")]) * length_multiplier_input


        if units_output == 'm':
            length_multiplier_output = 0.001
        elif units_output == 'cm':
            length_multiplier_output = 0.1
        else:
            length_multiplier_output = 1.0

        return cls(n, dia * length_multiplier_output, s * length_multiplier_output)

    @property
    def As(self):
        return As_layer(self.n, self.dia)