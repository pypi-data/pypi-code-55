#! python3  # noqa: E265

"""
    Model converter from lookup to Isogeo model.
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import json
import logging
import re
from time import gmtime, strftime
from typing import List

# 3rd party
import geojson
from isogeo_pysdk import Event, FeatureAttribute, Metadata, Workgroup

# submodules
from scan_metadata_processor.__about__ import __version__
from scan_metadata_processor.converter import MATCHER_FORMAT, MATCHER_GEOMETRY
from scan_metadata_processor.parser.models import Lookup

# #############################################################################
# ########## Globals ###############
# ##################################

logger = logging.getLogger(__name__)

# regex
reg_digits_parentesis = re.compile(r"^.*?\([^\d]*(\d+)[^\d]*\).*$")

# ##############################################################################
# ########## Classes ###############
# ##################################


class LookupToIsogeo:
    """Model converter from lookup to Isogeo model."""

    COORDINATES_ROUND_LEVEL = 3

    def __init__(
        self, in_lookup: Lookup, isogeo_formats: list, isogeo_group: Workgroup,
    ):
        """Instanciation method."""
        self.in_lookup = in_lookup
        self.formats = isogeo_formats
        self.group = isogeo_group

    def prepare_event(self, evt_type: str = "creation") -> Event:
        """Prepare event text and date."""
        # prepare text
        if evt_type == "creation":
            evt_kind = "update"
            evt_txt = "Métadonnée générée par le Scan, puis créee par Metadata Processor v{}.".format(
                __version__,
            )
            if self.in_lookup.fmeEnv:
                evt_txt += "\nInformations extraites avec {} ({}.fmw)".format(
                    self.in_lookup.fmeEnv.get("version"),
                    self.in_lookup.fmeEnv.get("fmw"),
                )

        # creation event
        evt_date = strftime("%Y-%m-%d", gmtime())

        return Event(date=evt_date, description=evt_txt, kind=evt_kind)

    def prepare_feature_attributes(self) -> List[FeatureAttribute]:
        """Prepare feature attributes to be added to the metadata (only for vectors).

        :return: list of feature attributes ready to be added
        :rtype: List[FeatureAttribute]
        """
        out_feature_attributes = []

        # if no vector, no feature attributes
        if self.match_type != "vectorDataset":
            return out_feature_attributes

        # check if attributes were detected by the scan
        if not isinstance(self.in_lookup.attributes, list) or not len(
            self.in_lookup.attributes
        ):
            return out_feature_attributes

        for featattr in self.in_lookup.attributes:
            # extract length from feature-attribute type
            length_filter = reg_digits_parentesis.match(featattr.get("type"))
            if length_filter:
                attr_length = length_filter.group(1)
                attr_type = featattr.get("type").replace("({})".format(attr_length), "")
            else:
                attr_length = None
                attr_type = featattr.get("type")

            # load in object and to the output list
            out_feature_attributes.append(
                FeatureAttribute(
                    name=featattr.get("name"), dataType=attr_type, length=attr_length
                )
            )

        return out_feature_attributes

    def extract_envelope(self) -> dict:
        """Load envelope as GeoJSON, validate it and reduce precision to be more light.

        :return: geographic envelope as dict
        :rtype: dict
        """
        out_envelope = None

        if self.in_lookup.envelope:
            try:
                in_envelope = geojson.loads(self.in_lookup.envelope)
                if not in_envelope.is_valid:
                    logger.warning(
                        "Envelope GeoJSON of '{}' is not valid: {}".format(
                            self.in_lookup.name, in_envelope.errors()
                        )
                    )
                # round coordinates
                out_envelope = geojson.GeoJSON.to_instance(
                    geojson.utils.map_coords(
                        lambda x: round(x, self.COORDINATES_ROUND_LEVEL), in_envelope
                    )
                )
            except Exception as err:
                logger.error(
                    "Failed loading the envelope from {}. Using the raw string."
                    "Trace: {}".format(self.in_lookup.name),
                    err,
                )
                out_envelope = json.loads(self.in_lookup.envelope)

        return out_envelope

    def extract_name(self) -> str:
        """Extract name."""
        out_name = self.in_lookup.name

        # using open api driver add a forbidden char: '/'
        if (
            self.match_format_code == "filegdb"
            and self.in_lookup.formatShort == "FILEGDB"
        ):
            out_name = out_name.replace(r"/", ".")

        return out_name

    def extract_path(self) -> str:
        """Extract path."""
        out_path = None
        if self.in_lookup.path:
            out_path = self.in_lookup.path

        return out_path

    @property
    def match_format_code(self) -> str:
        """Try to match lookup format (FME short and long names) with:
          1. custom matching table included in submodule
          2. Isogeo formats registry codes.

        :return: Isogeo format code
        :rtype: str
        """
        isogeo_formats_codes = [i.get("code") for i in self.formats]
        # matching format
        md_format = MATCHER_FORMAT.get(self.in_lookup.formatShort)
        # first try to refer to Isogeo formats matrix
        if md_format in isogeo_formats_codes:
            logger.debug(
                "Format '{}' matched custom formats conversion table: {}".format(
                    self.in_lookup.formatShort, md_format
                )
            )
            out_format_code = md_format
        elif (
            isinstance(self.in_lookup.formatShort, str)
            and self.in_lookup.formatShort.lower() in isogeo_formats_codes
        ):
            logger.debug(
                "Format '{}' found in Isogeo formats registry (codes): {}".format(
                    self.in_lookup.formatShort.lower(), md_format
                )
            )
            out_format_code = self.in_lookup.formatShort.lower()
        else:
            out_format_code = None
            logging.warning(
                "Format '{}' not recognized for file: {}".format(
                    self.in_lookup.formatShort, self.in_lookup.path
                )
            )

        return out_format_code

    @property
    def match_format_version(self) -> str:
        """Guess the format version."""
        out_format_version = None

        # without format code, no format version
        if not self.match_format_code:
            return out_format_version

        # get the Isogeo format matching format code
        matched_fmt = [
            fmt for fmt in self.formats if fmt.get("code") == self.match_format_code
        ][0]

        # remove null versions
        matched_versions = [
            version for version in matched_fmt.get("versions") if version is not None
        ]

        # if only one version,so let's use it!
        if len(matched_versions) == 1:
            out_format_version = matched_versions[0]

        return out_format_version

    @property
    def match_geometry_type(self) -> str:
        """Guess metadata geometry type."""
        # matching format
        geometry_type = MATCHER_GEOMETRY.get(self.in_lookup.geometryType)

        return geometry_type

    @property
    def match_type(self) -> str:
        """Guess metadata type."""
        # default type
        out_md_type = "resource"

        # match between lookup status and type
        if self.in_lookup.isVector:
            out_md_type = "vectorDataset"
        elif self.in_lookup.isRaster:
            out_md_type = "rasterDataset"

        return out_md_type

    def as_metadata(self) -> Metadata:
        consolidated_md = Metadata(
            _creator=self.group,
            editionProfile="manual",
            envelope=self.extract_envelope(),
            features=self.in_lookup.numberOfFeatures or None,
            format=self.match_format_code,
            formatVersion=self.match_format_version,
            geometry=self.match_geometry_type,
            language=self.group.metadataLanguage or "fr",
            name=self.extract_name(),
            path=self.extract_path(),
            title=self.extract_name(),
            series=False,
            type=self.match_type,
        )

        return consolidated_md


# #############################################################################
# ##### Main #######################
# ##################################
if __name__ == "__main__":
    pass
