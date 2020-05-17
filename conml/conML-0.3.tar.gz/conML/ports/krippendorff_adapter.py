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


"""Defines the wrapper for calculating the inter-reliabiilty coefficient.

"""


import krippendorff


def krippendorff_alpha(voter):
    """Wrapper for krippendorff - alpha interreliability.

   Calculates the consensus between voters.

    Args:
        voter (list): Multidimensional array.

    Returns:
        float:
            Interreliability between voters.
            1.0 perfect consensus between voter.
            0.0 no consensus at all.
            -1.0 contradiction between voter.


    """
    val = krippendorff.alpha(voter)
    return round(val, 3)
