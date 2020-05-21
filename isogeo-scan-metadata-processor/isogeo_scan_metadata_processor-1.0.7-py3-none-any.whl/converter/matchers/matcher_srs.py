#! python3  # noqa: E265

"""
    Helper to handle Coordinate-System.
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from typing import Tuple

# 3rd party
from isogeo_pysdk import CoordinateSystem
from scan_metadata_processor import Lookup

# #############################################################################
# ########## Globals ###############
# ##################################

logger = logging.getLogger(__name__)

# ##############################################################################
# ########## Classes ###############
# ##################################


def match_coordinate_system(
    group_srs: list, md_lookup: Lookup
) -> Tuple[int, CoordinateSystem]:
    """Determine if the dataset SRS is one of selected ones in the group configuration. \
    Match score:
      - 0: no SRS identified by lookup
      - 1: SRS identified and present among group's selection (4-4-2 as always)
      - 2: SRS identified but not selected in group configuration
      - 3: dataset seems to be projected but FME didn't not recognized the EPSG

    :param list group_srs: list of SRS selected in the group
    :param Lookup md_lookup: lookup model with a potential SRS EPSG Code

    :return: a tuple with: (match_score, SRS or None)
    :rtype: Tuple[int, CoordinateSystem]
    """
    # variables
    out_coordsys = None

    # handle case where coordinate-system could not be identified during Scan
    if not isinstance(md_lookup.coordsys, dict):
        return (0, None)

    # extract information
    in_epsg_code = md_lookup.coordsys.get("EPSG")
    in_srs_name = md_lookup.coordsys.get("name")

    # match
    if in_epsg_code is not None and in_epsg_code.isdigit():
        # transform into coordinate-system object
        out_coordsys = CoordinateSystem(code=in_epsg_code)

        # try match between group select SRS and lookup SRS
        group_srs_epsg = [int(i.get("code")) for i in group_srs]
        if int(in_epsg_code) in group_srs_epsg:
            logger.debug(
                "EPSG code matched group selected ESPG registry: {}.".format(
                    in_epsg_code
                )
            )
            has_srs = 1
        else:
            logger.debug(
                "EPSG code is not one of selected in group settings: {}.".format(
                    in_epsg_code
                )
            )
            has_srs = 2
    elif (
        "FME_0" in in_srs_name and in_srs_name == "" and md_lookup.envelope is not None
    ):
        logger.warning(
            "FME failed to recognize SRS but still calculated an envelope. "
            "Update your FME configuration."
        )
        has_srs = 3
    else:
        # fallback
        has_srs = 0

    return (has_srs, out_coordsys)
