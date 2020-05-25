import logging
import re
from copy import copy
from enum import IntEnum
from inspect import signature, Parameter
from typing import (
    List,
    Tuple,
    Union,
    Optional,
    Dict,
    Callable)

from pandas import DataFrame

_logger = logging.getLogger("augmentedtree")

_augmentation_classes = {}
_mappingtree_json_schemas = {}
_type_defined_augmentation_methods = {}
_detect_multiple_delimiter = re.compile("/+")
_valid_path_part_types = (str, int, float)


AUGMENTATION_FOR_MAPPING = "mapping"
AUGMENTATION_FOR_SEQUENCE = "sequence"
AUGMENTATION_FOR_VALUES = "any"
AUGMENTATION_ROOT_KEY = "@root"

ALL_ITEMS = slice(None, None, None)

IGNORE_PREFIX = "_"

PRIMARYKEY_KEY = "__key"
"""
The primary key is the `key` with which the data items representative 
value is shown.
"""

PRIMARYNAME_KEY = "__name"
"""
The primary name is the the representative value shown for the data item.
"""

PRIMARYVALUE_KEY = "__value"
"""
The primary value is the primary data structure of the data item.
"""


class NotSupportedError(Exception):
    pass


class MappingSchema:
    PRIMARYKEY: str = "atree_primekey"
    """
    Defines the field from which value should be used as `primekey` of 
    the `MappingTreeItem`.
    """

    PRIMARYNAME: str = "atree_primename"
    """
    Defines the field from which value should be used as `primename` of
    the `MappingTreeItem`.
    """

    OUTERVALUES: str = "atree_outervalues"
    """
    Defines the field from which value should be used as `primename` of
    the `MappingTreeItem`.
    """

    METAFIELDKEYS: str = "atree_metafieldkeys"
    """
    Defines the keys of a Mapping item which should be treated as
    'metadata' of this item. 'metadata' is hidden within the augmented
    default view.
    """

    IDENTIFIER: str = "atree_mappingschema"
    """
    This field defines the unique schema identifier by an tuple of
    (key, value), which has to be found within the Mapping item.

    Optionally if the field only contains a string, it is assumed the
    Mapping item contains this MappingTree.SCHEMA_IDENTIFIER as a key
    of an value with a unique name.
    """

    META_ATTRIBUTES: str = "atree.meta_attributes"


class ClassAugmentationSchema(object):
    Default = "default"
    QtSupport = "qt"


class MappingSchemaBuilder(object):
    IDENTIFIER = "identifier"
    PRIMARYKEY = "primarykey"
    PRIMARYNAME = "primaryname"
    OUTERVALUES_KEY = "outervalues_key"
    METAATTRIBUTES = "meta_attributes"

    @staticmethod
    def construct(
        identifier: Union[str, Tuple[str, str]],
        primarykey: Optional[str] = None,
        primaryname: Optional[str] = None,
        outervalues_key: Optional[str] = None,
        metafieldkeys: Optional[List[str]] = None,
        additional_metafieldkeys: Optional[List[str]] = None,
        meta_attributes: Optional[List[str]] = None,
    ) -> dict:
        """
        Construct a schema for MappingTreeItems.

        Notes:
            - If identifier is a single string the mapping to be used by this
              schema needs a field with the key `MappingSchema.IDENTIFIER`.

            - A mapping item can use `outervalues` or `metafieldkeys` therefore
              `outervalues_key` always suppress `metafieldkeys` and
              `additional_metafieldkeys`.

            - The identifiers resulting key, `primarykey` and `primaryname`
              are default `metafieldkeys` if supplied. The `metafieldkeys`
              overrides the default behavior.

            - With `additional_metafieldkeys` additional keys can be defined.

        Args:
            identifier (Union[str, Tuple[str, str]]):
                A single string or a tuple/list with 2 strings defines an
                identifier.

            primarykey (Optional[str]):
                Defines which key of the mapping should be used as the tree
                items `primekey`.

            primaryname (Optional[str]):
                Defines which key of the mapping should be used as the tree
                items `primename`.

            outervalues_key (Optional[str]):
                Defines the key, which contains the tree items children/values
                resulting in a 'nested-mapping' tree item.

            metafieldkeys (Optional[List[str]]):
                Defines the keys, which will be considered as metadata. All
                other entries within the mapping will be considered as a
                child/value.

            additional_metafieldkeys:
                Additional keys to `metafieldkeys`.

            meta_attributes (Optional[List[str]]):
                Defines which values will be used as meta attributes for
                selection via the `where` method.

        Returns:
            dict:
                A schema for MappingTreeItem(s).
        """
        identifier_error_msg = (
            "A schema identifier needs to be a single string "
            "or a two item `list`/`tuple`. Items need to be string."
        )
        if isinstance(identifier, str):
            schema = {MappingSchema.IDENTIFIER: identifier}
        elif isinstance(identifier, (list, tuple)):
            used_identifier = "'Error: No-valid-identifier-declared.'"
            try:
                if isinstance(identifier[0], str) and isinstance(identifier[1], str):
                    used_identifier = (str(identifier[0]), str(identifier[1]))
            except (TypeError, IndexError, KeyError):
                identifier_error_msg += " Got less then 2 items."
                raise ValueError(identifier_error_msg)
            schema = {MappingSchema.IDENTIFIER: used_identifier}
        else:
            raise ValueError(
                identifier_error_msg + " Got '{}'".format(type(identifier))
            )

        resulting_metafieldkeys = [identifier[0]]
        if primarykey is not None:
            schema[MappingSchema.PRIMARYKEY] = primarykey
            resulting_metafieldkeys.append(primarykey)
        if primaryname is not None:
            schema[MappingSchema.PRIMARYNAME] = primaryname
            resulting_metafieldkeys.append(primaryname)

        # if user defined metafieldkeys then these override the default definition
        # else the user does only need to define additional keys.
        if metafieldkeys:
            resulting_metafieldkeys = copy(metafieldkeys)
        if additional_metafieldkeys:
            resulting_metafieldkeys.extend(additional_metafieldkeys)
            resulting_metafieldkeys = list(set(resulting_metafieldkeys))

        if outervalues_key is not None:
            schema[MappingSchema.OUTERVALUES] = outervalues_key
        elif resulting_metafieldkeys is not None:
            schema[MappingSchema.METAFIELDKEYS] = resulting_metafieldkeys
        if meta_attributes is not None:
            schema[MappingSchema.META_ATTRIBUTES] = meta_attributes
        return schema

    @staticmethod
    def construct_from_collection(kwargs_of_schemas: Union[List, dict]):
        schemas = []
        if isinstance(kwargs_of_schemas, dict):
            for key, schema_kwargs in kwargs_of_schemas.items():
                if not MappingSchemaBuilder.parameters_are_valid(schema_kwargs):
                    continue
                schema = MappingSchemaBuilder.construct(**schema_kwargs)
                schemas.append(schema)
        elif isinstance(kwargs_of_schemas, list):
            for schema_kwargs in kwargs_of_schemas:
                if not MappingSchemaBuilder.parameters_are_valid(schema_kwargs):
                    continue
                schema = MappingSchemaBuilder.construct(**schema_kwargs)
                schemas.append(schema)
        return schemas

    @staticmethod
    def parameters_are_valid(schema_kwargs):
        # Identifier is mandatory
        if MappingSchemaBuilder.IDENTIFIER not in schema_kwargs:
            return False
        single_mandatory_fields = [
            MappingSchemaBuilder.OUTERVALUES_KEY,
            MappingSchemaBuilder.PRIMARYKEY,
            MappingSchemaBuilder.PRIMARYNAME,
            MappingSchemaBuilder.METAATTRIBUTES,
        ]
        for single_mandatory_field in single_mandatory_fields:
            if single_mandatory_field in schema_kwargs:
                return True
        return False


class TreeItemParameters:
    PRIMARYKEY = "primarykey"
    """
    The primary key is the `key` with which the data items
    representative value is shown.
    """

    PRIMARYNAME = "primaryname"
    """
    The primary name is the the representative value shown for the data
    item.
    """

    PRIMARYVALUE = "primaryvalue"
    """
    The primary value is the primary data structure of the data item.
    """

    OUTERVALUEKEY = "outervaluekey"
    """
    Key of field holding the values, which should be represented as
    values.
    """

    METADATAKEYS = "metadatakeys"
    """
    Fields which should be treatend as metadata (inner values).
    """

    META_ATTRIBUTES = "meta_attributes"
    """
    Mapping only; Fields which values will be used to associate
    data with.
    """

    REAL_KEY = "real_key"
    """
    The item's real key/index within the nested structure.
    """

    __ROOT = "__root"
    """
    This is used to pass a tree's root to all items.
    """


class LeafType(IntEnum):
    VIRTUAL = 0
    VALUE = 1
    CONTAINER = 2
    SEQUENCE = 4
    MAPPING = 8


def use_mappingtree_schema(schema: Dict, override_existing: bool = False):
    """
    Registers a (JSON-)schema for a `MappingTreeItem` for global use.

    Raises:
        ValueError:
            If a schema with the same identifier is already registered.

    Args:
        schema (Dict):
            (JSON-)schema to be registered.

        override_existing(bool):
            If `True` and existing registered schema with the same id
            will be overridden.
    """
    global _mappingtree_json_schemas
    schema_uid = None
    try:
        schema_uid = schema[MappingSchema.IDENTIFIER]
    except KeyError:
        ValueError(
            "The given JSON-schema for mapping trees is not sufficient defined."
            "The field '{}' for the unique schema identifier is missing."
            "".format(MappingSchema.IDENTIFIER)
        )
    if isinstance(schema_uid, list):
        schema_uid = tuple(schema_uid)
    if not isinstance(schema_uid, tuple):
        schema_key = MappingSchema.IDENTIFIER
        schema_uid = (schema_key, schema[MappingSchema.IDENTIFIER])
    else:
        schema_key = schema_uid[0]

    if schema_key not in _mappingtree_json_schemas:
        _mappingtree_json_schemas[schema_key] = {}
    schemas_at_schema_key = _mappingtree_json_schemas[schema_key]

    if not override_existing and (schema_uid in schemas_at_schema_key):
        _logger.info(
            "An schema with the identifier '{}' is already existing. Existing schema "
            "will be used instead given."
        )
        return
    schemas_at_schema_key[schema_uid] = schema


# noinspection PyTypeChecker
def use_mappingtree_schemas(*schemas: List[Dict], override_existing: bool = False):
    """
    Registers (JSON-)schemas for a `MappingTreeItem` for global use.

    Raises:
        ValueError:
            If a schema with the same identifier is already registered.

    Args:
        schemas (List[Dict]):
            (JSON-)schemas to be registered.
        
        override_existing(bool):
            If `True` and existing registered schema with the same id
            will be overridden.
    """
    for unregistered_schema in schemas:
        use_mappingtree_schema(unregistered_schema, override_existing)


def _find_schema(
    datastructure: dict,
) -> Tuple[Optional[Tuple[str, str]], Optional[dict]]:
    """
    Retrives the schema for the given `datastructure`.

    Args:
        datastructure(dict):
            Mapping for which a schema shall be found.

    Returns:
        Tuple[Optional[str], Optional[dict]]:
            Unique identifier of and the (Json-)schema of given
            `datastructure`, ``(None, None)``.
    """
    global _mappingtree_json_schemas
    for schema_key in _mappingtree_json_schemas:
        if schema_key not in datastructure:
            continue
        schema_name = datastructure[schema_key]
        schema_uid = (schema_key, schema_name)
        schemas_of_schemakey = _mappingtree_json_schemas[schema_key]
        if schema_uid in schemas_of_schemakey:
            return schema_uid, schemas_of_schemakey[schema_uid]
    return None, None


def _inspect_required_keywords(func, required_args: List[str]) -> bool:
    """
    Inspects given function for required arguments and raises
    NotImplementedError in case function doesn't meet required arguments.

    Args:
        func(function):
            function to inspect

        required_args (list of str):
            List of required argument to be defined by func.

    Raises:
        NotImplementedError
    """
    sig = signature(func)
    # Minimal allowed parameter declaration is **kwargs
    params = [param for param in sig.parameters.values()]
    paramnames = [param.name for param in params]
    msg = "The function {} does require the keywordarguments " "'{}'".format(
        func.__name__, "', '".join(required_args)
    )
    if len(params) == 0:
        raise NotImplementedError(msg)
    # next minimal parameter declaration are the required parameters
    if len(params) > 1 and params[0].kind != Parameter.VAR_KEYWORD:
        for arg in required_args:
            if arg not in paramnames:
                raise NotImplementedError(msg)
    return True


def use_augmentation_method_for_type(schema_uid: dict, target: Callable):
    """
    Registers a (JSON-)schema for a `MappingTreeItem` for global use.

    Args:
        schema_uid (dict):
            Id of json-schema for which a specific augmentation method,
            should be used.

        target (Callable):
            Method, which is used to augment the specific type.
    """
    global _type_defined_augmentation_methods
    if schema_uid in _type_defined_augmentation_methods:
        raise ValueError(
            "Identifer '{}' already exists within registered schemas."
            "".format(schema_uid)
        )
    augmentationkeys = ["parent", "childskey", "datastructure", "augmentclasses"]
    if not _inspect_required_keywords(target, augmentationkeys):
        pars = "', '".join(augmentationkeys)
        raise TypeError("The target method needs the parameters '{}'".format(pars))
    _type_defined_augmentation_methods[schema_uid] = target


def get_augmentation_method_for_type(schema_id: str) -> Callable:
    """
    Retrives the augmentation method for the given `schema_id`.

    Args:
        schema_id(str):
            Identifier of this schema.

    Raises:
        KeyError if schema_id is not registered.

    Returns:
        dict:
            Json-schema of given `schema_id`
    """
    global _type_defined_augmentation_methods
    return _type_defined_augmentation_methods[schema_id]


def get_augmentation_classes(usecase=None):
    if usecase is None:
        usecase = ClassAugmentationSchema.Default
    global _augmentation_classes
    return _augmentation_classes[usecase]


def set_augmentation_classes(usecase, class_type, augmentation_class):
    global _augmentation_classes
    if usecase not in _augmentation_classes:
        _augmentation_classes[usecase] = {}
    _augmentation_classes[usecase][class_type] = augmentation_class


def normalize_path_of_tree(*treepath: Union[str, List[str]]):
    """
    Normalized a path (str) or parts of a path (List[str]) to
    '/a/path/like/this'.

    Args:
        *treepath:
            A single tree path part or multiple tree path parts.

    Returns:
        str:
            Normalized path '/like/this/example'.
    """
    first_item_is_the_path_in_parts = (
        len(treepath) == 1
        and isinstance(treepath[0], (list, tuple))
    )
    if first_item_is_the_path_in_parts:
        return normalize_path_of_tree(*treepath[0])

    if not treepath:
        return ""
    convert_path = [
        str(part) for part in treepath
        if isinstance(part, _valid_path_part_types)
    ]
    joined_path = TreePath.DELIMITER.join(convert_path)

    normalized_path = _detect_multiple_delimiter.sub("/", joined_path)
    if not normalized_path:
        return ""

    last_char = -1
    first_char = 0
    all_except_last = slice(None, -1, None)

    path_ends_with_delimiter = normalized_path[last_char] == TreePath.DELIMITER
    if path_ends_with_delimiter:
        normalized_path = normalized_path[all_except_last]

    path_starts_with_delimiter = normalized_path[first_char] == TreePath.DELIMITER
    if not path_starts_with_delimiter:
        normalized_path = TreePath.DELIMITER + normalized_path

    return normalized_path


class TreePath(object):
    DELIMITER = "/"

    def __init__(
        self,
        real_path: Union[str, List[str]] = "",
        augmented_path: Union[str, List[str]] = "",
        meta_attributes: List = None,
    ):
        """
        Defines a path within a nested data structure of `sequence` and
        `mapping`.

        Args:
            real_path (str):
                The real path within the data structure.

            augmented_path (str):
                The path which is depicted by the augmentation.

            meta_attributes (List):
                Additional attributes of this tree item, which should
                refer to this path.
        """
        self.real_path = normalize_path_of_tree(real_path)
        self.augmented_path = normalize_path_of_tree(augmented_path)
        self.real_key = self.real_path.split(TreePath.DELIMITER)[-1]
        self.primekey = self.augmented_path.split(TreePath.DELIMITER)[-1]
        if meta_attributes is not None:
            self.meta_attributes = meta_attributes
        else:
            self.meta_attributes = []

    def get_real_path(self):
        parts = self.real_path.split(TreePath.DELIMITER)
        result = [part for part in parts if part]
        return result

    def get_augmented_path(self):
        parts = self.augmented_path.split(TreePath.DELIMITER)
        result = [part for part in parts if part]
        return result

    def __iter__(self):
        yield self.real_path
        yield self.augmented_path
        return self.meta_attributes

    def __next__(self):
        return next([self.real_path, self.augmented_path, self.meta_attributes])

    def join(
        self,
        real_path: Union[str, List[str]] = "",
        augmented_path: Union[str, List[str]] = "",
        meta_attributes: List = None,
    ) -> "TreePath":
        """
        Joins the path parts and returns a new AugmentedTreePath.

        Notes:
            If parameter `treepath` is given, all parameters are overriden by it.

        Args:
            real_path (Union[str, List[str]]):
                Real path within the nested data structure of the augmented tree items.

            augmented_path (Union[str, List[str]]):
                Path defined by the augmentation; if no schemas are used identical to
                *real_path*

            meta_attributes (List):
                Associations of this path part.

        Returns:
            TreePath:
                Path within augmented tree.
        """
        real_path_addition = normalize_path_of_tree(real_path)
        augmented_path_addition = normalize_path_of_tree(augmented_path)

        childs_real_path = normalize_path_of_tree([self.real_path, real_path_addition])
        childs_augmented_path = normalize_path_of_tree(
            [self.augmented_path, augmented_path_addition]
        )
        parents_meta_attributes = self.meta_attributes.copy()
        if meta_attributes is not None:
            parents_meta_attributes.extend(meta_attributes)

        new_sub_path = TreePath(
            real_path=childs_real_path,
            augmented_path=childs_augmented_path,
            meta_attributes=parents_meta_attributes,
        )
        return new_sub_path

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.real_path)


class TreePathMap(object):
    """
    A 'map' like object of all tree paths of an AugmentedTree.
    """
    def __init__(self):
        self._key_and_path_table = DataFrame()


class KeyLink(object):
    """
    Provides a link to a data object with an key.
    """

    def __init__(self, key):
        self._data = None
        self.key = key
        self.is_from_parent = False

    def is_linked(self) -> bool:
        return self._data is not None

    def link(self, data):
        self._data = data

    def __call__(self):
        return self._data[self.key]

    def change_value_of_key(self, new_value) -> bool:
        if self.key == PRIMARYKEY_KEY:
            return False
        self._data[self.key] = new_value
        return self._data[self.key] == new_value
