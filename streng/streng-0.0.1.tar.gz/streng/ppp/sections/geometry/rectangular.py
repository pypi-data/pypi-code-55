from dataclasses import dataclass, field
from streng.common.io.output import OutputTable

@dataclass
class RectangularSectionGeometry:
    b: float
    h: float

    _area: float = field(init=False, repr=False)

    def __post_init__(self):
        self.calc()

    def calc(self):
        self._area = self.b * self.h

    @property
    def area(self) -> float:
        return self._area

    @property
    def moment_of_inertia_yy(self) -> float:
        return self.b ** 3 * self.h / 12

    @property
    def moment_of_inertia_xx(self) -> float:
        return self.h ** 3 * self.b / 12

    @property
    def torsional_constant(self) -> float:
        return self.b ** 3 * self.h * (1 / 3 - 0.21 * self.b / self.h * (1 - self.b ** 4 / (12 * self.h ** 4)))

    @property
    def shear_area_2(self) -> float:
        return 5 / 6 * self._area

    @property
    def shear_area_3(self) -> float:
        return 5 / 6 * self._area

    @property
    def section_modulus_2(self) -> float:
        return self.b ** 2 * self.h / 6

    @property
    def section_modulus_3(self) -> float:
        return self.h ** 2 * self.b / 6

    @property
    def plastic_modulus_2(self) -> float:
        return self.b ** 2 * self.h / 4

    @property
    def plastic_modulus_3(self) -> float:
        return self.h ** 2 * self.b / 4

    @property
    def radius_of_gyration_2(self) -> float:
        return self.b / 12 ** 0.5

    @property
    def radius_of_gyration_3(self) -> float:
        return self.h / 12 ** 0.5

    @property
    def x_g(self) -> float:
        return self.b / 2

    @property
    def y_g(self) -> float:
        return self.h / 2

    @property
    def all_quantities(self):
        out = OutputTable()
        out.data.append({'quantity': 'b', 'value': self.b})
        out.data.append({'quantity': 'h', 'value': self.h})
        out.data.append({'quantity': 'area', 'value': self.area})
        out.data.append({'quantity': 'Iyy', 'value': self.moment_of_inertia_yy})
        out.data.append({'quantity': 'Ixx', 'value': self.moment_of_inertia_xx})
        out.data.append({'quantity': 'J', 'value': self.torsional_constant})
        out.data.append({'quantity': 'ShearArea2', 'value': self.shear_area_2})
        out.data.append({'quantity': 'ShearArea3', 'value': self.shear_area_3})
        out.data.append({'quantity': 'SectionModulus2', 'value': self.section_modulus_2})
        out.data.append({'quantity': 'SectionModulus3', 'value': self.section_modulus_3})
        out.data.append({'quantity': 'PlasticModulus2', 'value': self.plastic_modulus_2})
        out.data.append({'quantity': 'PlasticModulus3', 'value': self.plastic_modulus_3})
        out.data.append({'quantity': 'RadiusOfGyration2', 'value': self.radius_of_gyration_2})
        out.data.append({'quantity': 'RadiusOfGyration3', 'value': self.radius_of_gyration_3})
        out.data.append({'quantity': 'xG', 'value': self.x_g})
        out.data.append({'quantity': 'yG', 'value': self.y_g})
        return out

