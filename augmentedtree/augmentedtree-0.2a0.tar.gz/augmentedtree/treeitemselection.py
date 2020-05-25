import re
import warnings
from abc import ABC, abstractmethod
from itertools import zip_longest
from typing import (
    Union,
    List,
    Optional,
    Dict,
    Any,
    Tuple,
    Iterable,
    Iterator,
    Generator,
    Match,
    Callable,
)

from pandas import DataFrame, Series

from augmentedtree import AnAugmentedTreeItem, print_atree
from augmentedtree.core import AUGMENTATION_ROOT_KEY, TreePath

UFP2RE_WILDCARD_STAR = "*.?"
IGNORE_TREE_PATH_PARTS_IN_BETWEEN = "(.*/{})"
LAST_VALID_TREE_PATH_LEVEL = "(.*/{}$)"
END_POINT_SEARCH_PART_MUST_NOT_CONTINUE_AFTER_A_DELIMITER = "(?!.*/).*"
META_ATTRIBUTE_PAIR_REGEX_WRAPPER = ".*/{}/.*"


class QuestionmarkUnixFilePattern2RegexReplacer(object):
    this_char_is = "?"
    detector = re.compile("[?]+")

    def __new__(cls, expression_to_convert: str) -> str:
        if cls.this_char_is not in expression_to_convert:
            return expression_to_convert
        converted_expression = cls.detector.sub(
            cls.make_replacement, expression_to_convert
        )
        return converted_expression

    @staticmethod
    def make_replacement(questionmark_matchobject: Match):
        length = questionmark_matchobject.end(0) - questionmark_matchobject.start(0)
        if length == 1:
            return "."
        else:
            replacement = ".{{{}}}".format(length)
            return replacement


class StaticUnixFilePattern2RegexReplacer(object):
    def __init__(
        self,
        regex_detection_pattern: str,
        replacement: str,
        str_to_detect_in_expression: str = None,
    ):
        self.detector = re.compile(regex_detection_pattern)
        self.replacement = replacement
        self.this_char_is = str_to_detect_in_expression

    def __call__(self, expression_to_convert: str):
        nothing_to_replace = (
            self.this_char_is is not None
            and self.this_char_is not in expression_to_convert
        )
        if nothing_to_replace:
            return expression_to_convert
        converted_expression = self.detector.sub(
            self.replacement, expression_to_convert
        )
        return converted_expression


StarWildCard_Replacer = StaticUnixFilePattern2RegexReplacer(
    regex_detection_pattern=r"\*", replacement="*.?", str_to_detect_in_expression="*"
)

# ForewardSlash_Replacer = StaticUnixFilePattern2RegexReplacer(
#     regex_detection_pattern="\/", replacement="\/", str_to_detect_in_expression="/"
# )

UNIXFILEPATTERN_TO_REGEX_REPLACEMENTS = [
    QuestionmarkUnixFilePattern2RegexReplacer,
    StarWildCard_Replacer,
    # ForewardSlash_Replacer,
]


def convert_unixfilepattern_to_regex(expression_to_convert: str) -> str:
    converted_expression = expression_to_convert
    for converter in UNIXFILEPATTERN_TO_REGEX_REPLACEMENTS:
        converted_expression = converter(converted_expression)
    return converted_expression


class TreePathSearchPatternParts(ABC):
    """
    Defines a set of tree path parts, which are combined to an `or` condition
    within this group within a query.
    """

    def to_re_pattern(self) -> str:
        """
        Converts all parts of this entity to regular expressions.

        Returns:
            str:
                Regular expressions of all parts.
        """
        pass


class UnixFilePatternParts(TreePathSearchPatternParts):
    def __init__(self, *path_parts):
        self.path_parts = path_parts

    def to_re_pattern(self) -> str:
        """
        Converts these UnixFilePatternParts into a regular expression, which
        will work as an or condition, if multiple parts are defined.

        Returns:
            str:
                regular expression
        """
        re_path_parts = UnixFilePatternParts.convert_to_re_patterns(*self.path_parts)
        or_conditioned = "|".join(re_path_parts)
        or_conditioned = "(" + or_conditioned + ")"
        return or_conditioned

    @staticmethod
    def convert_to_re_patterns(*unix_file_pattern) -> List[str]:
        """
        Converts strings being considered as a unix file patterns to regular
        expression patterns.

        Args:
            *unix_file_pattern:
                Search pattern(s) to be converted into regular expressions.

        Returns:
            List(str):
                Regular expression patterns.
        """
        regex_patterns = []
        for unit_file_pattern in unix_file_pattern:
            regex_pattern = convert_unixfilepattern_to_regex(unit_file_pattern)
            regex_patterns.append(regex_pattern)
        return regex_patterns

    def __str__(self):
        joined_parts = " -> ".join(self.path_parts)
        return "({})".format(joined_parts)


UNIXFILEPATTERNPART_DEPRECATION_MESSAGE = (
    "The singular named 'UnixFilePatternPart' will be deprecated in the future release "
    "0.2a0. Use the plural form 'UnixFilePatternParts' instead."
)


class UnixFilePatternPart(object):
    def __new__(cls, *path_parts):
        warnings.warn(UNIXFILEPATTERNPART_DEPRECATION_MESSAGE, FutureWarning)
        return UnixFilePatternParts(*path_parts)

    @staticmethod
    def convert_to_re_patterns(*unix_file_pattern):
        warnings.warn(UNIXFILEPATTERNPART_DEPRECATION_MESSAGE, FutureWarning)
        return UnixFilePatternParts.convert_to_re_patterns(*unix_file_pattern)


class RegularExpressionParts(TreePathSearchPatternParts):
    def __init__(self, *path_parts):
        self.path_parts = path_parts

    def to_re_pattern(self) -> str:
        """
        Combines these RegularExpressionParts into a single regular
        expression, which will work as an or condition,
        if multiple parts are defined.

        Returns:
            str:
                regular expression
        """
        or_conditioned = "|".join(self.path_parts)
        or_conditioned = "(" + or_conditioned + ")"
        return or_conditioned

    def __str__(self):
        joined_parts = " -> ".join(self.path_parts)
        return "({})".format(joined_parts)


REGULAREXRESSIONPART_DEPRECATION_MESSAGE = (
    "The singular named 'RegularExpressionPart' will be deprecated in future release "
    "0.2a0. Use the plural form 'RegularExpressionParts' instead."
)


class RegularExpressionPart(object):
    def __new__(cls, *path_parts):
        warnings.warn(REGULAREXRESSIONPART_DEPRECATION_MESSAGE, FutureWarning)
        return RegularExpressionParts(*path_parts)


def _convert_search_part_to_regex_pattern(
    search_part: Union[str, UnixFilePatternParts, RegularExpressionParts]
) -> str:
    """
    Converts a single search part to a regular expression search part. Strings
    will be considered as a unix file pattern. Regular expression parts need
    to be explicitly defined as 'RegularExpressionParts'.

    Args:
        search_part(Union[str, UnixFilePatternParts, RegularExpressionParts]):
            Tree path search part, which will be converted to a regular
            expression.

    Returns:
        str:
            regular expression
    """
    if isinstance(search_part, str):
        regex_pattern = convert_unixfilepattern_to_regex(search_part)
    else:
        regex_pattern = search_part.to_re_pattern()
    return regex_pattern


def _convert_all_search_parts_to_regex_patterns(
    *search_parts: Union[str, UnixFilePatternParts, RegularExpressionParts]
) -> List[str]:
    """
    Converts multiple search parts to regular expression search parts. Strings
    will be considered as a unix file pattern. Regular expression parts need
    to be explicitly defined as 'RegularExpressionParts'.

    Args:
        *search_part:
            Search parts of *str*, *UnixFilePatternParts* or
            *RegularExpressionParts*, which will be converted to a regular
            expressions.

    Returns:
        List[str]:
            regular expressions
    """
    regular_expression_search_parts = []

    for search_part in search_parts:
        search_part_pattern = _convert_search_part_to_regex_pattern(search_part)
        regular_expression_search_parts.append(search_part_pattern)

    return regular_expression_search_parts


def _make_search_parts_to_ignore_unknown_ones(
    regex_search_parts: List[str],
) -> List[str]:
    """
    Puts regular expression parts into a group

    Args:
        regex_search_parts(str):
            Regular expression search parts, which need to be enabled to
            ignore unknown tree path parts in between them.

    Returns:
        List[str]:
            Regular expression search parts (with ignorance), which will
            ignore unknown tree path parts in between them.
    """
    template = IGNORE_TREE_PATH_PARTS_IN_BETWEEN
    regex_search_parts_with_ignorance = []
    for regular_expression_search_part in regex_search_parts:
        pattern_with_ignorance = template.format(regular_expression_search_part)
        regex_search_parts_with_ignorance.append(pattern_with_ignorance)
    return regex_search_parts_with_ignorance


def _consider_star_wildcard(end_point_regex_search_part: str) -> str:
    """
    Takes account of a star wildcard within a search part, which should
    behave as the end point of the selection.

    Args:
        end_point_regex_search_part:
            Regular expression search part being an end point of search.

    Returns:
        str:
            Regular expression search part, which cannot continue with a
            tree path delimiter.
    """
    star_wildcard_endpoint = end_point_regex_search_part.replace(
        UFP2RE_WILDCARD_STAR, END_POINT_SEARCH_PART_MUST_NOT_CONTINUE_AFTER_A_DELIMITER
    )
    return star_wildcard_endpoint


def create_selection_pattern(*search_parts):
    """
    Creates a search pattern, which will select tree paths up to the last
    defined `search part`.

    Args:
        *search_parts:
            Search parts being str,

    Returns:

    """
    regex_search_parts = _convert_all_search_parts_to_regex_patterns(*search_parts)
    final_search_parts = _make_search_parts_to_ignore_unknown_ones(regex_search_parts)

    last_regex_search_part = regex_search_parts[-1]
    end_point_search_part = LAST_VALID_TREE_PATH_LEVEL.format(last_regex_search_part)
    end_point_search_part = _consider_star_wildcard(end_point_search_part)
    final_search_parts[-1] = end_point_search_part

    # build search pattern
    search_pattern = "".join(final_search_parts)

    return search_pattern


def convert_to_where_searchable_parts(
    *search_parts: List[Union[str, UnixFilePatternParts, RegularExpressionParts]]
) -> List[str]:
    """
    Creates a search pattern, which will select tree paths up to the last
    defined `search part`.

    Args:
        *search_parts:
            Search parts being str,

    Returns:
        List[str]:
            Search pattern for looking at meta_attributes.
    """
    regex_search_parts = _convert_all_search_parts_to_regex_patterns(*search_parts)
    where_searchable_parts = []
    for search_part in regex_search_parts:
        where_searchable = META_ATTRIBUTE_PAIR_REGEX_WRAPPER.format(search_part)
        where_searchable_parts.append(where_searchable)
    return where_searchable_parts


class SelectionRegexPathQuery(object):
    def __init__(
        self,
        *path_parts: List[Union[str, UnixFilePatternParts, RegularExpressionParts]]
    ):
        self.path_parts = path_parts
        self.search_pattern = create_selection_pattern(*path_parts)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.search_pattern)


class PathMapItem(object):
    def __init__(
        self,
        real_path: str,
        augmented_path: str,
        primekey: str,
        real_key: str,
        meta_attributes: str,
        treeitem: AnAugmentedTreeItem = None,
    ):
        self.treeitem = treeitem
        self.real_path = real_path
        self.augmented_path = augmented_path
        self.primekey = primekey
        self.real_key = real_key
        self.meta_attributes = meta_attributes

    def __repr__(self):
        return "{}({}: {})".format(
            self.__class__.__name__, self.real_path, self.treeitem
        )

    def __str__(self):
        return self.__repr__()


class _IHaveToFuckingProperNameThis(ABC):
    def __getitem__(
        self, key: Union[int, str, slice]
    ) -> Union[AnAugmentedTreeItem, Iterable[AnAugmentedTreeItem]]:
        """
        Retrieves an item at the given *real_path* or the x-th integer
        *position* within its PathMap. If a *slice* is given all corresponding
        item are returned.

        Args:
            key(Union[int, str, slice]):
                Either a *real_path*, an integer *position* or a slice.

        Returns:
            Union[PathMapItem, Iterable[PathMapItem]]:
                An item for a *real_path* or integer *position* or a list
                of items for a *slice*.
        """
        if isinstance(key, int):
            return self.by_position(key)
        if isinstance(key, str):
            return self.by_real_path(key)
        if isinstance(key, slice):
            return self.by_slice(key)
        raise IndexError(
            "Neither a real_path, a integer position or a slice were given."
        )

    @abstractmethod
    def by_real_path(self, real_path: str) -> Any:
        """
        Retrieves an item at the given *real_path*.

        Args:
            real_path(str):
                Real path of the tree item, for which a PathMapItem is
                returned.

        Returns:
            Any
        """
        pass

    @abstractmethod
    def by_position(self, position: int) -> Any:
        """
        Retrieves an item for the integer *position* within this
        path map.

        Args:
            position(int):
                Integer position within the path map.

        Returns:
            Any
        """
        pass

    @abstractmethod
    def by_slice(self, positions: slice) -> List[Any]:
        """
        Retrieves a set of items at the positions, which are defined
        by a slice.

        Args:
            positions(slice):
                Slice for which items should be returned.

        Returns:
            List[Any]
        """
        pass


class _PathMapItems(_IHaveToFuckingProperNameThis):
    def __init__(self, parent_pathmap: "PathMap"):
        self._parent = parent_pathmap

    def __iter__(self) -> Generator[PathMapItem, None, None]:
        for index, pathmap_row in self._parent.iterrows():
            metadata_of_treeitem = pathmap_row.to_dict()
            treeitem = self._parent.treeitems.by_real_path(pathmap_row.real_path)
            pathmap_item = PathMapItem(treeitem=treeitem, **metadata_of_treeitem)
            yield pathmap_item

    def __getitem__(
        self, key: Union[int, str, slice]
    ) -> Union[AnAugmentedTreeItem, Iterable[AnAugmentedTreeItem]]:
        """
        Retrieves a PathMapItem at the given *real_path* or the x-th integer
        *position* within its PathMap. If a *slice* is given all corresponding
        PathMapItem are returned.

        Args:
            key(Union[int, str, slice]):
                Either a *real_path*, an integer *position* or a slice.

        Returns:
            Union[PathMapItem, Iterable[PathMapItem]]:
                A PathMapItem for a *real_path* or integer *position* or a list
                of tree items for a *slice*.
        """
        return super().__getitem__(key)

    def by_real_path(self, real_path: str) -> PathMapItem:
        """
        Retrieves a *PathMapItem* at the given *real_path*.

        Args:
            real_path(str):
                Real path of the tree item, for which a PathMapItem is
                returned.

        Returns:
            PathMapItem
        """
        pathmap_row = self._parent.get_treeitem_metadata(real_path)
        metadata_of_treeitem = pathmap_row.to_dict()
        treeitem = self._parent.treeitems.by_real_path(pathmap_row.real_path)
        pathmap_item = PathMapItem(treeitem=treeitem, **metadata_of_treeitem)
        return pathmap_item

    def by_position(self, position: int) -> PathMapItem:
        """
        Retrieves a *PathMapItem* for the integer *position* within this
        path map.

        Args:
            position(int):
                Integer position within the path map.

        Returns:
            PathMapItem
        """
        real_path = self._parent.real_paths[position]
        return self.by_real_path(real_path)

    def by_slice(self, positions: slice) -> List[PathMapItem]:
        """
        Retrieves a set of *PathMapItem* at the positions, which are defined
        by a slice.

        Args:
            positions(slice):
                Slice for which *PathMapItems* should be returned.

        Returns:
            List[PathMapItems]
        """
        requested_pathmapitems = []
        requested_real_paths = self._parent.real_paths[positions]
        for real_path in requested_real_paths:
            pathmapitem = self.by_real_path(real_path)
            requested_pathmapitems.append(pathmapitem)
        return requested_pathmapitems


class _TreeItems(_IHaveToFuckingProperNameThis):
    def __init__(self, parent_pathmap: "PathMap"):
        self._parent = parent_pathmap

    def __iter__(self):
        for real_path in self._parent.real_paths:
            treeitem = self.by_real_path(real_path)
            yield treeitem

    def __getitem__(
        self, key: Union[int, str, slice]
    ) -> Union[AnAugmentedTreeItem, Iterable[AnAugmentedTreeItem]]:
        """
        Retrieves a tree item at the given *real_path* or the x-th integer
        *position* within its PathMap. If a *slice* is given all corresponding
        tree items are returned.

        Args:
            key(Union[int, str, slice]):
                Either a *real_path*, an integer *position* or a slice.

        Returns:
            Union[AnAugmentedTreeItem, Iterable[AnAugmentedTreeItem]]:
                A tree item for a *real_path* or integer *position* or a list
                of tree items for a *slice*.
        """
        if isinstance(key, int):
            return self.by_position(key)
        if isinstance(key, str):
            return self.by_real_path(key)
        if isinstance(key, slice):
            return self.by_slice(key)
        raise IndexError(
            "Neither a real_path, a integer position or a slice were given."
        )

    def by_real_path(self, real_path: str) -> AnAugmentedTreeItem:
        """
        Retrives a tree item by its *real_path*.

        Args:
            real_path(str):
                The requested tree item's real path.

        Returns:
            AnAugmentedTreeItem:
                Tree item at the provided *real_path*.
        """
        item_row = self._parent.get_treeitem_metadata(real_path)
        parent_of_treeitem = self._parent.get_parent_of_treeitem_by_real_path(real_path)
        treeitem = parent_of_treeitem.get_child(item_row.primekey)
        return treeitem

    def by_position(self, position: int) -> Optional[AnAugmentedTreeItem]:
        """
        Retrives the treeitem by an integer index, based on the tree items
        row within the TreeMap.

        Args:
            position(int):
                Row's index within the PathMap

        Returns:
            AnAugmentedTreeItem:
                Tree item at the position.
        """
        assert isinstance(position, int), "position has to be an integer"
        assert position >= 0, "position needs to be a positive integer or zero."
        if self._parent.is_empty():
            return None
        real_path = self._parent.real_paths[position]
        item_row = self._parent.get_treeitem_metadata(real_path)
        parent_of_treeitem = self._parent.get_parent_of_treeitem_by_real_path(
            item_row.real_path
        )
        treeitem = parent_of_treeitem.get_child(item_row.primekey)
        return treeitem

    def by_slice(self, positions: slice) -> Iterable[AnAugmentedTreeItem]:
        """
        Retrives the treeitem by an integer index, based on the tree items
        row within the TreeMap.

        Args:
            positions(slice):
                Row's index within the PathMap

        Returns:
            AnAugmentedTreeItem:
                Tree item at the position.
        """
        if self._parent.is_empty():
            return []
        subtable = self._parent.get_slice_of_treeitem_metadata(positions)
        requested_treeitems = []
        get_the_treeitems_parent_by = self._parent.get_parent_of_treeitem_by_real_path
        for real_path, item_row in subtable.iterrows():
            # Within in this class the index of subtable is a str
            # noinspection PyTypeChecker
            parent_of_treeitem = get_the_treeitems_parent_by(real_path)
            treeitem = parent_of_treeitem.get_child(item_row.primekey)
            requested_treeitems.append(treeitem)
        return requested_treeitems

    def print(self):
        for index, pathmapitem in enumerate(self._parent.pathmapitems):
            print("#{} {}".format(index, pathmapitem.augmented_path))
            print_atree(pathmapitem.treeitem, indent="  ", prefix="  ")

    def get_value(self, position: int) -> Any:
        """
        Gets the primevalue of the tree item at the x-th integer *position*
        within the PathMap.

        Args:
            position(int):
                x-th position within the PathMap.

        Returns:
            Any:
                *primevalue* of the tree item
        """
        real_path_of_treeitem = self._parent.real_paths[position]
        selected_treeitem = self.by_real_path(real_path_of_treeitem)
        return selected_treeitem.primevalue

    def get_values(self, positions: slice) -> List[Any]:
        """
        Gets the primevalues of the sliced tree items.

        Args:
            positions(slice):
                Slicing the PathMap real paths.

        Returns:
            Any:
                *primevalue*s of the sliced tree items
        """
        if self._parent.is_empty():
            return []
        selected_real_paths = self._parent.real_paths[positions]
        requested_values = []
        for real_path in selected_real_paths:
            treeitem = self.by_real_path(real_path)
            requested_values.append(treeitem.primevalue)
        return requested_values

    def set_value_of_treeitem(self, position: int, value: Any):
        assert isinstance(position, int), "position needs to be an integer."
        assert position >= 0, "position needs to be a positive integer or zero."
        treeitem = self.by_position(position)
        self._set_new_value_of_treeitem(treeitem, value)

    def set_value_of_treeitems(self, positions: slice, value: Any):
        selected_real_paths: DataFrame = self._parent.real_paths[positions]
        for real_path in selected_real_paths:
            treeitem = self.by_real_path(real_path)
            self._set_new_value_of_treeitem(treeitem, value)

    @staticmethod
    def _set_new_value_of_treeitem(
        target_treeitem: AnAugmentedTreeItem, new_value: Any
    ):
        """
        Sets a *new_value* of the supplied tree item-

        Args:
            target_treeitem(AnAugmentedTreeItem):
                Targeted tree in which the new value should be set.

            new_value(Any):
                The new value for the tree item.
        """
        parent_treeitem = target_treeitem.parent
        assert (
            parent_treeitem is not None
        ), "The treeitem {} must have a parent, but doesn't have one."
        items_access_key = target_treeitem.primekey
        parent_treeitem[items_access_key] = new_value


class PathMap(object):
    """
    A map of an augmented tree.

    Args:
        pathmap_table(Optional[DataFrame]):
            pandas.DataFrame table with real_path, augmented_path,
            meta_attributes, real_key and primekey of each tree item;
            with the real_key as additional index.

        all_parents_of_treeitems(Optional[Dict[str, AnAugmentedTreeItem]]):
            The parent tree item for each tree item; key is the real_path.

        search_pattern(str):
            The regular expression, which lead to this PathMap.
    """

    METAATTRIBUTE_DELIMITER = "/"

    class ColumnNames:
        REAL_PATH = "real_path"
        AUGMENTED_PATH = "augmented_path"
        META_ATTRIBUTES = "meta_attributes"
        REAL_KEY = "real_key"
        PRIMEKEY = "primekey"

    def __init__(
        self,
        pathmap_table: DataFrame = None,
        all_parents_of_treeitems: Dict[str, AnAugmentedTreeItem] = None,
        search_pattern: str = None,
    ):
        """
        A map of an augmented tree.

        Args:
            pathmap_table(Optional[DataFrame]):
                pandas.DataFrame table with real_path, augmented_path,
                meta_attributes, real_key and primekey of each tree item;
                with the real_key as additional index.

            all_parents_of_treeitems(Optional[Dict[str, AnAugmentedTreeItem]]):
                The parent tree item for each tree item; key is the real_path.

            search_pattern(str):
                The regular expression, which lead to this PathMap.
        """
        self.pathmapitems = _PathMapItems(self)
        self.treeitems = _TreeItems(self)

        if all_parents_of_treeitems is None:
            self._all_parents_of_treeitems = {}
        else:
            self._all_parents_of_treeitems = all_parents_of_treeitems

        if pathmap_table is None:
            self._treepath_table: DataFrame = DataFrame()
        else:
            self._treepath_table = pathmap_table

        if search_pattern is None:
            self.search_pattern = "*"
        else:
            self.search_pattern = search_pattern

    def iterrows(self) -> Generator[Tuple[str, Series], None, None]:
        for real_path, treeitem_metadata in self._treepath_table.iterrows():
            # Within in this class the index of subtable is a str
            # noinspection PyTypeChecker
            yield real_path, treeitem_metadata

    def __bool__(self):
        return self.is_empty()

    def is_empty(self):
        return self._treepath_table.empty

    @property
    def real_paths(self):
        return self._treepath_table[self.ColumnNames.REAL_PATH]

    @property
    def augmented_paths(self):
        return self._treepath_table[self.ColumnNames.AUGMENTED_PATH]

    @property
    def meta_attributes(self):
        return self._treepath_table[self.ColumnNames.META_ATTRIBUTES]

    def get_treeitem_metadata(self, real_path: str) -> Series:
        """
        Retrieves a treeitem's meta data as a *pandas.Series* for the
        given *real_path* of the tree item.

        Args:
            real_path(str):
                real path of the requested tree item.

        Returns:
            Series
        """
        try:
            item_metadata = self._treepath_table.loc[real_path]
            return item_metadata
        except KeyError:
            raise KeyError(
                "real_path '{}' doesn't exists in this pathmap.".format(real_path)
            )

    def get_slice_of_treeitem_metadata(self, positions: slice) -> DataFrame:
        """
        Retrieves a treeitem's meta data as a *pandas.DataFrame* for the
        given *slice*.

        Args:
            positions(slice):
                real path of the requested tree item.

        Returns:
            pandas.DataFrame
        """
        slice_of_items_metadata = self._treepath_table.iloc[positions]
        return slice_of_items_metadata

    def get_parent_of_treeitem_by_real_path(self, real_path_of_treeitem: str):
        """
        Retrieves the parent of the tree item by its real path.

        Args:
            real_path_of_treeitem(str):
                Real path of the tree item, which parent tree item should be
                retrived.

        Returns:
            AnAugmentedTreeItem:
                Parent of the requested tree item's *real_path*.
        """
        return self._all_parents_of_treeitems[real_path_of_treeitem]

    def get_parent_of_treeitem_by_index(self, row_index: int):
        """
        Retrives the parent tree item of the tree item with at the path map's
        row.

        Args:
            row_index(integer):
                Row integer index of the tree item, which parent should be
                retrieved.

        Returns:
            Parent tree item of the tree item at the path map's row.
        """
        items_real_path = self._treepath_table.index[row_index]
        parent_of_treeitem = self.get_parent_of_treeitem_by_real_path(items_real_path)
        return parent_of_treeitem

    @staticmethod
    def _select_submap_from_dataframe(
        treepath_table, selection_pattern: str, target_column_name
    ) -> DataFrame:
        """
        Returns all entries of the pathmap which fits to the `query` at the
        `target_column_name`.

        Args:
            treepath_table(DataFrame):
                Table from which items will be selected.

            selection_pattern(str):
                A regular expression by which the entries are selected.

            target_column_name(str):
                The column within the tree item path table, which is to be
                used for the search.

        Returns:
            pandas.DataFrame:
                Selected items in regard of the `query` within the
                `target_column_name`.
        """
        assert target_column_name is not None, "target_column_name cannot be None."
        indexes = treepath_table[target_column_name].str.match(selection_pattern)
        selected_map = treepath_table[indexes]
        return selected_map

    def _select_submap(self, selection_pattern: str, target_column_name) -> DataFrame:
        """
        Returns all entries of the pathmap which fits to the `query` at the
        `target_column_name`.

        Args:
            selection_pattern(str):
                A regular expression by which the entries are selected.

            target_column_name(str):
                The column within the tree item path table, which is to be
                used for the search.

        Returns:
            pandas.DataFrame:
                Selected items in regard of the `query` within the
                `target_column_name`.
        """
        return self._select_submap_from_dataframe(
            self._treepath_table, selection_pattern, target_column_name
        )

    @staticmethod
    def _turn_iterables_to_unixfilepatterns(
        search_parts,
    ) -> List[Union[str, UnixFilePatternParts, RegularExpressionParts]]:
        appropriate_search_parts = []
        for search_part in search_parts:
            if isinstance(search_part, (list, tuple)):
                clean_part = UnixFilePatternParts(*search_part)
            else:
                clean_part = search_part
            appropriate_search_parts.append(clean_part)
        return appropriate_search_parts

    def sort(self, sorting_method: Optional[Callable[[PathMapItem], int]] = None):
        """
        Sorts the items within this map by their augmented path.

        Args:
            sorting_method(Callable[[PathMapItem], int], optional):
                Custom method to tag PathMapItems of this selection with a
                ascending integer number.
        """
        if sorting_method is None:
            self._default_sort()
        else:
            self._custom_sort(sorting_method)

    def _default_sort(self):
        """
        By default the items are sorted by their augmented path.
        """
        self._treepath_table = self._treepath_table.sort_values(
            by=[PathMap.ColumnNames.AUGMENTED_PATH]
        )

    def _custom_sort(self, sorting_method: Optional[Callable[[PathMapItem], int]]):
        """
        Sorts the items using a custom user method by the PathMapItems.

        Args:
            sorting_method(Callable[[PathMapItem], int]):
                Custom method to tag PathMapItems of this selection with a
                ascending integer number.
        """
        tagged_real_paths = []
        for path_map_item in self.pathmapitems:
            order_number = sorting_method(path_map_item)
            tagged_real_paths.append([path_map_item.real_path, order_number])
        ordered_real_paths_and_numbers = sorted(tagged_real_paths, key=lambda x: x[1])
        custom_ordered_real_paths = [item[0] for item in ordered_real_paths_and_numbers]
        self._treepath_table = self._treepath_table.loc[custom_ordered_real_paths]

    def select(self, *search_parts) -> "PathMap":
        """
        Selects tree items on base of the supplied w*search_parts*, which are
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
            PathMap:
                Selection of augmented tree items.
        """
        fitting_search_parts = self._turn_iterables_to_unixfilepatterns(search_parts)
        selection_query = create_selection_pattern(*fitting_search_parts)
        selection = self._select_submap(
            selection_query, self.ColumnNames.AUGMENTED_PATH
        )
        pathmap_of_selection = PathMap(
            pathmap_table=selection,
            all_parents_of_treeitems=self._all_parents_of_treeitems,
            search_pattern=selection_query,
        )
        return pathmap_of_selection

    def where(self, *search_parts) -> "PathMap":
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
            PathMap:
                Selection of augmented tree items.
        """
        fitting_search_parts = self._turn_iterables_to_unixfilepatterns(search_parts)
        where_searchables = convert_to_where_searchable_parts(*fitting_search_parts)

        selection = self._where_select_by_all_parts(where_searchables)
        where_searchables_representation = str(where_searchables)
        pathmap_of_selection = PathMap(
            pathmap_table=selection,
            all_parents_of_treeitems=self._all_parents_of_treeitems,
            search_pattern=where_searchables_representation,
        )
        return pathmap_of_selection

    def _where_select_by_all_parts(
        self, where_searchable_search_parts: List[str]
    ) -> DataFrame:
        reduced_frame = self._treepath_table.copy()
        for where_searchable_search_part in where_searchable_search_parts:
            if reduced_frame.empty:
                return reduced_frame
            reduced_frame = self._select_submap_from_dataframe(
                reduced_frame,
                where_searchable_search_part,
                self.ColumnNames.META_ATTRIBUTES,
            )
        return reduced_frame

    @staticmethod
    def _group_metaattributes(metaattribute_parts: Iterable) -> Iterator:
        """
        Taken from https://docs.python.org/3.8/library/itertools.html#recipes at
        grouper.
        Collects data into fixed-length chunks or blocks.

        Examples:

            >>> # noinspection PyProtectedMember
            >>> list(
            >>>     PathMap._group_metaattributes(
            >>>         ['a', 'b', 'c', 'd']
            >>>     )
            >>> )
            [('a', 'b') ('c', 'd')]

        Args:
            metaattribute_parts(Iterable):
                An iterable, which will be grouped into groups of *group_size*.
        Returns:
            Iterator
        """
        # Group size of metaattibutes is 2
        key_value_pairs = [iter(metaattribute_parts)] * 2
        # uneven occurrences are filled with empty strings
        return zip_longest(*key_value_pairs, fillvalue="")

    @staticmethod
    def convert_pathlike_metaattributes(
        pathlike_metaattribute: str,
    ) -> List[Tuple[str, str]]:
        """
        Converts a pathlike *meta attribute* from this path map to a
        sequence of key and value tuples.

        Examples:

            >>> PathMap.convert_pathlike_metaattributes(
            >>>    "/key1/value1/key2/value2/"
            >>> )
            [("key1", "value1"), ("key2", "value2")]

        Args:
            pathlike_metaattribute(str):
                A string like a tree path with an addition of a closing
                delimiter.

        Returns:
            List[Tuple[str, str]]:
                Sequence of key, value pairs
        """
        all_without_first_and_last = slice(1, -1, 1)
        splitted_parts = pathlike_metaattribute.split(PathMap.METAATTRIBUTE_DELIMITER)
        metaattribute_parts = splitted_parts[all_without_first_and_last]
        metaattributes = list(PathMap._group_metaattributes(metaattribute_parts))
        return metaattributes

    @staticmethod
    def convert_metaattributes_to_pathlike(
        meta_attributes: List[Tuple[str, str]]
    ) -> str:
        converted_attribute_pairs = []
        for attribute_name, attribute_value in meta_attributes:
            formatted_pair = "{}{}{}".format(
                attribute_name, TreePath.DELIMITER, attribute_value
            )
            converted_attribute_pairs.append(formatted_pair)
        combined_metaattributes = TreePath.DELIMITER.join(converted_attribute_pairs)
        meta_attributes_alike_treepath = TreePath.DELIMITER + combined_metaattributes
        meta_attributes_alike_treepath += TreePath.DELIMITER
        return meta_attributes_alike_treepath

    def from_treeitem(self, treeitem: AnAugmentedTreeItem):
        treepaths_n_parent_treeitems = treeitem.get_pathmap()
        data_of_mapping_frame = []
        for treepath, parent_treeitem in treepaths_n_parent_treeitems:
            real_item_path = treepath.real_path
            augmented_item_path = treepath.augmented_path
            real_item_path = real_item_path.replace("/" + AUGMENTATION_ROOT_KEY, "")
            augmented_item_path = augmented_item_path.replace(
                "/" + AUGMENTATION_ROOT_KEY, ""
            )
            meta_attribute_alike_treepath = self.convert_metaattributes_to_pathlike(
                treepath.meta_attributes
            )
            items_primekey = treepath.primekey
            items_real_key = treepath.real_key
            items_data = [
                real_item_path,
                augmented_item_path,
                meta_attribute_alike_treepath,
                items_real_key,
                items_primekey,
            ]
            data_of_mapping_frame.append(items_data)
            self._all_parents_of_treeitems[real_item_path] = parent_treeitem
        columnnames = [
            self.ColumnNames.REAL_PATH,
            self.ColumnNames.AUGMENTED_PATH,
            self.ColumnNames.META_ATTRIBUTES,
            self.ColumnNames.REAL_KEY,
            self.ColumnNames.PRIMEKEY,
        ]
        self._treepath_table = DataFrame(data_of_mapping_frame, columns=columnnames)
        real_path_as_index = self._treepath_table[self.ColumnNames.REAL_PATH].to_list()
        self._treepath_table.set_index([real_path_as_index], inplace=True)
