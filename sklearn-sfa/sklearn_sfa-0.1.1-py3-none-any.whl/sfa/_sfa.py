"""
This is a module to be used as a reference for building other modules
"""
import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin, TransformerMixin
from sklearn.decomposition import PCA, IncrementalPCA
from sklearn.utils.validation import check_array
from scipy.sparse import issparse
from sklearn.utils.multiclass import unique_labels
from sklearn.metrics import euclidean_distances

class SFA(TransformerMixin, BaseEstimator):
    """ Slow Feature Analysis (SFA)

    Linear dimensionality reduction and feature extraction method to be trained
    on time-series data. The data is decorrelated by whitening and linearly
    projected into the most slowly changing subspace. Slowness is measured by the
    average of squared one-step differences - thus, the most slowly changing subspace
    corresponds to the directions with minimum variance for the dataset of one-step
    differences and can be found using PCA.

    After training, the reduction can be applied to non-ordered data as well.

    For more information on SFA, read :ref:`User Guide <SFA>`.

    Parameters
    ----------
    n_components : int, None
        Number of slow features to extract.

    copy : bool, default=True
        If False, data passed to fit are overwritten and running
        fit(X).transform(X) will not yield the expected results,
        use fit_transform(X) instead.

    use_generalised_eigenproblem : bool, default=False
        If True, an alternative training method based on solving a
        generalised eigenproblem is used.

    svd_solver : str {'auto', 'full', 'arpack', 'randomized'}
        If auto :
            The solver is selected by a default policy based on `X.shape` and
            `n_components`: if the input data is larger than 500x500 and the
            number of components to extract is lower than 80% of the smallest
            dimension of the data, then the more efficient 'randomized'
            method is enabled. Otherwise the exact full SVD is computed and
            optionally truncated afterwards.
        If full :
            run exact full SVD calling the standard LAPACK solver via
            `scipy.linalg.svd` and select the components by postprocessing
        If arpack :
            run SVD truncated to n_components calling ARPACK solver via
            `scipy.sparse.linalg.svds`. It requires strictly
            0 < n_components < min(X.shape)
        If randomized :
            run randomized SVD by the method of Halko et al.
        For more information, refer to *PCA.
        This parameter is shared for whitening as well as optimization in when
        training SFA.

    tol : float >= 0, optional (default .0)
        Tolerance for singular values computed by svd_solver == 'arpack'.

    iterated_power : int >= 0, or 'auto', (default 'auto')
        Number of iterations for the power method computed by
        svd_solver == 'randomized'.

    random_state : int, RandomState instance, default=None
        Used when ``svd_solver`` == 'arpack' or 'randomized'. Pass an int
        for reproducible results across multiple function calls.

    Examples
    --------
    >>> from sklearn_sfa import SFA
    >>> import numpy as np
    >>> t = np.linspace(0, 8*np.pi, 1000).reshape(1000, 1)
    >>> t = t * np.arange(1, 5)
    >>> ordered_cosines = np.cos(t)
    >>> mixed_cosines = np.dot(ordered_cosines, np.random.normal(0, 1, (5, 5)))
    >>> sfa = SFA(n_components=2)
    >>> unmixed_cosines = sfa.fit_transform(mixed_cosines)
    >>> print(f"The average squared differences (delta values) of your slow feature extractor: {sfa.d}")
    """
    def __init__(self, n_components, copy=True, use_generalised_eigenproblem=False, svd_solver="auto", tol=.0, iterated_power="auto", random_state=None):
        self.n_components = n_components
        if self.n_components < 1:
            raise ValueError(f"n_components={self.n_components} must be at least 1")
        self.copy = copy
        self.svd_solver = svd_solver
        self.tol = tol
        self.use_generalised_eigenproblem = use_generalised_eigenproblem
        # initialize internal pca methods
        if not use_generalised_eigenproblem:
            self.pca_whiten = PCA(svd_solver=svd_solver, tol=tol, whiten=True)
            self.pca_diff = IncrementalPCA()
        self.d = None

    def fit(self, X, y=None):
        """Fit the model to X

        Parameters
        ----------
        X : {array-like}, shape (n_samples, n_features)
            The training input samples.

        y : None or {array-like}, shape (n_samples, 1)
            Mask that marks the start of a new time series after a non-connected step. 
        Returns
        -------
        self : object
            Returns self.
        """
        if y is None:
            y = np.zeros(X.shape[0], dtype=bool)
            #y[0] = True
        if issparse(X):
            raise TypeError('SFA does not support sparse input.')
        X = check_array(X, dtype=[np.float64, np.float32], ensure_2d=True, copy=self.copy)
        if (X.shape[1] < self.n_components):
            raise ValueError(f"n_components={self.n_components} must be between 1 and n_features={X.shape[1]}")
        self._fit(X, y)
        self.is_fitted_ = True
        return self

    def _fit(self, X, y):
        """Fit the model to X either by using minor component extraction
        on the difference time-series of the whitened data or by solving
        a generalised eigenvalue problem.

        Parameters
        ----------
        X : {array-like}, shape (n_samples, n_features)
            The training input samples.
        """
        if self.use_generalised_eigenproblem:
            self._fit_generalised_eigenproblem(X, y)
        else:
            self._fit_standard_method(X, y)

    def _fit_generalised_eigenproblem(self, X):
        """Fit the model to X by solving the associated generalised
        eigenproblem.

        Parameters
        ----------
        X : {array-like}, shape (n_samples, n_features)
            The training input samples.
        """
        pass

    def _fit_standard_method(self, X, y):
        """ Fit the model to X either by first whitening the data, calculating
        the one-step differences and then extract minor components of the latter.

        Parameters
        ----------
        X : {array-like}, shape (n_samples, n_features)
            The training input samples.
        """
        self.pca_whiten.fit(X)
        X_whitened = self.pca_whiten.transform(X)
        X_diff = X_whitened[1:] - X_whitened[:-1]
        split_indices = np.argwhere(y)
        if split_indices.size != 0:
            last_start = 0
            for split_index in split_indices:
                current_batch = X_whitened[last_start:split_index[0]]
                if not current_batch.shape[0] < 2:
                    batch_diff = current_batch[1:] - current_batch[:-1]
                    self.pca_diff.partial_fit(batch_diff)
                last_start = split_index[0]
        else:
            self.pca_diff.fit(X_diff)
        # estimate delta values from training data
        X_out = self.pca_diff.transform(X_diff)[:, -self.n_components:][:, ::-1]
        self.d = X_out.var(axis=0)

    def transform(self, X):
        """ Use the trained model to apply dimensionality reduction to X.
        First, it is whitened using a trained PCA model. Afterwards, it
        is projected onto the previously extracted slow subspace using a
        second trained PCA model.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape (n_samples, n_features)
            The samples to be transformed.

        Returns
        -------
        y : ndarray, shape (n_samples, n_components)
            The slow features extracted from X.
        """
        X = check_array(X, dtype=[np.float64, np.float32], ensure_2d=True, copy=self.copy)
        y = self.pca_whiten.transform(X)
        y = self.pca_diff.transform(y)
        y = y[:, -self.n_components:][:, ::-1]
        return y


