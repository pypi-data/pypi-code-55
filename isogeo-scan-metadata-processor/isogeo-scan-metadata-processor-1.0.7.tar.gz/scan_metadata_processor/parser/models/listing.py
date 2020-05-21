#! python3  # noqa E265

"""
    Isogeo Scan - Model of metadata output of Listing vector.
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# standard library
import logging
import pprint
from typing import List


# #############################################################################
# ########## Globals ###############
# ##################################

logger = logging.getLogger(__name__)


# #############################################################################
# ########## Classes ###############
# ##################################
class Listing(object):
    """Output from FME scripts list-*."""

    ATTR_TYPES = {"listFeaturesTypes": list, "source": str}

    def __init__(self, results: List[dict], source: str = None, **kwargs):
        # default values for the object error/properties
        self._listFeatureTypes = None
        self._source = source

        # if values have been passed, so use them as objects error.
        # error are prefixed by an underscore '_'
        if results is not None:
            self._listFeatureTypes = [
                i.get("result").get("featureType") for i in results
            ]
        if source is not None:
            self._source = source

        # warn about unsupported attributes
        if len(kwargs):
            logger.warning(
                "Folllowings fields were not expected and have been ignored. "
                "Maybe consider adding them to the model: {}.".format(
                    " | ".join(kwargs.keys())
                )
            )

    # -- PROPERTIES --------------------------------------------------------------------
    # listFeaturesTypes
    @property
    def listFeaturesTypes(self) -> List[dict]:
        """Gets the list of feature types of the described dataset.

        :return: the list of feature types of the described dataset.
        :rtype: List[dict]
        """
        return self._listFeatureTypes

    @listFeaturesTypes.setter
    def listFeaturesTypes(self, listFeaturesTypes: List[dict]):
        """Sets the list of features types of the described dataset.

        :param List[dict] listFeaturesTypes: the list of feature types of the described dataset.
        """

        self._listFeatureTypes = listFeaturesTypes

    # source
    @property
    def source(self) -> str:
        """Gets the source.

        :return: the source of the listed feature types.
        :rtype: str
        """
        return self._source

    @source.setter
    def source(self, source: str):
        """Sets the source of the listed feature types.

        :param str source: the source of the listed feature types.
        """

        self._source = source

    # -- METHODS -----------------------------------------------------------------------
    def to_dict(self) -> dict:
        """Returns the model properties as a dict."""
        result = {}

        for attr, _ in self.ATTR_TYPES.items():
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value
        if issubclass(Listing, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model."""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other) -> bool:
        """Returns true if both objects are equal."""
        if not isinstance(other, Listing):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other) -> bool:
        """Returns true if both objects are not equal."""
        return not self == other


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """standalone execution."""
