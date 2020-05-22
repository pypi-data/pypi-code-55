#  C O N S T R U C T I V I S T__ __
#   _____ ____   ____   /  |/  // /
#  / ___// __ \ / __ \ / /|_/ // /
# / /__ / /_/ // / / // /  / // /___
# \___/ \____//_/ /_//_/  /_//_____/
#  M A C H I N E   L E A R N I N G
#
#
# A Project by
# Thomas Schmid | UNIVERSITÄT LEIPZIG
# www.constructivist.ml
#
# Code Author: Dmitrij Denisenko
# Licence: MIT


"""Defines adapters for machine machine algorithms of scikit-learn.

"""


from copy import deepcopy
from collections import Counter
import warnings

from sklearn.cluster import KMeans
from sklearn.cluster import Birch
from sklearn.cluster import SpectralClustering
from sklearn.cluster import DBSCAN
from sklearn.cluster import OPTICS
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import MeanShift
from scipy.stats import gaussian_kde
from numpy import random


CLUSTERING_SPECIFIC = {
    KMeans: True,
    DBSCAN: False,
    SpectralClustering: True,
    AgglomerativeClustering: True,
    AffinityPropagation: False,
    MeanShift: False,
    OPTICS: False,
    Birch: True,
}


class MachineLearningModel:
    """Base class for all machine learning models.

    """

    def train(self, data, *args, **kwargs):
        raise NotImplementedError


class FilterMethod(MachineLearningModel):
    """Responsible for encapsulating filter methods.

    Filter methods are used during the feature selection process.

    Args:
        model: Scikit-learn filter method.

    """

    def __init__(self, model):
        self.model = model

    def __str__(self):
        return "Filtermethod: {}".format(str(self.model))

    def __repr__(self):
        return "FilterMethod({})".format(repr(self.model))

    def train(self, data, *args, **kwargs):
        """Train the filter method on given data set.

        Args:
            data (PandasBlock): Learnblock.

        """
        labels = data.get_column("Z")
        self.model = self.model.fit(data.df.iloc[:, :-3], y=labels)

    def reduce(self, data):
        """Determine features that can be savely removed.

        Args:
            data (PandasBlock): Learnblock.

        Returns:
            set:
                Features that do not contribute much to the label.

        """
        supported_indices = set(self.model.get_support(indices=True))
        features_indices = {i for i in range(data.n_columns(effective=True))}
        return features_indices.difference(supported_indices)


class EmbeddedMethod(MachineLearningModel):
    """Resposible for encapsulating embedded methods.

    Args:
        model: Scikit-learn embedded method.

    """
    _ONE_HUNDRET_PERCENT = 100

    def __init__(self, model):
        self.model = model

    def __str__(self):
        return "EmbeddedMethod: {}".format(str(self.model))

    def __repr__(self):
        return "EmbeddedMethod({})".format(repr(self.model))

    def train(self, data, *args, **kwargs):
        """Train the embedded method on given data set.

        Args:
            data (PandasBlock): Learnblock.

        """
        labels = data.get_column("Z")
        self.model = self.model.fit(data.df.iloc[:, :-3], labels)

    def reduce(self, data):
        """Determine features that can be savely removed from the given
        learnblock.

        Args:
            data (PandasBlock):  Learnblock.

        Returns:
            set:
                Features that do not contribute much to the label.

        """
        supported_indices = set(self.model.get_support(indices=True))
        features_indices = {i for i in range(data.n_columns(effective=True))}
        return features_indices.difference(supported_indices)


class ConstructionClusteringMLModel(MachineLearningModel):
    """Responsible for encapsulating unsupervised machine learning
    models from scitkit-learn.

    Args:
        model: Unsupervised machine learning model from scikit-learn.
        abbreviation (str): Subject identifier.

    """
    def __init__(self, model, abbreviation):
        self.model = model
        self.abbreviation = abbreviation
        self._cluster = None

    def __str__(self):
        return "\n".join([
                "{}: {}".format("Model", str(self.model)),
                "{}: {}".format("Abbreviation", str(self.abbreviation)),
           ]
        )

    def __repr__(self):
        return ",".join([
                "{}={}".format("Model", repr(self.model)),
                "{}={}".format("Abbreviation", str(self.abbreviation)),
                "{}={}".format("Cluster", str(self._cluster))
            ]
        )

    def new_model_depending_on_cluster(self, n_cluster):
        """Factory method for creating ConstructionClusteringMLModel
        with a specific cluster number.

        Args:
            n_cluster (int): Number of cluster that the unsupervised
                machine learning model should find.

        Returns:
            ConstructionClusteringMLModel

        """
        new_model = deepcopy(self)
        new_model._cluster = n_cluster
        new_model.model.n_clusters = n_cluster
        return new_model

    def new_model(self):
        """Create a deep copy of itself.

        Returns:
              ConstructionClusteringMLModel

        """
        return deepcopy(self)

    def get_labels(self):
        """Return found labels

        Returns:
            numpy.ndarray

        """
        return self.model.labels_

    @property
    def cluster_specific(self):
        """Check if the used unsupervised machine learning model needs
        a cluster specification.

        Returns:
            bool:
                True, if the number of cluster that needs to be found
                should be specified by the user.

        """
        return CLUSTERING_SPECIFIC[type(self.model)]

    @property
    def found_cluster(self):
        """Number of found clusters.

        Returns:
            int

        """
        return len(set(self.model.labels_))

    @property
    def cluster(self):
        return self._cluster

    @cluster.setter
    def cluster(self, value):
        self.model.n_clusters = value
        self._cluster = value

    @property
    def cluster_sizes(self):
        return Counter(self.model.labels_)

    def train(self, data, *args, **kwargs):
        """Train the unsupervised machine learning model on the given learnblock.

        Args:
            data (PandasBlock): Learnblock.

        """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.model.fit(data)


class ReconstructionConceptualMLModel(MachineLearningModel):
    """Responsible for encapsulating supervised machine learning
    models from scitkit-learn.

    Args:
        model: Supervised machine learning model from scikit-learn.
        abbreviation (str): Subject identifier.

    Attributes:
        accuracy (float): Prediction accuracy on test data.

    """

    def __init__(self, model, abbreviation):
        self.model = model
        self.subject = abbreviation
        self.accuracy = None

    def train(self, data, *args, **kwargs):
        """Train the supervised machine learning model on the given data set.

        Args:
            data (numpy.ndarray): Training data.

        Returns:
            ReconstructionConceptualMLModel

        """
        labels = args[0]
        model = self.model.fit(data, labels)
        recon_model = deepcopy(self)
        copy_model = deepcopy(model)
        recon_model.model = copy_model
        return recon_model

    def score(self, data, labels):
        """Calculate the accuracy on the given data set.

        Args:
            data (numpy.ndarray): Data set.
            labels (list): True labels for the data set.

        Returns:
            float:
                Accuracy.

        """
        return round(self.model.score(data, labels), 3)

    def predict(self, data):
        """Predict the labels for the given data set.

        Args:
            data (numpy.ndarray): Data set.

        Returns:
            list:
                Predicted labels for the given data set.

        """
        return [i for i in self.model.predict(data)]


class KernelDensityEstimator:

    def __init__(self):
        """Responsible for encapsulating  kernel density estimation
        algorithms from scikit-learn.

        """
        self.model = gaussian_kde

    def density(self, data):
        """Calculate the density of the given data.

        Args:
            data (list): List with time stamps.

        Returns:
            list:
                List of floats representing the denisty values.

        """
        return gaussian_kde(data)(data)
