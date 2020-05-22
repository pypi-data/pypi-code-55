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


"""Define application specific exceptions.

"""


class BaseError(Exception):
    """Base class for all application specific exceptions.

    """
    pass


class ModeError(BaseError):
    """Will be thrown, if the modes for Constructor and Reconstructor
    are not identical.

    """
    pass


class IndexOutOfBucket(BaseError):
    """Will be thrown, if the given index for the requested row does not
    correspond to any row within the stored block.

    """
    pass


class ConfigurationFileError(BaseError):
    """Will be thrown, if the configuration file cannot be read.

    """
    pass
