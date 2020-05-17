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


"""Defines the construction process.

"""

from copy import deepcopy
from functools import partial

from conML.shared.logger import ConstructionInfo


def return_model(m):
    """Used to monkeypatch the machine_learning_models() method
    of a Constructor object.

    Args:
        m (ConstructionClusteringMLModel): A valid instantiated object.

    Yield:
        ConstructionClusteringMLModel:
            The only model used by the patched constructor.

    """
    yield m


class Constructor:
    """Encapsulates the construction procedure.


    Notes:
        Only conceptual mode is currently supported.

    Args:
        mode (str):
            Either 'conceptual' or 'procedural'.
        ml_models (list):
            A list with instantiated ConceptualClusteringMLModels.
        settings (ConstructionSettings):
            Instantiated object controlls the behavior of the Constructor.

    """
    def __init__(self, mode, ml_models, settings):
        self.mode = mode
        self.ml_models = ml_models
        self.settings = settings

    def __str__(self):
        return "\n".join([
            "{:20}: {}".format("Mode", str(self.mode)),
            "{:20}: {}".format("ML Models", [
                str(m) for m in self.ml_models]),
            str(self.settings),
            ]
        )

    def __repr__(self):
        return ", ".join([
            "{}={}".format("mode", str(self.mode)),
            "{}".format(repr(self.settings)),
            "{}={}".format("ml_models", repr(self.ml_models))
            ]
        )

    def construct(self, learnblock):
        """Main method for constructing a given learnblock.

        Args:
            learnblock (PandasBlock):
                Valid learnblock.

        Yields:
            tuple:
                A ConstructionInfo object containing information about
                the currently executed construction process regarding
                only one unsupervised machine learning model, and the
                the constructed learnblock.

        """
        if learnblock.labeled():
            yield (
                ConstructionInfo(
                    state=ConstructionInfo.State.PASSED,
                    learnblock=learnblock
                ),
                learnblock
            )

        else:
            for model in self.machine_learning_models():
                model.train(learnblock)

                if not self.valid_trained(model, learnblock.n_rows()):
                    yield (
                        ConstructionInfo(
                            state=ConstructionInfo.State.DISCARDED,
                            subject=model.abbreviation,
                            n_cluster=model.found_cluster
                        ),
                        None
                    )

                else:
                    labeled_learnblock = self.label_block(learnblock, model)
                    yield (
                        ConstructionInfo(
                            state=ConstructionInfo.State.CONSTRUCTED,
                            subject=model.abbreviation,
                            n_cluster=model.found_cluster,
                            learnblock=labeled_learnblock
                        ),
                        labeled_learnblock
                    )

    def machine_learning_models(self):
        """Yields valid configurations of unsupervised machine learning models
        regarding their cluster specificiation.

        Yields:
            ConstructionClusteringMLModel

        """
        for ml_model in self.ml_models:
            if ml_model.cluster_specific:
                for n_cluster in range(2, self.settings.max_categories+1):
                    yield ml_model.new_model_depending_on_cluster(n_cluster)
            else:
                yield ml_model.new_model()

    def valid_trained(self, model, n_rows):
        """Validate the trained unsupervised machine learning model.

        Args:
            model (ConstructionClusteringMLModel):
                Trained model.
            n_rows:
                Number of samples in learnblock, which should be constructed.

        Returns:
            bool:
                True, if the model is valid else False.

        """
        if model.found_cluster <= 1:
            return False

        for cluster, size in model.cluster_sizes.items():
            if size < self.settings.min_category_size*n_rows:
                return False

        return True

    def label_block(self, block, trained_model):
        """Assign the labels, origin, subject, sigma to the constructed
        learnblock.


        Args:
            block (PandasBlock):
                Successfully constructed learnblock.
            trained_model (ConstructionClusteringMLModel):
                Unsupervised machine learning model, which successfully
                constructed the given learnblock.

        Returns:
            PandasBlock:
                Labeled learnblock.

        """
        copied_block = deepcopy(block)
        labels = trained_model.get_labels()
        copied_block.set_column("Z", labels)
        copied_block.n_cluster = trained_model.found_cluster
        copied_block.origin = block.origin
        subject = "{}{:02}".format(trained_model.abbreviation,
                                   trained_model.found_cluster)
        copied_block.set_column("Sigma", subject)
        copied_block.subject = subject
        return copied_block

    def serial_constructor_per_combination(self):
        """Generate many constructor objects, which only using one configuraton
        regarding their cluster specification.

        Yields:
            Constructor

        """
        for model in self.machine_learning_models():
            constructor = Constructor(self.mode, self.ml_models, self.settings)
            constructor.machine_learning_models = partial(return_model, model)
            yield constructor

    @property
    def min_category_size(self):
        return self.settings.min_category_size

    @min_category_size.setter
    def min_category_size(self, value):
        self.settings.min_category_size = value

    @property
    def max_categories(self):
        return self.settings.max_categories

    @max_categories.setter
    def max_categories(self, value):
        self.settings.max_categories = value
