#! python3  # noqa E265

"""
    Isogeo Scan - Model of metadata output of Sign vector.
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# standard library
import logging
import pprint
from typing import Union


# #############################################################################
# ########## Globals ###############
# ##################################

logger = logging.getLogger(__name__)


# #############################################################################
# ########## Classes ###############
# ##################################
class Sign(object):
    """Output from FME scripts sign-*."""

    ATTR_TYPES = {
        "error": list,
        "signatures": Union[str, list],
    }

    def __init__(
        self,
        feature: dict = None,
        error: list = None,
        signatures: Union[str, list] = None,
        **kwargs,
    ):
        # default values for the object error/properties
        self._feature = None
        self._error = None
        self._signatures = None

        # if values have been passed, so use them as objects error.
        # error are prefixed by an underscore '_'
        if feature is not None:
            # case when the JSON is passed
            error = feature.get("error")
            signatures = feature.get("signatures")
        if error is not None:
            self._error = error
        if signatures is not None:
            if isinstance(signatures, str):
                signatures = [signatures]
            self._signatures = signatures

        # warn about unsupported attributes
        if len(kwargs):
            logger.warning(
                "Folllowings fields were not expected and have been ignored. "
                "Maybe consider adding them to the model: {}.".format(
                    " | ".join(kwargs.keys())
                )
            )

    # -- PROPERTIES --------------------------------------------------------------------
    # error
    @property
    def error(self) -> str:
        """Gets the error message.

        :return: error message recorded by the Scan.
        :rtype: str
        """
        return self._error

    @error.setter
    def error(self, error: str):
        """Sets the error message.

        :param str error: error message recorded by the Scan.
        """

        self._error = error

    # signatures
    @property
    def signatures(self) -> list:
        """Gets the signatures of this Metadata.

        :return: The signatures of this Metadata.
        :rtype: list
        """
        return self._signatures

    @signatures.setter
    def signatures(self, signatures: list):
        """Sets the signatures of this Metadata.

        :param list signatures: to be set
        """
        self._signatures = signatures

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
        if issubclass(Sign, dict):
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
        if not isinstance(other, Sign):
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
    sample = Sign()
