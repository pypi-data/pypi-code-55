import pkg_resources
from typing import Optional

import pandas as pd
from rpy2 import rinterface
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import (
    importr,
    SignatureTranslatedAnonymousPackage as STAPkg
)


class ArmaGarchSpec:
    """
     A limited wrapper to the R objects rugarch::ugarchspec

     Usage:
       arma_order -> tuple [default=(1,1)] :
           the number of autoregressive and moving average terms respectively
           in the ARMA process (of the means)
       garch_order -> tuple [default=(1,1)] :
           the number of volatility terms and (ARCH) error terms respectively
           in the GARCH process (of the volatilities)
       external_regressors -> pandas.DataFrame (optional) :
           additional external regressors that predict the mean
       dist -> str ["norm", "std"] [default="norm"] :
           the error distribution. Gaussian (norm) or Student-t (std)
       dof -> int (optional) :
           the degrees of the freedom in the Student-t distribution. If not
           specified then it is fit
       fixed_ar -> tuple (optional) :
           a tuple of coefficients for the autoregressive terms of the ARMA
           model.
       fixed_ma -> tuple (optional) :
           a tuple of coefficients for the moving-average terms of the ARMA
           model.
       model_mean -> bool [default=True] :
           whether to model the mean in the ARMA process (like the intercept
           in a linear regression
    """

    r_lib = None

    def __new__(cls, *args, **kwargs):
        if not cls.r_lib:
            importr('rugarch')
            lib_path = pkg_resources.resource_filename('pygarch', 'lib/spec.R')
            with open(lib_path, 'r') as script:
                cls.r_lib = STAPkg(script.read(), 'r_lib')
        return super().__new__(cls)

    def __init__(self,
                 arma_order: tuple = (1, 1),
                 garch_order: tuple = (1, 1),
                 external_regressors: Optional[pd.DataFrame] = None,
                 dist: str = "norm",
                 dof: Optional[int] = None,
                 fixed_ar: Optional[tuple] = None,
                 fixed_ma: Optional[tuple] = None,
                 model_mean: bool = True):

        pandas2ri.activate()

        self.arma_order = arma_order
        self.garch_order = garch_order
        self.external_regressors = external_regressors
        self.dist = dist
        self.dof = dof
        self.fixed_ar = fixed_ar
        self.fixed_ma = fixed_ma
        self.model_mean = model_mean

    def as_r_obj(self):
        return ArmaGarchSpec.r_lib.create_spec(
            self._arma_order, self._garch_order,
            self._external_regressors, self._dist, self._dof,
            self._fixed_ar, self._fixed_ma, self.model_mean
        )

    @property
    def arma_order(self) -> tuple:
        return tuple(self._arma_order)

    @arma_order.setter
    def arma_order(self, order: tuple) -> None:
        if len(order) != 2:
            raise ValueError(
                'arma_order must be a tuple of length 2 that specifies the '
                'number of autoregressive and moving-average terms'
            )
        self._arma_order = rinterface.IntSexpVector(order)

    @property
    def garch_order(self) -> tuple:
        return tuple(self._garch_order)

    @garch_order.setter
    def garch_order(self, order: tuple) -> None:
        if len(order) != 2:
            raise ValueError(
                'garch_order must be a tuple of length 2 that specifies the '
                'number of volatility terms and error terms respectively'
            )
        self._garch_order = rinterface.IntSexpVector(order)

    @property
    def external_regressors(self) -> pd.DataFrame:
        if not self._external_regressors:
            return pd.DataFrame()
        else:
            # TODO: update this when we update pandas
            return pd.DataFrame(pandas2ri.ri2py_vector(self._external_regressors))

    @external_regressors.setter
    def external_regressors(self, frame: Optional[pd.DataFrame]) -> None:
        if frame is None:
            self._external_regressors = rinterface.NULL
        else:
            self._external_regressors = pandas2ri.py2ri(frame)

    @property
    def dist(self) -> str:
        return self._dist

    @dist.setter
    def dist(self, dist: str) -> None:
        if dist not in ("norm", "std"):
            raise ValueError("distribution must be 'norm' for Gaussian error or 'std' "
                             "for Student-t errors")
        self._dist = dist

    @property
    def dof(self) -> Optional[int]:
        return int(self._dof) if self._dof else None

    @dof.setter
    def dof(self, dof: Optional[int]) -> None:
        if dof is not None:
            if self.dist != "std":
                raise ValueError("degrees of freedom (dof) can only be set with "
                                 "the Student-t error distribution")
            elif dof <= 0:
                raise ValueError("degrees of freedom (dof) must be positive")

        self._dof = dof if (dof is not None) else rinterface.NULL

    @property
    def fixed_ar(self) -> Optional[tuple]:
        if not self._fixed_ar:
            return None
        return tuple(self._fixed_ar)

    @fixed_ar.setter
    def fixed_ar(self, coeffs: Optional[tuple]) -> None:
        if not coeffs:
            self._fixed_ar = rinterface.NULL
        elif len(coeffs) > self.arma_order[0]:
            raise ValueError(
                f"the fixed autoregressive coefficients cannot be longer than "
                f"the arma order, {self.arma_order[0]}"
            )
        else:
            self._fixed_ar = rinterface.IntSexpVector(coeffs)

    @property
    def fixed_ma(self) -> Optional[tuple]:
        if not self._fixed_ma:
            return None
        return tuple(self._fixed_ma)

    @fixed_ma.setter
    def fixed_ma(self, coeffs: Optional[tuple]) -> None:
        if not coeffs:
            self._fixed_ma = rinterface.NULL
        elif len(coeffs) > self.arma_order[1]:
            raise ValueError(
                f"the fixed autoregressive coefficients cannot be longer than "
                f"the arma order, {self.arma_order[1]}"
            )
        else:
            self._fixed_ma = rinterface.IntSexpVector(coeffs)
