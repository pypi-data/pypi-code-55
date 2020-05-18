#! python3  # noqa E265

"""
    Isogeo Scan - Model of metadata output of lookup vector.
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# standard library
import logging
import pprint

# #############################################################################
# ########## Globals ###############
# ##################################

logger = logging.getLogger(__name__)


# #############################################################################
# ########## Classes ###############
# ##################################
class Lookup(object):
    """Metadata produced by FME script lookup-*."""

    ATTR_TYPES = {
        "attributes": list,
        "bands": list,
        "bands_count": int,
        "bbox": list,
        "cols_count": int,
        "coordsys": dict,
        "dataSources": list,
        "description": str,
        "envelope": str,
        "fmeEnv": dict,
        "formatLong": str,
        "formatShort": str,
        "formatVersion": str,
        "geometryType": str,
        "name": str,
        "numberOfFeatures": int,
        "path": str,
        "rows_count": int,
    }

    ATTR_MAP = {
        "fme_formatShort": "formatShort",
        "fme_formatLong": "formatLong",
    }

    def __init__(
        self,
        attributes: list = None,
        bands: list = None,
        bands_count: int = None,
        bbox: list = None,
        cols_count: int = None,
        coordsys: dict = None,
        dataset: dict = None,
        dataSources: list = None,
        description: str = None,
        envelope: str = None,
        fmeEnv: dict = None,
        fme_formatShort: str = None,
        fme_formatLong: str = None,
        formatLong: str = None,
        formatShort: str = None,
        formatVersion: str = None,
        name: str = None,
        numberOfFeatures: int = None,
        path: str = None,
        rows_count: int = None,
        type: str = None,  # will be converted to geometry_type
        **kwargs,
    ):
        # default values for the object attributes/properties
        self._attributes = None
        self._bands = None
        self._bands_count = None
        self._bbox = None
        self._cols_count = None
        self._coordsys = None
        self._dataSources = None
        self._description = None
        self._envelope = None
        self._fmeEnv = None
        self._fme_formatShort = None
        self._fme_formatLong = None
        self._formatLong = None
        self._formatShort = None
        self._formatVersion = None
        self._geometryType = None
        self._name = None
        self._numberOfFeatures = None
        self._path = None
        self._rows_count = None

        # case when the JSON is passed
        if dataset:
            attributes = dataset.get("attributes")
            bands = dataset.get("bands")
            bands_count = dataset.get("bands_count")
            bbox = dataset.get("bbox")
            cols_count = dataset.get("cols_count")
            dataSources = dataset.get("dataSources")
            description = dataset.get("description")
            envelope = dataset.get("envelope")
            fmeEnv = dataset.get("fmeEnv")
            fme_formatShort = dataset.get("fme_formatShort")
            fme_formatLong = dataset.get("fme_formatLong")
            formatLong = dataset.get("formatLong")
            formatShort = dataset.get("formatShort")
            formatVersion = dataset.get("formatVersion")
            name = dataset.get("name")
            numberOfFeatures = dataset.get("numberOfFeatures")
            path = dataset.get("path")
            rows_count = dataset.get("rows_count")
            type = dataset.get("type")

        # if values have been passed, so use them as objects attributes.
        # attributes are prefixed by an underscore '_'
        if attributes is not None:
            self._attributes = attributes
        if bands is not None:
            self._bands = bands
        if bands_count is not None:
            self._bands_count = bands_count
        if bbox is not None:
            self._bbox = bbox
        if cols_count is not None:
            self._cols_count = cols_count
        if coordsys is not None:
            self._coordsys = coordsys
        if dataSources is not None:
            self._dataSources = dataSources
        if description is not None:
            self._description = description
        if envelope is not None:
            self._envelope = envelope
        if fmeEnv is not None:
            self._fmeEnv = fmeEnv
        # handle different formats names
        if fme_formatLong is not None:
            self.formatLong = fme_formatLong
        if fme_formatShort is not None:
            self.formatShort = fme_formatShort
        if formatLong is not None:
            self._formatLong = formatLong
        if formatShort is not None:
            self._formatShort = formatShort
        if formatVersion is not None:
            self._formatVersion = formatVersion
        if name is not None:
            self._name = name
        if numberOfFeatures is not None:
            self._numberOfFeatures = numberOfFeatures
        if path is not None:
            self._path = path
        if rows_count is not None:
            self._rows_count = rows_count
        if type is not None:
            self._geometryType = type

        # warn about unsupported attributes
        if len(kwargs):
            logger.warning(
                "Folllowing fields were not expected and have been ignored. "
                "Maybe consider adding them to the model: {}. Object name: {}".format(
                    " | ".join(kwargs.keys()), name
                )
            )

    # -- PROPERTIES --------------------------------------------------------------------
    # attributes
    @property
    def attributes(self) -> int:
        """Gets the attributes.

        :return: The attributes.
        :rtype: int
        """
        return self._attributes

    @attributes.setter
    def attributes(self, attributes: int):
        """Sets the attributes.

        :param int attributes: The attributes.
        """

        self._attributes = attributes

    # bands properties
    @property
    def bands(self) -> list:
        """Gets the bands.

        :return: The bands.
        :rtype: list
        """
        return self._bands

    @bands.setter
    def bands(self, bands: list):
        """Sets the bands.

        :param list bands: The bands.
        """

        self._bands = bands

    # bands count
    @property
    def bands_count(self) -> list:
        """Gets the bands_count.

        :return: The bands_count.
        :rtype: list
        """
        return self._bands_count

    @bands_count.setter
    def bands_count(self, bands_count: list):
        """Sets the bands_count.

        :param list bands_count: The bands_count.
        """

        self._bands_count = bands_count

    # Bounding Box
    @property
    def bbox(self) -> dict:
        """Gets the bbox of this Metadata.

        :return: The bbox of this Metadata.
        :rtype: dict
        """
        return self._bbox

    @bbox.setter
    def bbox(self, bbox: dict):
        """Sets the coordinate systems of this Metadata.

        :param dict bbox: to be set
        """

        self._bbox = bbox

    # cols count
    @property
    def cols_count(self) -> list:
        """Gets the cols_count.

        :return: The cols_count.
        :rtype: list
        """
        return self._cols_count

    @cols_count.setter
    def cols_count(self, cols_count: list):
        """Sets the cols_count.

        :param list cols_count: The cols_count.
        """

        self._cols_count = cols_count

    # coordinateSystem
    @property
    def coordsys(self) -> dict:
        """Gets the coordsys of this Metadata.

        :return: The coordsys of this Metadata.
        :rtype: dict
        """
        return self._coordsys

    @coordsys.setter
    def coordsys(self, coordsys: dict):
        """Sets the coordinate systems of this Metadata.

        :param dict coordsys: to be set
        """

        self._coordsys = coordsys

    # related data sources
    @property
    def dataSources(self) -> list:
        """Gets the dataSources.

        :return: The dataSources of this Metadata.
        :rtype: list
        """
        return self._dataSources

    @dataSources.setter
    def dataSources(self, dataSources: list):
        """Sets the dataSources.

        :param list dataSources: the dataSources of this Metadata.
        """

        self._dataSources = dataSources

    # metadata description
    @property
    def description(self) -> str:
        """Gets the description.

        :return: The description of this Metadata.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description: str):
        """Sets the description used into Isogeo filters of this Metadata.

        :param str description: the description of this Metadata.
        """

        self._description = description

    # search envelope
    @property
    def envelope(self) -> dict:
        """Gets the abilities.

        :return: The abilities.
        :rtype: dict
        """
        return self._envelope

    @envelope.setter
    def envelope(self, envelope: dict):
        """Sets the envelope of this InlineResponse2001.

        The aggregated convex hull for the entire serach numberOfFeatures. \
        Might be null (if the numberOfFeatures span the entire globe, for instance).  # noqa: E501

        :param envelope: The envelope of this InlineResponse2001.  # noqa: E501
        :type: object
        """

        self._envelope = envelope

    # FME Environment
    @property
    def fmeEnv(self) -> dict:
        """Gets the modified.

        :return: The modified.
        :rtype: dict
        """
        return self._fmeEnv

    @fmeEnv.setter
    def fmeEnv(self, fmeEnv: dict):
        """Sets the fmeEnv of this InlineResponse2001.

        :param fmeEnv: The fmeEnv of this InlineResponse2001.  # noqa: E501
        :type: object
        """

        self._fmeEnv = fmeEnv

    # formatShort UUID
    @property
    def formatShort(self) -> str:
        """Gets the formatShort.

        :return: The formatShort.
        :rtype: str
        """
        return self._formatShort

    @formatShort.setter
    def formatShort(self, formatShort: str):
        """Sets the formatShort.

        :param str formatShort: The formatShort.
        """

        self._formatShort = formatShort

    # search last modification date
    @property
    def formatLong(self) -> str:
        """Gets the modified.

        :return: The modified.
        :rtype: str
        """
        return self._formatLong

    @formatLong.setter
    def formatLong(self, formatLong: str):
        """Sets the formatLong.

        :param str formatLong: The formatLong
        """

        self._formatLong = formatLong

    @property
    def formatVersion(self) -> str:
        """Gets the format version.

        :return: the format version.
        :rtype: str
        """
        return self._formatVersion

    @formatVersion.setter
    def formatVersion(self, formatVersion: str):
        """Sets the formatVersion.

        :param str formatVersion: format version
        """

        self._formatVersion = formatVersion

    # geometry type = type
    @property
    def geometryType(self) -> str:
        """Gets the type of geometry of the described dataset. \
        It's mapped from the `type` attribute in Scan output.

        :return: the type of geometry of the described dataset.
        :rtype: str
        """
        return self._geometryType

    @geometryType.setter
    def geometryType(self, geometryType: str):
        """Sets the type of geometry of the described dataset.

        :param str geometryType: the type of geometry of the described dataset.
        """

        # check type value
        self._geometryType = geometryType

    # search creation date
    @property
    def name(self) -> int:
        """Gets the created.

        :return: The created.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: int):
        """Sets the name of this InlineResponse2001.

        :param int name: The name
        """

        self._name = name

    # search numberOfFeatures path
    @property
    def numberOfFeatures(self) -> int:
        """Gets the tag.

        :return: The tag.
        :rtype: int
        """
        return self._numberOfFeatures

    @numberOfFeatures.setter
    def numberOfFeatures(self, numberOfFeatures: int):
        """Sets the numberOfFeatures of this InlineResponse2001.

        :param int numberOfFeatures: The numberOfFeatures of this InlineResponse2001.  # noqa: E501
        """

        self._numberOfFeatures = numberOfFeatures

    # path
    @property
    def path(self) -> dict:
        """Gets the path.

        :return: The path.
        :rtype: dict
        """
        return self._path

    @path.setter
    def path(self, path: dict):
        """Sets the path of this InlineResponse2001.

        The aggregated set of path for the entire search numberOfFeatures  # noqa: E501

        :param path: The path of this InlineResponse2001.  # noqa: E501
        :type: path
        """

        self._path = path

    # rows count
    @property
    def rows_count(self) -> list:
        """Gets the rows_count.

        :return: The rows_count.
        :rtype: list
        """
        return self._rows_count

    @rows_count.setter
    def rows_count(self, rows_count: list):
        """Sets the rows_count.

        :param list rows_count: The rows_count.
        """

        self._rows_count = rows_count

    # -- SPECIFIC TO IMPLEMENTATION ----------------------------------------------------
    @property
    def isMapDocument(self) -> bool:
        """Determine if the metadata is about a map document containing datasets\
             (like *.mxd, *.lyr, etc.) and not a single dataset."""
        if self._dataSources is not None:
            return True
        else:
            return False

    @property
    def isRaster(self) -> bool:
        """Determine if the metadata describes a raster dataset."""
        if (
            self._bands is not None
            and not self._numberOfFeatures
            and not self.isMapDocument
        ):
            return True
        else:
            return False

    @property
    def isVector(self) -> bool:
        """Determine if the metadata describes a vector dataset."""
        if not self._bands_count and self._numberOfFeatures and not self.isMapDocument:
            return True
        else:
            return False

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
        if issubclass(Lookup, dict):
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
        if not isinstance(other, Lookup):
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
    sample = Lookup()
