#! python3  # noqa: E265

"""
    Compare metadata and calculate diffs.
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from copy import copy
from typing import Tuple, Union

# 3rd party
from isogeo_pysdk import CoordinateSystem, FeatureAttribute, Metadata

# submodule
from scan_metadata_processor import _
from scan_metadata_processor.__about__ import __title__, __version__

# #############################################################################
# ########## Globals ###############
# ##################################

# log
logger = logging.getLogger(__name__)

# ##############################################################################
# ########## Classes ###############
# ##################################


class MetadataComparator:
    """Calculates diffs between two metadatas.

    :param Metadata metadata_old: reference metadata
    :param Metadata metadata_new: new metadata to compare with the reference
    """

    def __init__(self, metadata_old: Metadata, metadata_new: Metadata):
        """Instanciating module."""
        # store args as attributes
        self.md_old = copy(metadata_old)
        self.md_new = copy(metadata_new)

    def has_changed(self) -> bool:
        """Shortcut to determine if metadatas are different.

        :return: True if both metadata are different. False if not.
        :rtype: bool
        """
        return any(
            (
                self.diff_features_count(),
                self.diff_srs(),
                self.diff_features_attributes()[0],
            )
        )

    def diff_features_count(self) -> int:
        """Calculates the diff between features count. Only for vector datasets. \
        For non-vector data, returns 0. For vector datasets:
          - diff is positive if there is more objects than before.
          - diff is negative if there is less objects than before.

        :return: difference
        :rtype: int
        """
        if not all(i.type == "vectorDataset" for i in (self.md_old, self.md_new)):
            return 0

        # compare
        return self.md_new.features - self.md_old.features

    def diff_features_attributes(self) -> Tuple[int, set, set]:
        """Calculates the diff between features attributes. Only for vector datasets. \
        For non-vector data, returns (0,).

        :return: (diff, set of added attributes, set of removed attributes)
        :rtype: Tuple[0] or Tuple[int, set, set]
        """
        if not all(i.type == "vectorDataset" for i in (self.md_old, self.md_new)):
            return (0,)

        # shortcuts
        md_old_attrs = self.md_old.featureAttributes or []
        md_new_attrs = self.md_new.featureAttributes or []

        # ensure types
        self.md_old.featureAttributes = md_old_attrs = [
            FeatureAttribute(**f) if isinstance(f, dict) else f for f in md_old_attrs
        ]
        self.md_new.featureAttributes = md_new_attrs = [
            FeatureAttribute(**f) if isinstance(f, dict) else f for f in md_new_attrs
        ]

        # make feature attributes list unique
        md_new_attrs_set = set(x.name for x in md_new_attrs)
        md_old_attrs_set = set(x.name for x in md_old_attrs)

        # calculate diff between sets
        diff_set_add = md_new_attrs_set - md_old_attrs_set  # added
        diff_set_rmv = md_old_attrs_set - md_new_attrs_set  # removed
        return (len(diff_set_add) + len(diff_set_rmv), diff_set_add, diff_set_rmv)

    def diff_srs(self) -> int:
        """Calculates the diff between features count:
          - `-1`: coordinate-system have been removed
          - `0`: no change
          - `1`: coordinate-system have been added
          - `2`: coordinate-system have changed

        :return: difference code
        :rtype: int
        """
        # shortcuts
        md_old_srs = self.md_old.coordinateSystem
        md_new_srs = self.md_new.coordinateSystem

        # ensure input types
        if isinstance(md_old_srs, dict):
            md_old_srs = self.md_old.coordinateSystem = CoordinateSystem(**md_old_srs)
        if isinstance(md_new_srs, dict):
            md_new_srs = self.md_new.coordinateSystem = CoordinateSystem(**md_new_srs)

        # if both metadata have a coordinate-system, null or changed
        if isinstance(md_old_srs, CoordinateSystem) and isinstance(
            md_new_srs, CoordinateSystem
        ):
            if int(md_old_srs.code) == int(md_new_srs.code):
                return 0
            else:
                return 2
        # if previous version had a coordsys but not the new = removed
        elif isinstance(md_old_srs, CoordinateSystem) and not isinstance(
            md_new_srs, CoordinateSystem
        ):
            return -1
        # if previous version did not have a coordsys but the new = added
        elif not isinstance(md_old_srs, CoordinateSystem) and isinstance(
            md_new_srs, CoordinateSystem
        ):
            return 1
        else:
            return 0

    def diff_message(self) -> Union[str, None]:
        """Summarize diffences and returns a pre-formatted message. \
        Useful as update description. If no diff, returns None.

        :return: summary of diffs
        :rtype: str or None
        """
        # build output message
        out_msg = ""

        # -- FEATURES COUNT
        diff_features_count = self.diff_features_count()
        if diff_features_count > 0:
            out_msg += _("Entities count changed: ")
            out_msg += _("{} more objects (previously {})").format(
                abs(diff_features_count), self.md_old.features
            )
            out_msg += "\n"
        elif diff_features_count < 0:
            out_msg += _("Entities count changed: ")
            out_msg += _("{} objects less (previously {})").format(
                abs(diff_features_count), self.md_old.features
            )

            out_msg += "\n"
        else:
            pass

        # -- SRS
        diff_srs = self.diff_srs()
        if diff_srs < 0:
            out_msg += _(
                "\n**Coordinate-system** has been removed: {} ({}).".format(
                    self.md_old.coordinateSystem.name, self.md_old.coordinateSystem.code
                )
            )
            out_msg += "\n"
        elif diff_srs == 1:
            out_msg += _(
                "**Coordinate-system** has been added: {} ({}).".format(
                    self.md_new.coordinateSystem.name, self.md_new.coordinateSystem.code
                )
            )
            out_msg += "\n"
        elif diff_srs == 2:
            out_msg += _(
                "**Coordinate-system** have changed from {} ({}) to {} ({}).".format(
                    self.md_old.coordinateSystem.name,
                    self.md_old.coordinateSystem.code,
                    self.md_new.coordinateSystem.name,
                    self.md_new.coordinateSystem.code,
                )
            )
            out_msg += "\n"
        else:
            pass

        # -- FEATURE ATTRIBUTES
        diff_attrs = self.diff_features_attributes()
        if diff_attrs[0]:
            out_msg += _("\n**Feature attributes** have changed:\n")

            # added attrs
            if diff_attrs[1]:
                out_msg += _("\n- {} added: {}").format(
                    len(diff_attrs[1]), _("; ").join(diff_attrs[1])
                )

            else:
                out_msg += _("\n- no new attribute.")

            # removed attrs
            if diff_attrs[2]:
                out_msg += _("\n- {} removed: {}").format(
                    len(diff_attrs[2]), _("; ").join(diff_attrs[2])
                )

            else:
                out_msg += _("\n- no removed attribute.")

            out_msg += "\n"

        # if output message is still empty, returns None
        if out_msg == "":
            return None

        # add watermark
        out_msg += _("\n\n----\n*Processed by {} v{}*").format(__title__, __version__)

        return out_msg.strip()


# #############################################################################
# ##### Main #######################
# ##################################
if __name__ == "__main__":
    pass
