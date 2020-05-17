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


"""Define the commands of the framework.

"""


from conML.usecases.usecase import Usecase
from conML.domain import (
    FeatureSelector,
    Reconstructor,
    Constructor,
    Deconstructor,
    ClusterFinder)


class ModelCreationMixin:
    def create_models(self, interface, algorithms):
        """Instantiated MachineLearningModels via the given interface.

        Args:
            interface (Callable): Adapter.
            algorithms (List): List of scikit-algorithms.

        Yield:
            MachineLearningModel

        """
        for abbreviation, algorithm in algorithms:
            model = interface(algorithm, abbreviation)
            yield model


class FeatureSelectionUsecase(Usecase):
    def process(self, request):
        """Process request for creating a FeatureSelector.

        Args:
            request (FeatureSelectionRequest): Namedtuple with all essential
                ingredients.

        Returns:
            FeatureSelector

        """
        return FeatureSelector(request.filter_method,
                               request.embedded_method,
                               request.settings)


class ReconstructionUsecase(Usecase, ModelCreationMixin):
    def process(self, request):
        """Process request for creating a Reconstructor.

        Args:
            request (ReconstructorRequest): Namedtuple with all essential
                ingredients.

        Returns:
            Reconstructor

        """
        models = list(self.create_models(request.interface, request.algorithms))
        return Reconstructor(request.mode, models, request.settings,
                             request.krippendorf)


class ConstructionUsecase(Usecase, ModelCreationMixin):
    def process(self, request):
        """Process request for creating a Constructor.

        Args:
            request (ConstructorRequest): Namedtuple with all essential
                ingredients.

        Returns:
            Constructor

        """
        models = list(self.create_models(request.interface, request.algorithms))
        constructor = Constructor(request.mode, models, request.settings)
        return constructor


class DeconstructionUsecase(Usecase):
    def process(self, request):
        """Process request for creating Deconstructor.

        Args:
            request (DeconstructionRequest): Namedtuple with all essential
                ingredients.

        Returns:
            Deconstructor

        """
        cluster_finder = ClusterFinder(request.density_estimator,
                                       request.block_processing_settings,
                                       request.ckmeans)
        return Deconstructor(request.general_settings,
                             request.block_processing_settings,
                             request.deconstruction_settings,
                             request.reconstructor,
                             request.build_new_learnblock,
                             cluster_finder)
