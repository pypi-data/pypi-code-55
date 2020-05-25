from typing import Dict, List
import numpy as np
from sklearn.metrics import r2_score


def get_model_metrics(A: np.ndarray,
                      parameters: List[float],
                      y_target: np.ndarray,
                      y_predicted: np.ndarray) -> Dict[str, float]:
    """Computes model parameters and model evaluation metrics including
    * root-mean square-error (RMSE) over training set
    * R^2 score over training set (coefficient of determination, regression score function)
    * Akaike information criterion (AIC)
    * Bayesian information criterion (BIC)
    * leave-one-out cross-validation (LOO-CV, estimate)
    * number of non-zero parameters (n_nzp)
    * number of parameters (n_parameters)

    Parameters
    ----------
    A
        fit matrix used to train model
    parameters
        model parameters
    y_target
        target values used to train model
    y_predicted
        predicted values from model
    """
    n_samples, n_parameters_tot = A.shape
    n_parameters = np.count_nonzero(parameters)

    # compute rmse
    delta_y = y_predicted - y_target
    mse = np.mean(delta_y**2)
    rmse = np.sqrt(mse)

    # evaluate Information Criterias
    aic = get_aic(mse, n_samples, n_parameters)
    bic = get_bic(mse, n_samples, n_parameters)

    # r2 score
    r2 = r2_score(y_target, y_predicted)

    # summarize
    metrics = dict(rmse_train=rmse,
                   R2_train=r2,
                   AIC=aic,
                   BIC=bic,
                   n_nonzero_parameters=n_parameters)
    return metrics


def get_aic(mse: float, n_samples: int, n_parameters: int) -> float:
    """Returns the Akaiki information criterion (AIC)."""
    aic = n_samples * np.log(mse) + 2 * n_parameters
    return aic


def get_bic(mse: float, n_samples: int, n_parameters: int) -> float:
    """Returns the Bayesian information criterion (BIC)."""
    bic = n_samples * np.log(mse) + n_parameters * np.log(n_samples)
    return bic


def estimate_loocv(A: np.ndarray,
                   y_target: np.ndarray,
                   y_predicted: np.ndarray) -> float:
    """Calculates the approximative leave-one-out cross-validation
    (LOO-CV) root mean square error (RMSE).

    Parameters
    ----------
    A
        Matrix in OLS problem y=Ax, should be inversible
    y_target
        Target values for y
    y_predicted
        OLS obtained prediction for y
    """
    if len(A[1, :]) > len(A[:, 1]):
        raise ValueError('Matrix is underdetermined')

    H = A.dot(np.linalg.inv(A.T.dot(A))).dot(A.T)
    e = (y_target - y_predicted) / (1 - np.diag(H))

    return np.linalg.norm(e) / np.sqrt(len(e))
