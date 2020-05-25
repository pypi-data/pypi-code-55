# -*- coding: utf-8 -*-
"""
This module contains
"""
import collections
import json
import warnings
import copy
from collections import MutableSequence
from collections.abc import Mapping
from typing import (
    Any,
    Dict,
    Callable,
    Generator,
    List,
    Union,
    Sequence,
    Optional,
    Tuple,
    Hashable, Iterable)

from augmentedtree.abstractbaseclasses import AnAugmentedTreeItem, AnAugmentedCollection
from augmentedtree.augmentation import _augment, augment_datastructure, print_atree
from augmentedtree.core import (
    LeafType,
    get_augmentation_classes,
    PRIMARYKEY_KEY,
    PRIMARYNAME_KEY,
    PRIMARYVALUE_KEY,
    TreePath,
    NotSupportedError,
    KeyLink)

INNER_VALUE_MARKER_PREFIX = "@"
FIELDS_FOR_META_ATTRIBUTES = "__meta_attributes"


class TreeItems(collections.abc.Sequence):
    """
    This class supports indexing by primekeys of tree items returning a
    AnAugmentedTreeItem.
    """

    def __init__(self, parent: AnAugmentedTreeItem):
        """
        Provides indexing with primekeys.

        Args:
            parent(AnAugmentedTreeItem):
                Providing indexing for this `parent` item.
        """
        self._parent = parent

    def __getitem__(self, primary_key) -> AnAugmentedTreeItem:
        if isinstance(primary_key, slice):
            raise NotImplementedError("Slicing is not supported ... yet.")
        treeitem = self._parent.get_child(primary_key)
        return treeitem

    def __len__(self):
        return self._parent.children_count()

    def __iter__(self,) -> Generator[AnAugmentedTreeItem, None, None]:
        for child in self._parent.iter_children():
            yield child

    def __contains__(self, item: AnAugmentedTreeItem) -> bool:
        has_child = self._parent.has_primekey(item.primekey)
        return has_child


class ATreeItem(AnAugmentedTreeItem):
    """
    `ATreeItem` set the entry point for subclassing
    `AnAugmentedTreeItem` for usage with `augment_datastructure`. It
    also implements properties and methods for convenience. Properties
    and methods which has to be overwritten will raise
    NotImplementedErrors.

    Raises:
        TypeError:
            This class cannot be instantiated directly. It has to be
            sub-classed.
    """

    def __new__(
        cls,
        primarykey: Union[str, int],
        primaryname: Union[str, int] = None,
        primaryvalue: Any = None,
        outervaluekey: str = None,
        metadatakeys: List[str] = None,
        real_key: Union[int, str] = None,
        **kwargs
    ):
        if cls is ATreeItem:
            raise TypeError("Cannot instantiate ATreeItem directly.")
        return object.__new__(cls)

    def __init__(self, real_key=None, **kwargs):
        self._parent: Optional[AnAugmentedCollection] = None
        self._treeitems = TreeItems(self)
        self._real_key = real_key

    @property
    def primekey(self) -> Union[int, str]:
        raise NotImplementedError(
            "{} needs to override `primekey`.".format(self.__class__.__name__)
        )

    @property
    def primename(self) -> Any:
        raise NotImplementedError(
            "{} needs to override `PrimeName`.".format(self.__class__.__name__)
        )

    @property
    def primevalue(self) -> Any:
        raise NotImplementedError(
            "{} needs to override `PrimeName`.".format(self.__class__.__name__)
        )

    def data(self, column: Union[str, int]) -> Any:
        raise NotImplementedError(
            "{} needs to override `data`.".format(self.__class__.__name__)
        )

    @property
    def real_key(self) -> Union[int, str]:
        """
        The real key within the nested data.

        Returns:
            Union[int, str]
        """
        raise NotImplementedError(
            "{} needs to override `real_key`.".format(self.__class__.__name__)
        )

    @property
    def leaf_type(self) -> LeafType:
        raise NotImplementedError(
            "{} needs to override `leaf_type`.".format(self.__class__.__name__)
        )

    @property
    def parent(self) -> Optional[AnAugmentedCollection]:
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @property
    def children(self,) -> Sequence:
        return self._treeitems

    def iter_children(self,) -> Generator["AnAugmentedTreeItem", None, None]:
        raise NotImplementedError(
            "{} needs to override `iter_children`.".format(self.__class__.__name__)
        )

    def insert_child_at(self, position, child):
        raise NotImplementedError(
            "{} needs to override `insertChildAt`.".format(self.__class__.__name__)
        )

    def has_primekey(self, key: Union[int, str]) -> bool:
        raise NotImplementedError(
            "{} needs to override `hasKey`.".format(self.__class__.__name__)
        )

    def get_child(self, primary_key: str) -> AnAugmentedTreeItem:
        raise NotImplementedError(
            "{} needs to override `get_child`.".format(self.__class__.__name__)
        )

    def children_count(self) -> int:
        raise NotImplementedError(
            "{} needs to override `children_count`.".format(self.__class__.__name__)
        )

    def get_pathmap(
        self, parent_path: TreePath = None, section_root_path: TreePath = None
    ):
        msg = (
            "get_pathmap() will be deprecated in future releases. The"
            " backend related to selection of tree items will"
            " be reworked, keeping its current interface."
        )
        warnings.warn(msg, DeprecationWarning)
        raise NotImplementedError(
            "{} needs to override `get_pathmap`.".format(self.__class__.__name__)
        )

    def print(
        self,
        additional_columns: List = None,
        show_hidden: bool = False,
        indent: str = "  ",
        prefix: str = "",
    ):
        print_atree(
            self,
            additional_columns=additional_columns,
            show_hidden=show_hidden,
            indent=indent,
            prefix=prefix,
        )

    def __str__(self):
        return "{}({})".format(self.__class__.__name__, self.primevalue)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.primevalue)


# Inherits abstract methods from ATreeItem
# noinspection PyAbstractClass
class ACollectionTreeItem(AnAugmentedCollection, ATreeItem):
    def __new__(
        cls,
        primarykey: Union[KeyLink, str, int],
        primaryname: Union[KeyLink, str, int] = None,
        primaryvalue: Union[Sequence, Mapping] = None,
        outervaluekey: str = None,
        metadatakeys: List[str] = None,
        real_key: Union[int, str] = None,
        **kwargs
    ):
        if cls is ATreeItem:
            raise TypeError("Cannot instantiate ACollectionTreeItem directly.")
        return object.__new__(cls)

    def __init__(
        self,
        primarykey: Union[KeyLink, str, int] = None,
        primaryname: Union[KeyLink, str, int] = None,
        primaryvalue: Union[Sequence, Mapping] = None,
        real_key: str = None,
        **kwargs
    ):
        super().__init__()

        self._data = {PRIMARYVALUE_KEY: primaryvalue}

        if isinstance(primarykey, KeyLink):
            self._primarykeylink = primarykey
            self._primarykeylink.link(primaryvalue)
        else:
            self._primarykeylink = KeyLink(PRIMARYKEY_KEY)
            self._primarykeylink.link(self._data)
            self._data[PRIMARYKEY_KEY] = primarykey

        if isinstance(primaryname, KeyLink):
            self._primarynamelink = primaryname
            self._primarynamelink.link(primaryvalue)
        else:
            self._primarynamelink = KeyLink(PRIMARYNAME_KEY)
            self._primarynamelink.link(self._data)
            self._data[PRIMARYNAME_KEY] = primaryname

        if isinstance(real_key, (str, int)):
            self._real_key = real_key
        elif isinstance(primarykey, (str, int)):
            self._real_key = primarykey
        else:
            raise ValueError(
                "Defining a proper `real_key` of ACollectionTreeItem is"
                " mandatory. If no `real_key` is provided the `primarykey`"
                " needs to be a int or str and cannot be a `KeyLink`."
                " Please provide a proper key."
            )

    def __getitem__(self, key_or_index):
        raise NotImplementedError(
            "{} needs to override `__getitem__`.".format(self.__class__.__name__)
        )

    def __setitem__(self, key, value):
        raise NotImplementedError(
            "{} needs to override `__setitem__`.".format(self.__class__.__name__)
        )

    @property
    def outervalues(self):
        raise NotImplementedError(
            "{} needs to override `outervalues`.".format(self.__class__.__name__)
        )


# noinspection PyUnreachableCode
class ValueTreeItem(ATreeItem):
    def __init__(self, primarykey=None, **metadata):
        super().__init__(primarykey=primarykey, primaryname=None, primaryvalue=None)
        assert not isinstance(
            primarykey, KeyLink
        ), "KeyLink is not allowed for ValueItems"
        self._data = {PRIMARYKEY_KEY: primarykey}
        self._data.update(metadata)

    @property
    def unit(self):
        try:
            return self._data["unit"]
        except KeyError:
            return ""

    @property
    def indexes(self):
        try:
            return self._data["index"]
        except KeyError:
            return [1]

    @property
    def real_key(self) -> Union[int, str]:
        return self._data[PRIMARYKEY_KEY]

    @property
    def primekey(self):
        return self._data[PRIMARYKEY_KEY]

    @property
    def primename(self):
        return self.parent.outervalues[self._data[PRIMARYKEY_KEY]]

    @property
    def primevalue(self):
        return self.parent.outervalues[self._data[PRIMARYKEY_KEY]]

    # noinspection PyUnreachableCode
    @property
    def children(self) -> Generator[AnAugmentedTreeItem, None, None]:
        # Value items do not have children.
        return
        yield

    def iter_children(self) -> Generator["AnAugmentedTreeItem", None, None]:
        return
        yield

    def get_child(self, primary_key: str) -> AnAugmentedTreeItem:
        raise NotSupportedError(
            "A ValueTreeItem does not has children. This method"
            "should never been called."
        )

    @property
    def leaf_type(self) -> LeafType:
        return LeafType.VALUE

    def get_pathmap(
        self, parent_path: TreePath = None, section_root_path: TreePath = None
    ):
        assert parent_path is not None, "A _parent_path of a value cannot be None"
        mypath = parent_path.join(
            real_path=self.real_key, augmented_path=self.primekey,
        )
        return [(mypath, self.parent)]

    def data(self, column: str) -> Any:
        if column == PRIMARYKEY_KEY:
            return self._data[PRIMARYKEY_KEY]
        assert self.parent is not None, "This element should have a parent."
        if column == PRIMARYVALUE_KEY or column == PRIMARYNAME_KEY:
            value = self.parent.outervalues[self.primekey]
            return value
        try:
            return self._data[column]
        except (KeyError, TypeError):
            pass
        return self.parent.data(column)

    def insert_child_at(self, position, child):
        raise NotSupportedError(
            "A leaf cannot has children. This method should not have been called."
        )

    def has_primekey(self, key):
        raise NotSupportedError(
            "A leaf cannot has children. This method should not have been called."
        )

    def __str__(self):
        return self.__repr__()
        # if self.parent is None:
        #     output = "{}({})".format(self.__class__.__name__, self.primekey)
        # else:
        #     output = "{}({}: {})".format(
        #         self.__class__.__name__,
        #         self.primekey,
        #         self.parent.outervalues[self.primekey],
        #     )
        # return output

    def __repr__(self):
        output = "{}({}: {})".format(
            self.__class__.__name__,
            self.primekey,
            self.parent.outervalues[self.primekey],
        )
        return output
        # if self.leaf_type == LeafType.VALUE:
        #     if self.parent is None:
        #         return None
        #     representation = str(self.parent[self.primekey])
        #     return representation

    def children_count(self) -> int:
        """
        Value items do not posses children.

        Returns:
            int:
                Returning 0, since value items do not posses children.
        """
        return 0


# noinspection PyMethodOverriding
class SequenceTreeItem(MutableSequence, ACollectionTreeItem):
    def __init__(
        self,
        primarykey=None,
        primaryname=None,
        primaryvalue=None,
        real_key=None,
        **kwargs
    ):
        super().__init__(
            primarykey=primarykey,
            primaryname="[...]",
            primaryvalue=primaryvalue,
            real_key=real_key,
        )
        self._children = []
        self._augemtationclasses = get_augmentation_classes()
        self._real_key = None
        self._data = None
        self._primarykeylink = None
        self._primarynamelink = None
        self.set_my_data(
            primarykey, primaryname, primaryvalue, real_key,
        )

    def __bool__(self):
        return len(self.primevalue) == 0

    def is_empty(self):
        return len(self.outervalues) == 0

    # This was defined by I don't remember why. I should have written better
    # code.
    # # convinient method
    # def is_empty(self):
    #     return ((self.primekey is None) and (self.primevalue is None)) or (
    #         self.primekey == ""
    #     )

    def set_my_data(
        self, primarykey=None, primaryname=None, primaryvalue=None, real_key=None,
    ):
        assert isinstance(
            primaryvalue, Sequence
        ), "value of a {} should be a dict but got {} instead.".format(
            self.__class__.__name__, type(primaryvalue)
        )

        self._data = {PRIMARYVALUE_KEY: primaryvalue}

        if isinstance(primarykey, KeyLink):
            self._primarykeylink = primarykey
            self._primarykeylink.link(primaryvalue)
        else:
            self._primarykeylink = KeyLink(PRIMARYKEY_KEY)
            self._primarykeylink.link(self._data)
            self._data[PRIMARYKEY_KEY] = primarykey

        if isinstance(primaryname, KeyLink):
            self._primarynamelink = primaryname
            self._primarynamelink.link(primaryvalue)
        else:
            self._primarynamelink = KeyLink(PRIMARYNAME_KEY)
            self._primarynamelink.link(self._data)
            self._data[PRIMARYNAME_KEY] = primaryname

        if real_key is not None:
            self._real_key = real_key
        else:
            self._real_key = primarykey

        assert self._primarykeylink.is_linked(), "Linking primarykey to data failed."
        assert self._primarynamelink.is_linked(), "Linking primeryname to data failed."

    def has_primekey(self, key):
        return key <= len(self._children)

    def insert_child_at(self, position, child) -> bool:
        self._children.insert(position, child)
        child.parent = self
        return True

    def get_child(self, primary_key: int) -> AnAugmentedTreeItem:
        return self._children[primary_key]

    # MutableSequence implementation
    def insert(self, index: int, item) -> None:
        pass

    # Sequence implementation
    def __getitem__(self, index: int):
        return self._data[PRIMARYVALUE_KEY][index]

    # MutableSequence implementation
    def __setitem__(self, index: int, value):
        # The current data container will be set with the new value.
        # In case the current container is a mapping, it has to be checked.
        # whether this key already existed of not.
        if type(index) is slice:
            raise NotImplementedError("Slicing in __set__ is not implemented yet.")
        _augment(self, index, value, self._augemtationclasses)
        self.primevalue[index] = value

    # MutableSequence implementation
    def __delitem__(self, i: slice) -> None:
        del self._data[PRIMARYVALUE_KEY][i]

    # MutableSequence implementation
    def __len__(self) -> int:
        return len(self._data[PRIMARYVALUE_KEY])

    # sequence implementation
    def __iter__(self):
        return iter(self._data[PRIMARYVALUE_KEY])

    def __next__(self):
        return next(self._data[PRIMARYVALUE_KEY])

    # mutable sequence implementation
    def pop(self, index):
        del self._children[index]
        return self._data[PRIMARYVALUE_KEY].pop(index)

    def remove(self, item) -> None:
        raise NotImplementedError("not yet {}".format(self.__class__.__name__))

    # mutable sequence implementation
    def append(self, item) -> None:
        mydata = self._data[PRIMARYVALUE_KEY]
        key = len(mydata)
        mydata.append(item)
        _augment(self, key, item)

    # sequence implementation
    def __reversed__(self):
        return self._data[PRIMARYVALUE_KEY].__reversed__()

    def extend(self, iterable) -> None:
        offset = len(self._data[PRIMARYVALUE_KEY])
        self._data[PRIMARYVALUE_KEY].extend(iterable)
        for index, item in enumerate(iterable):
            _augment(self, index + offset, item)

    # sequence implementation
    def __contains__(self, item):
        return self._data[PRIMARYVALUE_KEY].__contains__(item)

    # sequence implementation
    def clear(self):
        self._data[PRIMARYVALUE_KEY].clear()
        self._children.clear()

    @property
    def outervalues(self):
        return self._data[PRIMARYVALUE_KEY]

    @property
    def real_key(self) -> Union[int, str]:
        return self._real_key

    @property
    def primekey(self):
        return self._primarykeylink()

    @property
    def primename(self):
        return self._primarynamelink()

    @property
    def primevalue(self) -> dict:
        return self._data[PRIMARYVALUE_KEY]

    @property
    def leaf_type(self) -> LeafType:
        return LeafType.SEQUENCE

    @staticmethod
    def get_meta_attributes():
        """
        Sequences do not support meta attributes.

        Returns:
            list:
                Empty List
        """
        return []

    def data(self, column):
        if column == PRIMARYKEY_KEY:
            return self._primarykeylink()
        if column == PRIMARYNAME_KEY:
            return self._primarynamelink()
        if column == PRIMARYVALUE_KEY:
            return self.primevalue
        try:
            return self.primevalue[column]
        except (IndexError, TypeError):
            return None

    def children_count(self) -> int:
        """
        Value items do not posses children.

        Returns:
            int:
                Returning 0, since value items do not posses children.
        """
        return len(self._children)

    def iter_children(self) -> Generator[AnAugmentedTreeItem, None, None]:
        for child in self._children:
            yield child

    def get_pathmap(
        self, parent_path: TreePath = None, section_root_path: TreePath = None
    ):
        pathmap = []
        my_real_path = str(self.real_key)
        my_augmented_path = str(self.primekey)
        my_meta_attributes = self.get_meta_attributes()
        if parent_path is not None:
            my_treepath = parent_path.join(
                real_path=my_real_path,
                augmented_path=my_augmented_path,
                meta_attributes=my_meta_attributes,
            )
        else:
            my_treepath = TreePath(my_real_path, my_augmented_path, my_meta_attributes)
        if self.parent is not None:
            pathmap.append((my_treepath, self.parent))

        base_childs_path = my_treepath

        for child in self._children:
            childs_paths = child.get_pathmap(parent_path=base_childs_path)
            pathmap.extend(childs_paths)
        return pathmap


class MappingTreeItem(Mapping, ACollectionTreeItem):
    def __init__(
        self,
        primarykey=None,
        primaryname=None,
        primaryvalue=None,
        outervaluekey=None,
        metadatakeys=None,
        real_key=None,
        field_types: Dict[str, Callable] = None,
        meta_attributes=None,
        keypairs: dict = None,
    ):
        super().__init__(
            primarykey=primarykey,
            primaryname=primaryname,
            primaryvalue=primaryvalue,
            real_key=real_key,
        )

        assert isinstance(
            self._data[PRIMARYVALUE_KEY], dict
        ), "primaryvalue of a {} should be a dict but got {} instead. {}".format(
            self.__class__.__name__, type(primaryvalue), primaryvalue
        )

        self._childrenskeys = []
        self._children = {}
        self._augmentationclasses = get_augmentation_classes()
        self._outervalues = None
        self._metadatakeys = None
        self._skip_level_for_values = False
        self.meta_attribute_fields = []
        self.field_types = {}
        self._outervaluekey = None
        self._keypairs_of_related_values = {}

        self.set_field_types(field_types)
        self.set_keypairs_of_related_values(keypairs)

        if primaryvalue is None:
            primaryvalue = {}

        is_a_nested_item_but_outervaluekey_item_missing = not (
            outervaluekey is None
            or (outervaluekey is not None and outervaluekey in primaryvalue)
        )
        if is_a_nested_item_but_outervaluekey_item_missing:
            msg = (
                "A schema was applied to this mapping, but item '{0}' is missing."
                "This mapping might be broken.\n{1} <-- '{0}' is missing."
            )
            prettyprint = json.dumps(primaryvalue, indent="  ")
            raise ValueError(msg.format(outervaluekey, prettyprint))

        if outervaluekey is not None:
            self._skip_level_for_values = True

        if outervaluekey is None:
            self._outervalues = primaryvalue
        else:
            self._outervaluekey = outervaluekey
            self._outervalues = primaryvalue[outervaluekey]

        if metadatakeys is None:
            self._metadatakeys = []
        else:
            self._metadatakeys = metadatakeys

        #
        # The meta attributes explicitly are defined by the user
        if meta_attributes is not None:
            self.meta_attribute_fields = meta_attributes
        #
        # meta attributes are defined by a key within the mapping itself
        elif FIELDS_FOR_META_ATTRIBUTES in primaryvalue:
            self.meta_attribute_fields = primaryvalue[FIELDS_FOR_META_ATTRIBUTES]
        #
        # The default meta_attributes are metadata fields
        # If the user defined the metadata keys, then only these are taken.
        elif self._metadatakeys:
            default_meta_attributes_keys = []
            for key in self._metadatakeys:
                try:
                    item = primaryvalue[key]
                except KeyError:
                    continue
                if isinstance(item, (str, float, int)):
                    default_meta_attributes_keys.append(key)
            self.meta_attribute_fields = default_meta_attributes_keys
        #
        # If no metadata keys are defined explicitly than all single values of
        # type str, float, int are considered as meta attributes.
        else:
            meta_attributes_keys = []
            for key, item in primaryvalue.items():
                if isinstance(item, (str, float, int)):
                    meta_attributes_keys.append(key)
            self.meta_attribute_fields = meta_attributes_keys

        assert self._primarykeylink.is_linked(), "Linking primarykey to data failed."
        assert self._primarynamelink.is_linked(), "Linking primeryname to data failed."

        if field_types is not None:
            for key, destination_type in field_types.items():
                if key not in self._outervalues:
                    continue
                source_data_item = self._outervalues[key]
                self._outervalues[key] = destination_type(source_data_item)

    def set_keypairs_of_related_values(self, key_pairs):
        if key_pairs is None:
            self._keypairs_of_related_values = {}
        else:
            self._keypairs_of_related_values = key_pairs

    def set_field_types(self, field_types: Dict[str, Callable]):
        assert field_types is None or isinstance(
            field_types, dict
        ), "`field_types` need to be of type Dict[str, Callable]"
        if field_types is not None:
            self.field_types = field_types

    def get_child(self, primary_key: str) -> AnAugmentedTreeItem:
        treeitem = self._children[primary_key]
        return treeitem

    def get_pathmap(
        self, parent_path: TreePath = None, section_root_path: TreePath = None
    ):
        """
        Retrives a pathmap.

        Returns:
            List[Tuple[TreePath, ATreeItem]]
        """
        pathmap = []
        my_real_path = self.real_key
        my_augmented_path = self.primekey
        my_meta_attributes = self.get_meta_attributes()
        if parent_path is not None:
            my_treepath = parent_path.join(
                real_path=my_real_path,
                augmented_path=my_augmented_path,
                meta_attributes=my_meta_attributes,
            )
        else:
            my_treepath = TreePath(
                real_path=my_real_path,
                augmented_path=my_augmented_path,
                meta_attributes=my_meta_attributes,
            )

        if self.parent is not None:
            pathmap.append((my_treepath, self.parent))

        if self._skip_level_for_values:
            base_childs_path = TreePath(real_path=self._outervaluekey)
        else:
            base_childs_path = TreePath()

        base_childs_path = my_treepath.join(*base_childs_path)

        for childs_key, child in self._children.items():
            childs_paths = child.get_pathmap(parent_path=base_childs_path)
            pathmap.extend(childs_paths)
        return pathmap

    def __copy_wrapper__(self, copy_function_of_copy):
        if self.parent is None:
            underlying_real_data = self.primevalue
        else:
            # This part only works because a parent can only be a
            # collection, which defines __getitem__(), while
            # AnAugmentedTreeItem does not.
            underlying_real_data = self.parent[self.primekey]
        copied_real_data = copy_function_of_copy(underlying_real_data)
        copied_augmentation = augment_datastructure(
            copied_real_data, augmentclasses=self._augmentationclasses
        )
        return copied_augmentation

    def __copy__(self):
        return self.__copy_wrapper__(copy.copy)

    def copy(self, class_augmentation_schema=None):
        return self.__copy__()

    def __deepcopy__(self, memodict={}):
        return self.__copy_wrapper__(copy.deepcopy)

    def deepcopy(self):
        return self.__deepcopy__()

    @property
    def real_key(self) -> Union[int, str]:
        return self._real_key

    @property
    def primekey(self) -> Union[int, str]:
        return self._primarykeylink()

    @property
    def primename(self) -> Any:
        return self._primarynamelink()

    @property
    def primevalue(self) -> Any:
        return self._data[PRIMARYVALUE_KEY]

    @property
    def outervalues(self):
        return self._outervalues

    @property
    def leaf_type(self) -> LeafType:
        return LeafType.MAPPING

    def has_primekey(self, key):
        return key in self._children

    def data(self, column):
        if column == PRIMARYKEY_KEY:
            return self._primarykeylink()
        if column == PRIMARYNAME_KEY:
            return self._primarynamelink()
        if column == PRIMARYVALUE_KEY:
            return self.primevalue
        try:
            if column[0] == INNER_VALUE_MARKER_PREFIX:
                return self.primevalue[column[1:]]
            if not self._skip_level_for_values:
                return self._outervalues[column]
            return None
        except (KeyError, TypeError):
            return None

    def iter_children(self) -> Generator[AnAugmentedTreeItem, None, None]:
        for key in self._childrenskeys:
            yield self._children[key]

    def __contains__(self, item):
        return item in self._children

    # mapping implementation
    def __getitem__(self, key):
        if self._skip_level_for_values:
            if key[0] == INNER_VALUE_MARKER_PREFIX:
                return self.primevalue[key[1:]]
        return self._outervalues[key]

    # mapping implementation
    def __setitem__(self, key, value):
        # The current data container will be set with the new value.
        # In case the current container is a mapping, it has to be checked.
        # whether this key already existed of not.
        if key in self.field_types:
            target_type_converter = self.field_types[key]
            value = target_type_converter(value)
        _augment(self, key, value, self._augmentationclasses)
        self._outervalues[key] = value

    # mapping implementation
    def __delitem__(self, key):
        del self._outervalues[key]

    # mapping implementation
    def __iter__(self):
        return iter(self._outervalues)

    # mapping implementation
    def __len__(self):
        return len(self._outervalues)

    # mapping implementation
    def pop(self, key):
        return self._outervalues.pop(key)

    # mapping implementation
    def clear(self):
        self._outervalues.clear()
        self._children.clear()
        self._childrenskeys.clear()

    # mapping implementation
    def update(self, *key_pairs: Iterable[Tuple[Hashable, Any]], **kwargs):
        items_to_update = dict(*key_pairs, **kwargs)
        for key, item in items_to_update.items():
            self[key] = item

    # mapping implementation
    def setdefault(self, k, default):
        return self._outervalues.setdefault(k, default)

    # mapping implementation
    def keys(self):
        return self._outervalues.keys()

    def insert_child_at(self, key, child) -> bool:
        if key in self._metadatakeys:
            return False
        if key not in self._children:
            self._childrenskeys.append(key)
        self._children[key] = child
        child.parent = self
        return True

    def __bool__(self) -> bool:
        return len(self.outervalues) == 0

    def is_empty(self) -> bool:
        return len(self.outervalues) == 0

    def get_meta_attributes(self) -> List[Tuple[str, str]]:
        meta_attributes = []
        for meta_attribute_key in self.meta_attribute_fields:
            meta_attribute = self.primevalue[meta_attribute_key]
            meta_attributes.append((meta_attribute_key, meta_attribute))
        return meta_attributes

    def children_count(self) -> int:
        """
        Value items do not posses children.

        Returns:
            int:
                Returning 0, since value items do not posses children.
        """
        return len(self._children)

    def __getattr__(self, attribute_name):
        # Condition:
        # Real attributes come first. After this
        try:
            return super().__getattribute__(attribute_name)
        except AttributeError:
            if attribute_name in self._keypairs_of_related_values:
                requested_fieldkey = self._keypairs_of_related_values[attribute_name]
                return self.primevalue[requested_fieldkey]
            return self.primevalue[attribute_name]

    def __setattr__(self, attribute_name, value):
        # Because I (D. Scheliga) got brainf****d the first time.
        #
        # The task is to get a access of the dictionary values visible to the
        # outside as attributes. Assuming there is a dict with the key 'foo' then
        # this instance would have an attribute called 'foo'.
        #
        # If 'foo' should be changed via an attribute, the dictionary
        # `_outervalues` is needed.
        # Therefore super().__getattribute__("_outervalues") is mandatory to get
        # that container; else RecursionErrors or no access at all will happen.
        #
        # Only if the dictionary key preexists this attribute can be changed.
        # This condition is mandatory or else no attribute can be set at all.
        try:
            outer_values = super().__getattribute__("_outervalues")
            if outer_values is None:
                super().__setattr__(attribute_name, value)
                return
            if attribute_name in outer_values:
                setitem_func = super().__getattribute__("__setitem__")
                setitem_func(attribute_name, value)
            elif attribute_name in self._keypairs_of_related_values:
                target_fieldkey = self._keypairs_of_related_values[attribute_name]
                setitem_func = super().__getattribute__("__setitem__")
                setitem_func(target_fieldkey, value)
            else:
                super().__setattr__(attribute_name, value)
        except AttributeError:
            super().__setattr__(attribute_name, value)
