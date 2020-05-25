from typing import (
    Union,
    Mapping,
    Sequence,
    Dict,
    Any,
    Generator,
    List,
    Optional,
    Tuple,
    Callable,
)
from augmentedtree.core import TreePath, NotSupportedError
from augmentedtree.abstractbaseclasses import (
    AnAugmentedCollection,
    AnAugmentedTreeItem,
)
from augmentedtree.augmentation import augment_datastructure, print_atree
from augmentedtree.treeitemselection import (
    UnixFilePatternParts,
    RegularExpressionParts,
    PathMap,
    PathMapItem,
)


class Selectable(object):
    """
    This class enables and `AnAugmentedTreeItem` to be able to select
    items by parts of a path within the nested data.
    """

    def __call__(self, *path_parts: List[Union[str, int]]) -> List[AnAugmentedTreeItem]:
        """
        Makes a selection of tree items in regard of the given path
        parts. The path parts do not need to resemble the whole path.


        Args:
            path_parts: List[Union[str, int]]:
                Path parts for which tree items should be retrived.

        Returns:
            List[AnAugmentedTreeItem]:
                Tree items which fit to the given tree parts.
        """
        pass


class WhereRefineable(object):
    """
    This class enables and `AnAugmentedTreeItem` to be able to refine
    a selection with `where`.
    """

    def __call__(
        self, conditions: Dict[str, Any], **kwargs
    ) -> List[AnAugmentedTreeItem]:
        """
        Narrows a selection to tree items, which fits the given
        conditions.

        Args:
            conditions (Dict["str": Any]):


            **kwargs:

        Returns:

        """
        pass


class AugmentedTree(AnAugmentedTreeItem):
    """
    This class is the recommended entry for augmenting nested data.

    Args:
        data(Union[Mapping, Sequence]):
            Augments this given data.

        use_schemas(bool):
            As default registered schemas are used. If turned to
            `false` this tree will represent the pure data
            structure.
    """

    def __init__(
        self,
        data: Union[AnAugmentedCollection, Mapping, Sequence],
        use_schemas: bool = True,
        pathmap: PathMap = None,
    ):
        """
        Augments the given `data`.

        Args:
            data(Union[Mapping, Sequence]):
                Augments this given data.

            use_schemas(bool):
                As default registered schemas are used. If turned to
                `false` this tree will represent the pure data
                structure.

            pathmap(PathMap, optional):
                If given this map resembles the selected items of this
                tree.
        """
        if isinstance(data, AnAugmentedCollection):
            augmented_treeitem = data
        else:
            augmented_treeitem = augment_datastructure(data, use_schemas=use_schemas)

        self._is_in_selectionmode = False
        self._augmentedtree: AnAugmentedCollection = augmented_treeitem
        self._pathmap: PathMap = pathmap
        self.using_schemas: bool = use_schemas
        self.missing_paths_of_queries = []
        self._selections = []
        if pathmap is None:
            self.map()

    @property
    def parent(self) -> Optional["AnAugmentedCollection"]:
        return None

    @parent.setter
    def parent(self, parent):
        raise NotSupportedError(
            "An AugmentedTree cannot have a parent. Its the root."
            "This property setter should not have been called."
        )

    @property
    def pathmap(self):
        return self._pathmap

    @property
    def treeitems(self):
        return self.pathmap.treeitems

    def collect_missing_query_results(self):
        result = self.missing_paths_of_queries.copy()
        for selection in self._selections:
            subresults = selection.collect_missing_query_results()
            result.extend(subresults)
        return result

    def register_failed_query(self, search_pattern: str):
        self.missing_paths_of_queries.append(search_pattern)

    def __enter__(self):
        self._is_in_selectionmode = True
        self._selections.clear()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._is_in_selectionmode = False
        for selection in self._selections:
            subresults = selection.collect_missing_query_results()
            self.missing_paths_of_queries.extend(subresults)

    def start_selecting(self):
        return self

    @property
    def all_selections_succeeded(self) -> bool:
        return len(self.missing_paths_of_queries) == 0

    def data(self, column: [int, str]) -> Any:
        try:
            return self._augmentedtree.data(column)
        except AttributeError:
            raise ValueError("AugmentedTree doesn't have proper data.")

    @property
    def primekey(self):
        try:
            return self._augmentedtree.primekey
        except AttributeError:
            raise ValueError("AugmentedTree doesn't have proper data.")

    @property
    def primename(self):
        try:
            return self._augmentedtree.primename
        except AttributeError:
            raise ValueError("AugmentedTree doesn't have proper data.")

    @property
    def primevalue(self):
        try:
            return self._augmentedtree.primevalue
        except AttributeError:
            raise ValueError("AugmentedTree doesn't have proper data.")

    @property
    def real_key(self):
        try:
            return self._augmentedtree.real_key
        except AttributeError:
            raise ValueError("AugmentedTree doesn't have proper data.")

    def iter_children(self,) -> Generator[AnAugmentedTreeItem, None, None]:
        try:
            for child in self._augmentedtree.iter_children():
                yield child
        except AttributeError:
            raise ValueError("AugmentedTree doesn't have proper data.")

    @property
    def children(self) -> Sequence:
        try:
            return self._augmentedtree.children
        except AttributeError:
            raise ValueError("AugmentedTree doesn't have proper data.")

    def insert_child_at(self, position, child):
        try:
            return self._augmentedtree.insert_child_at(position, child)
        except AttributeError:
            raise ValueError("AugmentedTree doesn't have proper data.")

    def has_primekey(self, key):
        try:
            return self._augmentedtree.has_primekey(key)
        except AttributeError:
            raise ValueError("AugmentedTree doesn't have proper data.")

    def get_child(self, primary_key):
        try:
            return self._augmentedtree.get_child(primary_key)
        except AttributeError:
            raise ValueError("AugmentedTree doesn't have proper data.")

    def children_count(self) -> int:
        try:
            return self._augmentedtree.children_count()
        except AttributeError:
            raise ValueError("AugmentedTree doesn't have proper data.")

    def get_pathmap(
        self,
        parent_path: Optional["TreePath"] = None,
        section_root_path: Optional["TreePath"] = None,
    ):
        try:
            return self._augmentedtree.get_pathmap(parent_path, section_root_path)
        except AttributeError:
            raise ValueError("AugmentedTree doesn't have proper data.")

    @property
    def leaf_type(self):
        try:
            return self._augmentedtree.leaf_type
        except AttributeError:
            raise ValueError("AugmentedTree doesn't have proper data.")

    def __bool__(self):
        return self._pathmap.is_empty()

    def __iter__(self) -> Generator[Any, None, None]:
        for item in self._augmentedtree:
            yield item

    def __getitem__(self, position_or_key: Union[int, str]) -> Any:
        """
        Returns the item or value for the x-th integer position within a
        sequence or the key within a mapping.

        Args:
            position_or_key(Union[int, str]:
                x-th integer position within a sequence or the key
                within a mapping.

        Returns:
            Any:
                The *primevalue* ergo item or value of the requested
                item.
        """
        return self._augmentedtree[position_or_key]

    def __setitem__(self, index_or_key: Union[int, str], value: Any):
        self._augmentedtree[index_or_key] = value

    def iter_selection(self) -> Generator[Tuple[str, Any], None, None]:
        """
        Iterates through the done selection and retrieving the *primekey* of
        the element and its *primevalue*.

        Returns:
            Tuple[str, Any]:
                Tree items *primekey* and *primevalue*, which are the *key*
                and *value* of a dictionary and the *integer index* and
                *value* of a sequence.
        """
        for treeitem in self._pathmap.treeitems:
            print(treeitem.primekey)
            yield treeitem.primekey, treeitem.primevalue

    def select(
        self,
        *search_parts: List[
            Union[str, List[str], UnixFilePatternParts, RegularExpressionParts]
        ]
    ) -> "AugmentedItemSelection":
        """
        Selects tree items on base of the supplied *search_parts*, which are
        parts of the *augmented_paths* within the tree. All parts are
        considered with an *and* condition in between them. Multiple parts
        within a part are considered with an *or* condition in between.

        Examples:
            select("this", "and_that", ["this", "or_this", "or_that"])

        Args:
            *search_parts:
                Tree path parts which are parts of the requested tree items
                paths.

        Returns:
            AugmentedItemSelection:
                Selection of augmented tree items.
        """
        selected_pathmap = self._pathmap.select(*search_parts)

        if selected_pathmap:
            self.register_failed_query(selected_pathmap.search_pattern)

        selection = AugmentedItemSelection(
            data=self._augmentedtree, pathmap=selected_pathmap,
        )
        self._selections.append(selection)

        return selection

    def where(self, *search_parts) -> "AugmentedItemSelection":
        """
        Selects tree items on base of the supplied *search_parts*, which are
        parts of the tree items *meta_attributes*. All parts are
        considered with an *and* condition in between them. Multiple parts
        within a part are considered with an *or* condition in between.

        Examples:
            select("this", "and_that", ["this", "or_this", "or_that"])

        Args:
            *search_parts:
                Tree path parts which are parts of the requested tree items
                paths.

        Returns:
            AugmentedItemSelection:
                Selection of augmented tree items.
        """
        selected_pathmap = self._pathmap.where(*search_parts)

        if selected_pathmap:
            self.register_failed_query(selected_pathmap.search_pattern)

        selection = AugmentedItemSelection(
            data=self._augmentedtree, pathmap=selected_pathmap,
        )
        self._selections.append(selection)

        return selection

    def map(self):
        self._pathmap = PathMap()
        self._pathmap.from_treeitem(self._augmentedtree)

    def sort(
        self, sorting_method: Optional[Callable[[PathMapItem], int]] = None
    ) -> AnAugmentedTreeItem:
        """
        Sorts the items within this selection by their augmented path by
        default or by a custom method, which returns an ascending integer
        number for each PathMapItem within this tree.

        Args:
            sorting_method(Callable[[PathMapItem], int], optional):
                Custom method to tag PathMapItems of this selection with a
                ascending integer number.
        """
        self._pathmap.sort(sorting_method)
        return self

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self._augmentedtree.primevalue)

    def print(self, additional_columns: List = None, show_hidden: bool = False):
        print_atree(
            treeitem=self._augmentedtree,
            additional_columns=additional_columns,
            show_hidden=show_hidden,
        )


class AugmentedItemSelection(AugmentedTree):
    def __init__(
        self,
        data: Union[AnAugmentedCollection, Mapping, Sequence],
        use_schemas: bool = True,
        pathmap: Optional[PathMap] = None,
    ):
        """
        Augments the given `data`.

        Args:
            data(Union[Mapping, Sequence]):
                Augments this given data.

            use_schemas(bool):
                As default registered schemas are used. If turned to
                `false` this tree will represent the pure data
                structure.

            pathmap(PathMap, optional):
                If given this map resembles the selected items of this
                tree.
        """
        super().__init__(
            data=data, use_schemas=use_schemas, pathmap=pathmap,
        )

    def is_empty(self):
        return self.pathmap.is_empty()

    def __getitem__(self, index) -> Any:
        if isinstance(index, slice):
            return self._get_items_by_slice(index)
        selected_treeitem = self._pathmap.treeitems.by_position(index)
        if selected_treeitem is None:
            return None
        return selected_treeitem.primevalue

    def _get_items_by_slice(self, slicing_index):
        requested_values = []
        for real_path in self._pathmap.real_paths[slicing_index]:
            selected_treeitem = self._pathmap.treeitems.by_real_path(real_path)
            if selected_treeitem is None:
                continue
            requested_values.append(selected_treeitem.primevalue)
        return requested_values

    def __setitem__(self, position: Union[int, slice], value: Any):
        """
        Set the value (*primevalue*) of a tree item at the x-th integer
        position within the path map. If a slice is supported values of all
        items within the slice are set.

        Args:
            position(Union[int, slice]):
                x-th integer position or slice within path map.

            value(Any):
                The new value of the selected treeitem(s)
        """
        if isinstance(position, slice):
            self._pathmap.treeitems.set_value_of_treeitems(position, value)
        else:
            self._pathmap.treeitems.set_value_of_treeitem(position, value)

    def __str__(self):
        return "{}({})".format(self.__class__.__name__, self._pathmap.search_pattern)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self._pathmap.search_pattern)

    def print(self, **kwargs):
        index_for_getitem = 0
        for pathmapitem in self._pathmap.pathmapitems:
            print("#{} {}".format(index_for_getitem, pathmapitem.treeitem.primevalue))
            index_for_getitem += 1
