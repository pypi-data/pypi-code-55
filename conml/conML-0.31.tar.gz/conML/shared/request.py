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


"""Defines request for commands and queries.

"""


from collections import namedtuple


ConstructionRequest = namedtuple(
    "ConstructionRequest", "settings, algorithms, interface, mode"
)


FeatureSelectionRequest = namedtuple("FeatureSelectionRequest",
                                     ("filter_method,"
                                      "embedded_method,"
                                      "settings"))


ReconstructionRequest = namedtuple("ReconstructionRequest", ("settings,"
                                                             "algorithms,"
                                                             "interface,"
                                                             "mode,"
                                                             "krippendorf"))

DeconstructionRequest = namedtuple("DeconstructionRequest",
                                   ("general_settings,"
                                    "deconstruction_settings,"
                                    "density_estimator,"
                                    "ckmeans,"
                                    "block_processing_settings,"
                                    "build_block_from_rows,"
                                    "build_new_learnblock,"
                                    "reconstructor"))


KnowledgeSearchingRequest = namedtuple("KnowledgeSearchingRequest",
                                       ("general_settings,"
                                        "block_processing_settings,"
                                        "density_estimator,"
                                        "df_converter,"
                                        "build_block_from_rows,"
                                        "ckmeans,"
                                        "constructor,"
                                        "feature_selector,"
                                        "reconstructor,"
                                        "deconstructor,"
                                        "knowledge,"
                                        "stdout,"
                                        "n_procs"))
