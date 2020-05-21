#! python3  # noqa: E265

"""
    Synchroniser between loaded metadata from Scan and Isogeo database through API.
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import json
import logging
import re
import warnings
from concurrent.futures import ThreadPoolExecutor
from io import BufferedIOBase
from pathlib import Path
from time import gmtime, sleep, strftime
from typing import Union

# 3rd party
from isogeo_pysdk import Catalog, Event, FeatureAttribute, Isogeo, Metadata, Workgroup
from scan_metadata_processor.converter import LookupToIsogeo
from scan_metadata_processor.converter.matchers import (
    match_coordinate_system,
    MATCHER_FORMAT,
    MATCHER_GEOMETRY,
)

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
    """Load metadata produced by the Scan and send it to Isogeo.

    :param Isogeo api_client: authenticated API client
    :param object report: report object in which to store process results
    """

    def __init__(self, api_client: Isogeo, report: object = None):
        """Instanciating metadata synchronizer."""
        # Isogeo API client
        self.isogeo = api_client
        self.isogeo_formats_codes = [
            i.get("code") for i in self.isogeo.formats.listing()
        ]

        # report object to fill
        self.report = report

    def read_json_scanned(
        self, in_json: Union[Path, BufferedIOBase], isogeo_workgroup: str
    ):
        """Initila method to push JSON metadata to Isogeo database.

        :param Union[Path, BufferedIOBase] in_json: input JSON
        :param str isogeo_workgroup: Isogeo group in which to create the metadata
        """
        # warn about deprecated method
        warn_msg = (
            "This method was the initial tool to push JSON metadata"
            " to Isogeo. Prefer using ZIP instead."
        )
        warnings.warn(warn_msg, DeprecationWarning)
        logger.warning(warn_msg)

        # process
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
            description="Création de la métadonnée par le Scan Offline",
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

    def create_from_lookup(
        self,
        group: Workgroup,
        group_catalogs: list,
        group_coordsys: list,
        converter: LookupToIsogeo,
    ) -> Metadata:
        """Create a metadata from a Scan lookup model.

        :param Workgroup group: Isogeo group in which to create the metadata
        :param list group_catalogs: list of the group's catalogs with the option "add to scan"
        :param list group_coordsys: list of group selected coordinate-systems
        :param LookupToIsogeo converter: lookup model

        :return: created metadata
        :rtype: Metadata
        """
        # create metadata - handle hard (code) and soft (API) errors
        try:
            md_created = self.isogeo.metadata.create(
                workgroup_id=group._id, metadata=converter.as_metadata()
            )
        except Exception as err:
            err_msg = "Failed to create a metadata: {} ({}). Trace: {}".format(
                md_created.title_or_name(slugged=True), md_created._id, err
            )
            logger.error(err_msg)
            self.report.counter_errorred += 1
            return

        # check if API could create the metadata
        if not isinstance(md_created, Metadata):
            logger.error(
                "Metadata creation failed for '{}'. Error: {}".format(
                    converter.extract_name(), md_created
                )
            )
            self.report.counter_errorred += 1
            return
        else:
            self.report.counter_created += 1
            pass

        # have a break, have a kitkat (API needs a breathe...)
        sleep(0.5)
        logger.debug(
            "MD created: {} ({})".format(
                md_created._id, md_created.title_or_name(slugged=True)
            )
        )

        # creation event
        try:
            md_evt_creation = converter.prepare_event(evt_type="creation")
            self.isogeo.metadata.events.create(
                metadata=md_created, event=md_evt_creation
            )
        except Exception as err:
            err_msg = "Failed to add an event to metadata: {} ({}). Trace: {}".format(
                md_created.title_or_name(slugged=True), md_created._id, err
            )
            logger.error(err_msg)

        # SRS
        try:
            srs_match = match_coordinate_system(
                group_srs=group_coordsys, md_lookup=converter.in_lookup
            )
            self.apply_coordinate_system(
                target_metadata=md_created, srs_matcher_result=srs_match, group=group
            )
        except Exception as err:
            err_msg = "Failed to get and associate a coordinate-system to metadata: {} ({}). Trace: {}".format(
                md_created.title_or_name(slugged=True), md_created._id, err
            )
            logger.error(err_msg)

        # feature attributes
        try:
            with ThreadPoolExecutor(
                thread_name_prefix="MdFeatureAttributes"
            ) as executor:
                for featattr in converter.prepare_feature_attributes():
                    executor.submit(
                        self.isogeo.metadata.attributes.create,
                        metadata=md_created,
                        attribute=featattr,
                    )
        except Exception as err:
            err_msg = "Failed to add feature attributes to metadata: {} ({}). Trace: {}".format(
                md_created.title_or_name(slugged=True), md_created._id, err
            )
            logger.error(err_msg)

        # catalogs
        if isinstance(group_catalogs, list) and len(group_catalogs):
            try:
                self.isogeo.metadata.bulk.prepare(
                    metadatas=(md_created._id,),
                    action="add",
                    target="catalogs",
                    models=tuple(group_catalogs),
                )
                self.isogeo.metadata.bulk.send()
            except Exception as err:
                err_msg = "Failed to associate all catalogs to metadata: {} ({}). Trace: {}".format(
                    md_created.title_or_name(slugged=True), md_created._id, err
                )
                logger.warning(err_msg)
                self.isogeo.catalog.associate_metadata(
                    metadata=md_created, catalog=group_catalogs[0]
                )
        else:
            logger.warning("No catalogs to associate")

        # return signature
        return md_created

    def apply_coordinate_system(
        self, target_metadata: Metadata, srs_matcher_result: tuple, group: Workgroup
    ):
        """Add a coordinate-system to a metadata according to the SRS matcher result.

        :param Metadata target_metadata: metadata to which to add the coordinate-system
        :param tuple srs_matcher_result: result of the SRS matcher
        :param Workgroup group: group to which to add the missing coordinate-system

        :raises ValueError: for unexpected srs matcher result
        """
        if srs_matcher_result[0] == 0:
            logger.warning(
                "No coordinate-system identified for: {}".format(
                    target_metadata.title_or_name(slugged=True)
                )
            )
            self.report.li_srs_not_identified.append(target_metadata._id)
        elif srs_matcher_result[0] == 1:
            self.isogeo.srs.associate_metadata(
                metadata=target_metadata, coordinate_system=srs_matcher_result[1]
            )
        elif srs_matcher_result[0] == 2:
            self.isogeo.srs.associate_workgroup(
                coordinate_system=srs_matcher_result[1], workgroup=group
            )
            self.isogeo.srs.associate_metadata(
                metadata=target_metadata, coordinate_system=srs_matcher_result[1]
            )
        elif srs_matcher_result[0] == 3:
            logger.warning(
                "Coordinate-system not recognized by FME for: {}".format(
                    target_metadata.title_or_name(slugged=True)
                )
            )
        else:
            raise ValueError(
                "Unexpected value returned by coordinate-system matcher: {}".format(
                    srs_matcher_result
                )
            )


# #############################################################################
# ##### Main #######################
# ##################################
if __name__ == "__main__":
    pass
