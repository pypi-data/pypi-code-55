import numpy as np
from dataclasses import dataclass

from ...raw.ch3.seismic_action import spectra as spec_raw


@dataclass
class SpectraEc8:
    """Eurocode 8 response spectra

    .. note::
        If αgR values are given in g, displacements and velocities should be multiplied with 9.81

    .. uml::

        class SpectraEc8 {
        .. attributes ..
        + αgR (float)
        + γI (float)
        + ground_type (str)
        + spectrum_type (int)
        + η (float)
        + q (float)
        + β (float)
        .. properties ..
        + dg()
        + getAllSpectra0to4()
        .. methods ..
        + Se(T) (float)
        + SDe(T) (float)
        + Sd(T) (float)
        }

    Attributes:
        αgR (float): reference peak ground acceleration on type A ground
        γI (float): importance factor
        ground_type (str): Ground type (A, B, C, D or E)
        spectrum_type (int): Spectrum type 1 or 2
        η (float): value of the damping correction factor
        q (float): behaviour factor
        β (float): lower bound factor for the horizontal design spectrum. Recommended value for β is 0.2

    """
    αgR: float
    γI: float
    ground_type: str
    spectrum_type: int
    η: float = 1.0
    q: float = 1.0
    β: float = 0.2

    def __post_init__(self):
        self.αg = self.γI * self.αgR
        self.S = spec_raw.S(ground_type=self.ground_type, spectrum_type=self.spectrum_type)
        self.TB = spec_raw.TB(ground_type=self.ground_type, spectrum_type=self.spectrum_type)
        self.TC = spec_raw.TC(ground_type=self.ground_type, spectrum_type=self.spectrum_type)
        self.TD = spec_raw.TD(ground_type=self.ground_type, spectrum_type=self.spectrum_type)

    def Se(self, T):
        """
        Args:
            T(float): Period

        Returns:
            float: The elastic acceleration response spectrum

        """
        return spec_raw.Se(T, self.αg, self.S, self.TB, self.TC, self.TD, self.η)

    def SDe(self, T):
        """
        Args:
            T(float): Period

        Returns:
            float: The elastic displacement response spectrum

        """
        return spec_raw.SDe(T, self.Se(T))

    @property
    def dg(self):
        """float: Design ground displacement"""
        return spec_raw.dg(self.αg, self.S, self.TC, self.TD)

    def Sd(self, T):
        """
        Args:
            T(float): Period

        Returns:
            float: Design spectrum for elastic analyses

        """
        return spec_raw.Sd(T, self.αg, self.S, self.TB, self.TC, self.TD, self.q, self.β)

    @property
    def getAllSpectra0to4(self):
        """ dict: A dictionary of numpy arrays with spectral values in the range 0-4sec"""
        _T_range = np.linspace(0.01, 4, 400)

        _Se = self.Se(_T_range)
        _SDe = self.SDe(_T_range)
        _Sv = _Se / (2 * np.pi / _T_range)
        _Sd = self.Sd(_T_range)

        _T_range = np.append(0., _T_range)
        _Se = np.append(self.αg * self.S, _Se)
        _SDe = np.append(0., _SDe)
        _Sv = np.append(0., _Sv)
        _Sd = np.append(self.αg * self.S * 2.0 / 3.0, _Sd)

        _data = {'T': _T_range,
                 'Se': _Se,
                 'Sv': _Sv,
                 'SDe': _SDe,
                 'Sd': _Sd}

        return _data


class ExampleClass(object):
    """The summary line for a class docstring should fit on one line.

    If the class has public attributes, they may be documented here
    in an ``Attributes`` section and follow the same formatting as a
    function's ``Args`` section. Alternatively, attributes may be documented
    inline with the attribute's declaration (see __init__ method below).

    Properties created with the ``@property`` decorator should be documented
    in the property's getter method.

    Attributes:
        attr1 (str): Description of `attr1`.
        attr2 (:obj:`int`, optional): Description of `attr2`.

    """

    def __init__(self, param1, param2, param3):
        """Example of docstring on the __init__ method.

        The __init__ method may be documented in either the class level
        docstring, or as a docstring on the __init__ method itself.

        Either form is acceptable, but the two should not be mixed. Choose one
        convention to document the __init__ method and be consistent with it.

        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            param1 (str): Description of `param1`.
            param2 (:obj:`int`, optional): Description of `param2`. Multiple
                lines are supported.
            param3 (:obj:`list` of :obj:`str`): Description of `param3`.

        """
        self.attr1 = param1
        self.attr2 = param2
        self.attr3 = param3  #: Doc comment *inline* with attribute

        #: list of str: Doc comment *before* attribute, with type specified
        self.attr4 = ['attr4']

        self.attr5 = None
        """str: Docstring *after* attribute, with type specified."""

    @property
    def readonly_property(self):
        """str: Properties should be documented in their getter method."""
        return 'readonly_property'

    @property
    def readwrite_property(self):
        """:obj:`list` of :obj:`str`: Properties with both a getter and setter
        should only be documented in their getter method.

        If the setter method contains notable behavior, it should be
        mentioned here.
        """
        return ['readwrite_property']

    @readwrite_property.setter
    def readwrite_property(self, value):
        value

    def example_method(self, param1, param2):
        """Class methods are similar to regular functions.

        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            param1: The first parameter.
            param2: The second parameter.

        Returns:
            True if successful, False otherwise.

        """
        return True

    def __special__(self):
        """By default special members with docstrings are not included.

        Special members are any methods or attributes that start with and
        end with a double underscore. Any special member with a docstring
        will be included in the output, if
        ``napoleon_include_special_with_doc`` is set to True.

        This behavior can be enabled by changing the following setting in
        Sphinx's conf.py::

            napoleon_include_special_with_doc = True

        """
        pass

    def __special_without_docstring__(self):
        pass

    def _private(self):
        """By default private members are not included.

        Private members are any methods or attributes that start with an
        underscore and are *not* special. By default they are not included
        in the output.

        This behavior can be changed such that private members *are* included
        by changing the following setting in Sphinx's conf.py::

            napoleon_include_private_with_doc = True

        """
        pass

    def _private_without_docstring(self):
        pass
