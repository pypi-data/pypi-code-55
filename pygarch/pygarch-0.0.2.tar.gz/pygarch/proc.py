import pkg_resources
from typing import Optional

import pandas as pd
from rpy2.robjects import pandas2ri
from rpy2.rinterface import RRuntimeError, NULL
from rpy2.robjects.packages import (
    importr,
    SignatureTranslatedAnonymousPackage as STAPkg
)

from .spec import ArmaGarchSpec
from .exceptions import ArmaGarchException


class ArmaGarchProcess:
    """
     A time series model with means modelled as an ARMA process and
     volatilities modelled as a GARCH process

     This class wraps a limited subset of the R package rugarch.
     See ArmaGarchSpec for details on how to set the spec
    """

    r_lib = None

    def __new__(cls, *args, **kwargs):
        """ import the R library functions """
        if not cls.r_lib:
            importr('rugarch')
            src = pkg_resources.resource_filename('pygarch', 'lib/fit.R')
            with open(src, 'r') as script:
                cls.r_lib = STAPkg(script.read(), 'r_lib')
        return super().__new__(cls)

    def __init__(self, series: pd.Series,
                 arma_order: tuple = (1, 1),
                 garch_order: tuple = (1, 1),
                 dist: str = "std"):
        if series.empty:
            raise ValueError('series is empty!')

        self.spec = ArmaGarchSpec(arma_order, garch_order, dist=dist)

        # internal
        self._index = series.index
        self._model_converged = False

        # r objects
        pandas2ri.activate()
        self._r_series = pandas2ri.py2ri(series)
        self._r_model = None

    def __str__(self):
        return (f"<ARMA{self.spec.arma_order}-GARCH{self.spec.garch_order} "
                f"Process at {hex(id(self))}>")

    def fit(self) -> bool:
        """ fit an ARMA-GARCH model to the series """
        try:
            res = ArmaGarchProcess.r_lib.fit_model(self._r_series, self.spec.as_r_obj())
            self._r_model, converged = res
            self._model_converged = converged[0]
        except RRuntimeError:
            self._model_converged = False
        return self._model_converged

    @property
    def converged(self) -> bool:
        return self._model_converged

    def simulate(self,
                 len_sim: int,
                 num_sims: int,
                 external_regressors: Optional[pd.DataFrame] = None
                 ) -> pd.DataFrame:
        """
         Generate simulations from the ARMA-GARCH model starting from the
         period following the end date of the fitting-period
        """
        if (self._r_model is None) or (not self.converged):
            raise ArmaGarchException(
                "cannot simulate: model has not been fit or has not converged"
            )

        extr_fit = self.spec.external_regressors  # fitted on
        extr_sim = external_regressors            # to simulate on
        if isinstance(extr_sim, pd.Series):
            extr_sim = extr_sim.to_frame()

        if not extr_fit.empty and (extr_sim is None):
            raise ValueError(
                "cannot simulate: must supply simulations of external regressors"
            )

        elif extr_fit.empty and (extr_sim is not None):
            raise ValueError(
                "cannot simulate: model was not fit with external_regressors"
            )

        elif not extr_fit.empty and (extr_sim is not None):
            if extr_sim.shape != (len_sim, extr_sim.shape[1]):
                raise ValueError(
                    f"external_regressors is wrong dimension. It must be "
                    f"of size (len_sim, N)=({len_sim}, {extr_sim.shape[1]})"
                )

        if extr_sim is None:
            extr_sim = NULL

        sims = ArmaGarchProcess.r_lib.simulate_model(
            self._r_model, len_sim, num_sims, extr_sim
        )
        # TODO: update this when we update pandas
        return pd.DataFrame(pandas2ri.ri2py_vector(sims))

    @property
    def aic(self) -> float:
        """ return the Akaike Information Criteria """
        if self.converged:
            return ArmaGarchProcess.r_lib.calc_aic(self._r_model, self._r_series)[0]
        else:
            raise ArmaGarchException("model has not been fit or has not converged")

    @property
    def summary(self) -> str:
        """ return the summary of the model fit """
        if self.converged:
            rvec = ArmaGarchProcess.r_lib.get_model_summary(self._r_model)
            return '\n'.join(tuple(rvec))
        else:
            raise ArmaGarchException("model has not been fit or has not converged")

    @property
    def residuals(self) -> Optional[pd.Series]:
        """ return the residuals from the mean model """
        if self.converged:
            ret = ArmaGarchProcess.r_lib.get_residuals(self._r_model)
            return pd.Series(pandas2ri.ri2py(ret).ravel(), index=self._index)
        else:
            return None

    @property
    def fitted_values(self) -> Optional[pd.Series]:
        """ return the fitted values from the mean model """
        if self.converged:
            ret = ArmaGarchProcess.r_lib.get_fitted_values(self._r_model)
            return pd.Series(pandas2ri.ri2py(ret).ravel(), index=self._index)
        else:
            return None

    @property
    def volatilities(self) -> Optional[pd.Series]:
        """ return the fitted volatilities from the GARCH component on the model """
        if self.converged:
            ret = ArmaGarchProcess.r_lib.get_volatilities(self._r_model)
            return pd.Series(pandas2ri.ri2py(ret).ravel(), index=self._index)
        else:
            return None
