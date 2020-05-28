#! python3  # noqa: E265

"""
    Synchroniser between loaded metadata from Scan and Isogeo database through API.
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from concurrent.futures import ThreadPoolExecutor
from time import gmtime, sleep, strftime

# 3rd party
from isogeo_pysdk import Event, FeatureAttribute, Isogeo, Metadata, Workgroup
from scan_metadata_processor.comparator import MetadataComparator
from scan_metadata_processor.converter import LookupToIsogeo
from scan_metadata_processor.converter.matchers import match_coordinate_system

# #############################################################################
# ########## Globals ###############
# ##################################

logger = logging.getLogger(__name__)

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
        :param LookupToIsogeo converter: lookup converter to Isogeo metadata

        :return: created metadata
        :rtype: Metadata
        """
        # create metadata - handle hard (code) and soft (API) errors
        try:
            md_created = self.isogeo.metadata.create(
                workgroup_id=group._id, metadata=converter.as_metadata()
            )
        except Exception as err:
            err_msg = "Failed to create a metadata: {}. Trace: {}".format(
                converter.extract_name(), err
            )
            logger.error(err_msg)
            self.report.counter_errorred += 1
            return

        # check if API could create the metadata
        if not isinstance(md_created, Metadata):
            if converter.in_lookup.envelope is not None:
                logger.warning(
                    "Creation failed. Try again without the geographic envelope "
                    "because of left-hand rule handling in Isogeo API."
                )
                converter.in_lookup.envelope = None
                self.report.li_envelope_incorrect.append(converter.extract_name())
                return self.create_from_lookup(
                    group, group_catalogs, group_coordsys, converter
                )
            logger.error(
                "Metadata creation failed for '{}'. Error: {}".format(
                    converter.extract_name(), md_created
                )
            )
            self.report.counter_errorred += 1
            return
        else:
            self.report.counter_created += 1

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
                thread_name_prefix="AddFeatureAttributes"
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

    def update_from_comparator(self, comparator: MetadataComparator) -> Metadata:

        """Create a metadata from a Scan lookup model.

        :param MetadataComparator comparator: comparator object used to perform \
        deletion/addition operations

        :return: created metadata
        :rtype: Metadata
        """
        # extract objects from comparator
        md_to_update = comparator.md_old
        md_from_lookup = comparator.md_new
        evt_diff = Event(
            date=strftime("%Y-%m-%d", gmtime()),
            description=comparator.diff_message(),
            kind="update",
        )

        # update features count
        if comparator.diff_features_count():
            logger.debug("Updating features count for: {}".format(md_to_update._id))
            md_to_update.features = md_from_lookup.features
            self.isogeo.metadata.update(metadata=md_to_update)

        # update coordinate-system
        if comparator.diff_srs():
            logger.debug("Changing coordinate-system for: {}".format(md_to_update._id))
            self.isogeo.coordinate_system.associate_metadata(
                metadata=md_to_update, coordinate_system=md_from_lookup.coordinateSystem
            )

        # update feature attributes
        diff_attrs = comparator.diff_features_attributes()
        if diff_attrs[0]:
            # add new attributes
            try:
                with ThreadPoolExecutor(
                    thread_name_prefix="AddFeatureAttributes"
                ) as executor:
                    for new_attr in diff_attrs[1]:
                        executor.submit(
                            self.isogeo.metadata.attributes.create,
                            metadata=md_to_update,
                            attribute=FeatureAttribute(
                                name=new_attr[0], dataType=new_attr[1]
                            ),
                        )
            except Exception as err:
                err_msg = "Failed to add feature attributes to metadata: {} ({}). Trace: {}".format(
                    md_to_update.title_or_name(slugged=True), md_to_update._id, err
                )
                logger.error(err_msg)

            # remove deleted attributes
            # we need the attribute _id, so make a match
            match_attr_to_remove = [
                attr
                for attr in md_to_update.featureAttributes
                if attr.name in diff_attrs[2]
            ]
            try:
                with ThreadPoolExecutor(
                    thread_name_prefix="RemoveFeatureAttributes"
                ) as executor:
                    for attr in match_attr_to_remove:
                        executor.submit(
                            self.isogeo.metadata.attributes.delete,
                            attribute=attr,
                            metadata=md_to_update,
                        )
            except Exception as err:
                err_msg = "Failed to add feature attributes to metadata: {} ({}). Trace: {}".format(
                    md_to_update.title_or_name(slugged=True), md_to_update._id, err
                )
                logger.error(err_msg)

        # add update event
        try:
            self.isogeo.metadata.events.create(metadata=md_to_update, event=evt_diff)
        except Exception as err:
            logger.error(
                "Failed to add update event to metadata: {}. Trace: {}".format(
                    md_to_update.admin_url(), err
                )
            )


# #############################################################################
# ##### Main #######################
# ##################################
if __name__ == "__main__":
    pass
