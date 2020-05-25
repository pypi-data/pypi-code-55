from abc import ABC, abstractmethod
from typing import (
    Union,
    Any,
    Optional,
    Sequence,
    Generator,
    List,
    Dict,
    Callable,
)

from augmentedtree.core import LeafType, TreePath


class AnAugmentedTreeItem(ABC):
    """
    It is mandatory to implement this abstract basic class for any kind
    of augmented tree item. This class defines the minimal, necessary
    set of properties and methods for a tree item within a two column
    tree view (like it is presented using `print_atree`).
    """

    @property
    @abstractmethod
    def primekey(self) -> Union[int, str]:
        """
        Represents the key this tree item is associated within its
        parent container. Also it is the first columns (left) value
        within a 2-column view (like when using `print_atree()`).

        Returns:
            Union[int, str]
        """
        pass

    @property
    @abstractmethod
    def primename(self) -> Any:
        """
        Represents the value this tree item is associated with. Also it
        is the second columns (right) value within a 2-column view
        (like when using `print_atree()`).

        Returns:
            Any
        """
        pass

    @property
    @abstractmethod
    def primevalue(self) -> Any:
        """
        The 'real' value/nested data this tree item is representing.

        Returns:
            Any
        """
        pass

    @property
    @abstractmethod
    def real_key(self) -> Union[int, str]:
        """
        The real index of the Sequence or real key of a Mapping of this
        item is in, within the augmented nested data.

        Returns:
            Union[int, str]
        """
        pass

    @property
    @abstractmethod
    def leaf_type(self) -> LeafType:
        """
        The type of `leaf` within the augmented tree in regard of the classification
        of 'value', 'sequence' and 'mapping'. See LeafType for more details.

        Returns:
            LeafType:
                This tree items type in regard of value, sequence or mapping, ... .
        """
        pass

    @property
    @abstractmethod
    def parent(self) -> Optional["AnAugmentedCollection"]:
        """
        Gets and sets this tree item's parent. A 'Value' tree item
        cannot be a parent.

        Returns:
            AnAugmentedCollection:
                Parent tree item of this tree item.
        """
        pass

    @parent.setter
    @abstractmethod
    def parent(self, parent: Optional["AnAugmentedCollection"]):
        pass

    @property
    @abstractmethod
    def children(self) -> Sequence:
        """
        Access to the children (tree items) this tree item possess.
        Also obligatory for a brasic QT implementation.

        Returns:
            Sequence
                Sequence of `AnAugmentedTreeItem`
        """
        pass

    # basic implementation for QT
    @abstractmethod
    def insert_child_at(
        self, position: Union[int, str], child: "AnAugmentedTreeItem"
    ) -> bool:
        """
        Inserts *AnAugmentedTreeItem* as a `child` into this item at the
        `position`.

        Args:
            position:
            child:

        Returns:
            bool:
                `True` if `child` could by successfully inserted at
                `position`; False if insertion of `child` failed.
        """
        pass

    @abstractmethod
    def has_primekey(self, key: Union[int, str]):
        """
        Returns it the tree item has a child with the requested key.
        Basic implementation for QT, where it's called hasKey().

        Args:
            key (Union[int, str]):
                Requested key.

        Returns:
            bool
        """
        pass

    # basic implementation for QT
    @abstractmethod
    def data(self, column: str) -> Any:
        """
        Returns the tree items data for the requested column. Basic
        implementation for QT.

        Args:
            column (str):
                The column within a view.

        Returns:
            Any:
                Value associated with the requested column.
        """
        pass

    @abstractmethod
    def get_child(self, primary_key):
        """
        Returns `AnAugmentedTreeItem` for the requested `primary_key`.
        Basic implementation for QT.

        Args:
            primary_key (str):
                Key for which `AnAugmentedTreeItem` should be returned.

        Raises:
            KeyError:
                If no item for the given `primary_key` exist.

        Returns:
            AnAugmentedTreeItem
        """
        pass

    # basic implementation for QT
    @abstractmethod
    def children_count(self) -> int:
        """
        Returning the childrens' count. Basic implementation for QT.

        Returns:
            int: Count of children.
        """
        pass

    def iter_children(self,) -> Generator["AnAugmentedTreeItem", None, None]:
        """
        Since __iter__ of SequenceTreeItems and MappingTreeItems or
        other containers works differently this method assures, that
        the targeted behavior of AnAugmentedTreeItem.children can be
        applied.

        Returns:
            Generator[AnAugmentedTreeItem, None, None]
        """
        pass

    def get_pathmap(
        self,
        parent_path: Optional["TreePath"] = None,
        section_root_path: Optional["TreePath"] = None,
    ):
        """
        Creates a map of `tree paths` of all sub children from base of
        this tree item. If `parent_path` is supplied this items path and
        its children paths should join onto the parent items path.
        In a rare occasion a `section_root_path` might overrule
        `parent_path`.

        Args:
            parent_path (object):
                The path of this items parent.

            section_root_path (TreePath, optional):
                The path of a tree item, which is considered as path
                root, but not being necessarily the root.

        Returns:
            List[Tuple[TreePath, ATreeItem]]:
                A list with the `TreePath` and it's tree item within
                a tuple, from this item and its sub children.
        """
        pass


class AnAugmentedCollection(AnAugmentedTreeItem):
    """
    In addition to AnAugmentedTreeItem a tree item resembling a
    sequence or mapping has to implement `__getitem__`, `__setitem__`
    and `outervalues`.
    """
    @abstractmethod
    def __getitem__(self, key_or_index):
        pass

    @abstractmethod
    def __setitem__(self, key, value):
        pass

    @property
    @abstractmethod
    def outervalues(self):
        """
        Returns this tree items origin nested data, which is considered
        to represent this tree items values. These doesn't need to
        be identical to `primevalue`, but `primevalue` always contains
        the values visible to the outside.

        Returns:
            Any
        """
        pass


class TypeDefinable(ABC):
    @property
    @abstractmethod
    def field_types(self) -> Dict[str, Callable]:
        """
        Defines specific data types for a set of fields.

        Returns:
            Dict[Callable]:
                Keys refers to the field, which types will be enforced
                by the given `Callable`. Converting the data into the
                targeted type is done by `Callable(data)`
        """
        pass

    @field_types.setter
    @abstractmethod
    def field_types(self, typed_field_definition: Dict[str, Callable]):
        pass
