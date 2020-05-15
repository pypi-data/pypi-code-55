from dataclasses import dataclass, field
from streng.common.io.output import OutputTable
from .rectangular import RectangularSectionGeometry as Rect


@dataclass
class TeeSectionGeometry:
    bw: float
    h: float
    beff: float
    hf: float

    _area: float = field(init=False, repr=False)
    _y_g: float = field(init=False, repr=False)
    _x_g: float = field(init=False, repr=False)


    def __post_init__(self):
        self.calc()

    def calc(self):
        self._area = self.bw * (self.h - self.hf) + self.beff * self.hf
        self._y_g = (1.0 / self._area) * ((self.bw * self.h ** 2 / 2.0) + ((self.beff - self.bw) * self.hf ** 2 / 2.0))
        self._x_g = self.beff / 2.0


    @property
    def area(self) -> float:
        return self._area

    @property
    def moment_of_inertia_yy(self) -> float:
        return (self.h - self.hf) * self.bw ** 3 / 12 + self.hf * self.beff ** 3 / 12

    @property
    def moment_of_inertia_xx(self) -> float:
        Ix0 = self.bw * self.h ** 3 / 3.0 + (self.beff - self.bw) * self.hf ** 3 / 3.0
        return Ix0 - self._area * self._y_g ** 2

    @property
    def x_g(self) -> float:
        return self._x_g

    @property
    def y_g(self) -> float:
        """Υπολογισμένο ξεκινώντας από την πλευρά της πλάκας.
        https://calcresource.com/cross-section-tee.html"""
        return self._y_g

    @property
    def torsional_constant(self) -> float:
        """Δεν το έχω υπολογίσει ακόμα...κρατώ αποτέλεσμα ορθογωνικής δοκού"""
        r = Rect(self.bw, self.h)
        return r.torsional_constant
        # return self.bw ** 3 * self.h * (1 / 3 - 0.21 * self.bw / self.h * (1 - self.bw ** 4 / (12 * self.h ** 4)))

    @property
    def shear_area_2(self) -> float:
        return self.bw * self.h

    @property
    def shear_area_3(self) -> float:
        return 5. / 6. * self.beff * self.hf

    @property
    def section_modulus_2(self) -> float:
        return self.moment_of_inertia_yy / self.x_g

    @property
    def section_modulus_3(self) -> float:
        return self.moment_of_inertia_xx / (self.h- self._y_g)

    @property
    def plastic_modulus_2(self) -> float:
        return (self.beff**2 * self.hf / 4.0) + ((self.h - self.hf)*self.bw**2)/4.0

    @property
    def plastic_modulus_3(self) -> float:
        """Δεν το έχω υπολογίσει ακόμα...κρατώ αποτέλεσμα ορθογωνικής δοκού"""
        r = Rect(self.bw, self.h)
        return r.plastic_modulus_3
        # _pm3 = 0
        # if self.y_g()>self.hf:
        #     _pm3 = 0
        # else:
        #     _pm3 = 0
        #
        # return _pm3

    @property
    def radius_of_gyration_2(self) -> float:
        return (self.moment_of_inertia_yy/self._area) ** 0.5

    @property
    def radius_of_gyration_3(self) -> float:
        return (self.moment_of_inertia_xx/self._area) ** 0.5


    @property
    def all_quantities(self):
        out = OutputTable()
        out.data.append({'quantity': 'bw', 'value': self.bw})
        out.data.append({'quantity': 'h', 'value': self.h})
        out.data.append({'quantity': 'beff', 'value': self.beff})
        out.data.append({'quantity': 'hf', 'value': self.hf})
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