#! python3  # noqa: E265

"""
    Search for geographic files according to the required formats.
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
from io import BufferedIOBase
import json
import logging
import re
from pathlib import Path
from time import gmtime, strftime

# 3rd party
from isogeo_pysdk import Catalog, Event, Isogeo, FeatureAttribute, Metadata

# submodules
from scan_metadata_processor.converter import MATCHER_FORMAT, MATCHER_GEOMETRY

# #############################################################################
# ########## Globals ###############
# ##################################

logger = logging.getLogger(__name__)

# regex
reg_digits_parentesis = re.compile(r"^.*?\([^\d]*(\d+)[^\d]*\).*$")

# ##############################################################################
# ########## Classes ###############
# ##################################


class MetadataSynchronizer:
    """Load metadata produced by the Scan and send it to Isogeo."""

    def __init__(self, api_client: Isogeo):
        """Instanciating metadata synchronizer."""
        # store API client
        self.isogeo = api_client
        self.isogeo_formats_codes = [
            i.get("code") for i in self.isogeo.formats.listing()
        ]

    def read_json_file(self, in_json: Path or BufferedIOBase, isogeo_workgroup: str):
        if isinstance(in_json, Path):
            with in_json.open(mode="r") as f:
                json_read = json.load(f)
        if isinstance(in_json, BufferedIOBase):
            json_read = json.load(in_json)

        dataset_scanned = json_read[0].get("dataset")

        logging.info(
            "Workgroup '{}' uploaded a metadata about the dataset: {}".format(
                isogeo_workgroup.name, dataset_scanned.get("name")
            )
        )

        # load main attributes into a metadata object
        new_metadata = Metadata(
            name=dataset_scanned.get("name"),
            title=dataset_scanned.get("name"),
            series=False,
            editionProfile="manual",
            path=str(dataset_scanned.get("path")),
            features=dataset_scanned.get("numberOfFeatures"),
            geometry=MATCHER_GEOMETRY.get(dataset_scanned.get("type")),
            envelope=json.loads(dataset_scanned.get("envelope", [])),
            language=isogeo_workgroup.metadataLanguage,
        )

        # get type from matching format
        md_format = MATCHER_FORMAT.get(dataset_scanned.get("formatShort"))
        if md_format in self.isogeo_formats_codes:
            logging.info(
                "Format '{}' matched Isogeo formats registry: {}".format(
                    dataset_scanned.get("formatShort"), md_format
                )
            )
            new_metadata.format = md_format

            # deduce type from format
            isogeo_format = self.isogeo.formats.get(format_code=md_format)

            # if dataset, be more specific
            if isogeo_format.type == "dataset" and MATCHER_GEOMETRY.get(
                dataset_scanned.get("type")
            ):
                new_metadata.type = "vectorDataset"
            else:
                new_metadata.type = isogeo_format.type

        else:
            new_metadata.type = "resource"

        # create the metadata
        logging.info("Creating a new {} metadata...".format(new_metadata.type))
        metadata_created = self.isogeo.metadata.create(
            workgroup_id=isogeo_workgroup._id, metadata=new_metadata
        )
        if not isinstance(metadata_created, Metadata):
            logging.error("Creation of metadata on Isogeo failed...")
            return new_metadata
        else:
            logging.info("Metadata created on Isogeo: {}".format(metadata_created._id))

        # apply coordinate-system
        srs_epsg_code = dataset_scanned.get("coordsys", {}).get("EPSG")
        if srs_epsg_code is not None and srs_epsg_code.isdigit():
            isogeo_srs = self.isogeo.coordinate_system.get(
                coordinate_system_code=srs_epsg_code
            )
            logging.info(
                "EPSG code {} matched Isogeo ESPG registry: {}. Applying it to the created metadata...".format(
                    srs_epsg_code, isogeo_srs.name
                )
            )
            self.isogeo.coordinate_system.associate_metadata(
                metadata=metadata_created, coordinate_system=isogeo_srs
            )

        # apply feature attributes
        if metadata_created.type == "vectorDataset" and len(
            dataset_scanned.get("attributes", [])
        ):
            logging.info(
                "{} feature attributes spotted. Let's add them...".format(
                    len(dataset_scanned.get("attributes"))
                )
            )
            for featattr in dataset_scanned.get("attributes"):
                # extract length from feature-attribute type
                length_filter = reg_digits_parentesis.match(featattr.get("type"))
                if length_filter:
                    attr_length = length_filter.group(1)
                    attr_type = featattr.get("type").replace(
                        "({})".format(attr_length), ""
                    )
                else:
                    attr_length = None
                    attr_type = featattr.get("type")

                # load in object
                new_featattr = FeatureAttribute(
                    name=featattr.get("name"), dataType=attr_type, length=attr_length
                )
                # apply insee_com
                if featattr.get("name").lower() == "insee_com":
                    new_featattr.alias = "Numéro INSEE de la commune"
                    new_featattr.description = (
                        "Il  s’agit  de  la  valeur  de  l’attribut"
                        " INSEE_COM  de  la  commune  à  laquelle  se  rapporte  le  chef-lieu.\n\n"
                        "Il permet d’établir un lien entre le ponctuel de la classe CHEF_LIEU "
                        "et l’objet surfacique de la classe COMMUNE."
                    )

                #
                self.isogeo.metadata.attributes.create(
                    metadata=metadata_created, attribute=new_featattr,
                )

        # apply catalogs with $scan option
        wg_catalogs = self.isogeo.catalog.listing(
            workgroup_id=isogeo_workgroup._id, include=None
        )
        for cat in wg_catalogs:
            if cat.get("$scan", False):
                self.isogeo.catalog.associate_metadata(
                    metadata=metadata_created, catalog=Catalog.clean_attributes(cat)
                )
                logging.info(
                    "Metadata {} associated to the catalog: {}".format(
                        metadata_created._id, cat.get("name")
                    )
                )

        # creation event
        md_evt_creation = Event(
            date=strftime("%Y-%m-%d", gmtime()),
            description="Création de la métadonnée par le Scan Metadata Processor",
            kind="update",
            parent_resource=metadata_created._id,
        )
        self.isogeo.metadata.events.create(
            metadata=metadata_created, event=md_evt_creation
        )

        # return final metadata
        return self.isogeo.metadata.get(
            metadata_created._id,
            include=("coordinate-system", "feature-attributes", "tags"),
        )


# #############################################################################
# ##### Main #######################
# ##################################
if __name__ == "__main__":
    pass
