"""Defines the public interface to be used.

Every new functionality that is added to the system and capable of being
influenced by the user should have an interface.
The main functionality provided by this module is:
- Load settings file from a specific path.
- Returning the currently used settings.
- Create Construction object and initialize it with user specified arguments.
- Create FeatureSelector object and initialize it with user specified arguments.
- Create Reconstruction object and initialize it with user specified arguments.
- Create Deconstruction object and initialize it with user specified arguments.
- Start the learning process depending on user specified Construction,
Reconstruction, Deconstruction object.
- Load KnowledgeDatabase from a specific destination.

"""


import os
import pickle

from conML import ports
from conML.shared import settings
from conML.shared import request
from conML.usecases import command, query


__all__ = (
    "load_settings",
    "get_settings",
    "construction",
    "reconstruction",
    "reconstruction",
    "deconstruction",
    "knowledge_searcher",
    "load_knowledge",
    "feature_selection",
)


def load_settings(path):
    """Load settings from a source path and use them across the whole program.

    Args:
        path (str): Source path to the settings files.

    Returns:
        None

    """
    assert isinstance(path, str)
    assert os.path.exists(path)
    settings.read_settings(path)


def get_settings():
    """Return currently used settings.

    Returns:
        Settings:
            Currently used settings object.

    """
    return settings.Settings


def load_knowledge(path):
    """Load knowledge database from a source path.

    Args:
        path (str): Source path to the knowledge database.

    Returns:
        KnowledgeDatabase:
            Collected knowledge representation from learning process saved
            into database.

    """
    assert isinstance(path, str)
    assert os.path.exists(path)
    with open(path, "rb") as file:
        return pickle.load(file)


def construction(mode, algorithms):
    """Create construction object depending on user provided mode and
    algorithms. Algorithms should be a list of sklearn objects, which
    must define unsupervised machine learning methods.

    Note:
        Only "conceptual" mode is currently supported.

    Args:
        mode (str): Either "conceptual" or "procedural".
        algorithms (list): List with unsupervised learning algorithms from
            sklearn library.

    Returns:
        Constructor:
            Object defines construction part of learning process in
            constructivism machine learning.

    """
    assert mode == "conceptual"
    interface = ports.ConstructionClusteringMLModel
    setting = settings.specific_settings_factory("construction")
    req = request.ConstructionRequest(setting, algorithms, interface, mode)
    usecase = command.ConstructionUsecase()
    return usecase.execute(req)


def feature_selection(*, filter_method, embedded_method):
    """Create feature selection object depending on user provided filter
    and embedded methods.

    Args:
        filter_method: Filter method for feature reduction/selection from
            sklearn library.
        embedded_method: Embedded method for feature reduction/selection from
            sklearn library.

    Returns:
        FeatureSelector:
            Object define feature selection part within reconstruction process
            in constructivism machine learning.

    """
    assert filter_method is not None
    assert embedded_method is not None
    filter_method = ports.FilterMethod(filter_method)
    embedded_method = ports.EmbeddedMethod(embedded_method)
    setting = settings.specific_settings_factory("feature_selection")
    req = request.FeatureSelectionRequest(filter_method, embedded_method, setting)
    usecase = command.FeatureSelectionUsecase()
    return usecase.execute(req)


def reconstruction(mode, algorithms):
    """Create reconstruction object depending on user provided mode and
    algorithms. Algorithms should be a list of sklearn objects, which
    must define supervised machine learning methods.

    Note:
        Only "conceptual" mode is currently supported.

    Args:
        mode (str): Either "conceptual" or "procedural".
        algorithms (list): List with supervised learning algorithms from
            sklearn library.

    Returns:
        Reconstructor:
            Object defines reconstruction part of learning process in
            constructivism machine learning.

    """
    assert mode == "conceptual"
    interface = ports.ReconstructionConceptualMLModel
    setting = settings.specific_settings_factory("reconstruction")
    req = request.ReconstructionRequest(setting, algorithms, interface,
                                        mode, ports.krippendorff_alpha)
    usecase = command.ReconstructionUsecase()
    return usecase.execute(req)


def deconstruction(reconstructor):
    """Create deconstruction object depending on user provided mode.

    Note:
        Only "conceptual" mode is currently supported.

    Args:
        reconstructor (Reconstructor): Coherent instantiated Reconstructor
            object.

    Returns:
        Deconstructor:
            Object defines deconstruction part of learning process in
            constructivism machine learning.

    """
    general_settings = settings.specific_settings_factory("general")
    deconstruction_settings = settings.specific_settings_factory("deconstruction")
    block_processing_settings = settings.specific_settings_factory("block_processing")
    density_estimator = ports.KernelDensityEstimator()
    req = request.DeconstructionRequest(general_settings,
                                        deconstruction_settings,
                                        density_estimator,
                                        ports.ckmeans,
                                        block_processing_settings,
                                        ports.build_block_from_rows,
                                        ports.build_new_learnblock,
                                        reconstructor)
    usecase = command.DeconstructionUsecase()
    return usecase.execute(req)


def knowledge_searcher(constructor,
                       selector,
                       reconstructor,
                       deconstructor,
                       knowledge_database=None,
                       *,
                       stdout=False,
                       n_procs=1):
    """Start the learning process depending on user provided arguments.
    All components must have coherent modes. It is illegal to start the
    learning process with conceptual and procedural components. The user
    can follow the learning process on the stdout by flagging stdout parameter
    to True. By flagging debug to True the learning process will be logged
    in detail to a file. Further the user can speed up the process by
    utilizing many cpu cores by setting parallel to True.

    Args:
        constructor (Constructor): Coherent instantiated Constructor object.
        selector (FeatureSelector): Instantiated FeatureSelector object.
        reconstructor (Reconstructor): Coherent instantiated Reconstructor
            object.
        deconstructor (Deconstructor): Coherent instantiated Deconstructor
            object.
        knowledge_database (KnowledgeDatabase): ...
        stdout (bool): Indicator if the learning process should be logged
            to stdout.
        n_procs (int): Number of processes to utilize.

    Returns:
        KnowledgeDatabase:
            Modified Knowledge representation after the learning process.

    """
    general_settings = settings.specific_settings_factory("general")
    block_processing_settings = settings.specific_settings_factory("block_processing")
    density_estimator = ports.KernelDensityEstimator()
    req = request.KnowledgeSearchingRequest(general_settings,
                                            block_processing_settings,
                                            density_estimator,
                                            ports.convert_df_to_block,
                                            ports.build_block_from_rows,
                                            ports.ckmeans,
                                            constructor,
                                            selector,
                                            reconstructor,
                                            deconstructor,
                                            knowledge_database,
                                            stdout, n_procs)

    usecase = query.KnowledgeSearcherUsecase()
    return usecase.execute(req)
