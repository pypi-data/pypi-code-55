# -*- coding: utf-8 -*-
"""
This module contains methods to augment a nested data structure with
*AnAugmentedTreeItem*-Classes.
"""

from typing import Any, Dict, Union, Mapping, List, Sequence, Optional, Generator, Tuple
from pandas import DataFrame
import numpy as np

from augmentedtree.core import (
    AUGMENTATION_FOR_VALUES,
    AUGMENTATION_FOR_SEQUENCE,
    AUGMENTATION_FOR_MAPPING,
    AUGMENTATION_ROOT_KEY,
    PRIMARYKEY_KEY,
    PRIMARYNAME_KEY,
    PRIMARYVALUE_KEY,
    IGNORE_PREFIX,
    _find_schema,
    get_augmentation_classes,
    get_augmentation_method_for_type,
    MappingSchema,
    TreeItemParameters,
    KeyLink,
    LeafType,
)
from augmentedtree.abstractbaseclasses import AnAugmentedCollection, AnAugmentedTreeItem


def _estimate_tensor_size(sequence):
    # if this sequence is not nested anymore return its length for `childsize`
    # for the recursion
    if len(sequence) == 0:
        return 0
    if not isinstance(sequence[0], (list, tuple)):
        return len(sequence)
    # childsize is the dimension of the child
    childsize = _estimate_tensor_size(sequence[0])
    return childsize * len(sequence)


def _sum_item_sizes(sequence):
    itemsum = 0
    shouldbeflat = False
    for item in sequence:
        # the recursion hit the bottom of the nested sequence and sums up
        # all items, so this sequence should be flat
        if not isinstance(item, (list, tuple)):
            itemsum += 1
            shouldbeflat = True
            continue
        # if there was a flat item before but now a sequence was found
        # this nested sequence is not correct --> returning 0 should fuck up
        # the sum and n x m x .... != sum
        if shouldbeflat:
            return 0
        itemsum += _sum_item_sizes(item)
    return itemsum


def _is_proper_sized_tensor(sequence: Sequence) -> bool:
    """
    A proper sized tensor is a list, tuple, numpy.array.

    Args:
        sequence:

    Returns:

    """
    if not sequence:
        return False
    if isinstance(sequence, str):
        return False
    # this method checks whether this sequence is an matrix/tensor by using
    # sum of array lengths. n x m x ...
    targetsum = _estimate_tensor_size(sequence)
    summed_items = _sum_item_sizes(sequence)
    return targetsum == summed_items


def _sequence_is_value(sequence):
    if not isinstance(sequence, Sequence):
        return False
    if _is_proper_sized_tensor(sequence):
        for item in sequence:
            if isinstance(item, dict):
                return False
        return True
    return False


def _iter_nested_data_items(
    nested_data: Union[Sequence, Mapping], potential_childs_key: Union[int, str] = None
) -> Generator[Tuple[Union[str, int], Any], None, None]:
    if isinstance(nested_data, Sequence):
        if _sequence_is_value(nested_data):
            yield potential_childs_key, nested_data
        for index, item in enumerate(nested_data):
            yield index, item
    elif isinstance(nested_data, Mapping):
        for key, item in nested_data.items():
            yield key, item
    else:
        yield potential_childs_key, nested_data


def _augment_child(
    parent: AnAugmentedCollection,
    childs_key: Union[str, int],
    nested_data: Any,
    augmentclasses: dict,
    use_schemas: bool = True,
):
    """
    Augments the `nested data` as a child of `parent` at `childs_key`.

    Args:
        parent:
        childs_key:
        nested_data:
        augmentclasses:
        use_schemas:

    Returns:

    """
    if isinstance(nested_data, Mapping):
        next_level_parent = _augment_mapping(
            parent, childs_key, nested_data, augmentclasses, use_schemas
        )
        return next_level_parent
    elif isinstance(nested_data, Sequence) and not isinstance(nested_data, str):
        next_level_parent = _augment_sequence(
            parent, childs_key, nested_data, augmentclasses, use_schemas
        )
        return next_level_parent
    else:
        _augment_value(parent, childs_key, augmentclasses)


# noinspection PyCallingNonCallable
def _augment_sequence(
    parent: AnAugmentedCollection,
    childskey: Union[str, int],
    nested_data: Union[Sequence, Mapping],
    augmentclasses: Dict[str, AnAugmentedTreeItem] = None,
    use_schemas: bool = True,
) -> AnAugmentedTreeItem:
    # If the datastructure is a list, there are 3 possibilities.
    # The sequence is empty, nested or is a (nested) value sequence.
    given_sequence_is_a_value = nested_data and _sequence_is_value(nested_data)
    if given_sequence_is_a_value:
        if parent is None:
            raise ValueError(
                "A pure list, which is considered as a value within "
                "an AugmentedTree cannot be augmented as a sole "
                "`nested_data`."
            )
        _augment_value(
            parent=parent, childs_key=childskey, augmentclasses=augmentclasses
        )
        return parent
    # setup the parent for a Sequence
    if parent is None:
        if childskey is None:
            childskey = AUGMENTATION_ROOT_KEY
        next_level_parent = augmentclasses[AUGMENTATION_FOR_SEQUENCE](
            primarykey=childskey, primaryvalue=nested_data
        )
    else:
        child = augmentclasses[AUGMENTATION_FOR_SEQUENCE](
            primarykey=childskey, primaryvalue=nested_data
        )
        parent.insert_child_at(childskey, child)
        next_level_parent = child
    for subchilds_key, subchilds_data in enumerate(nested_data):
        _augment(
            parent=next_level_parent,
            childskey=subchilds_key,
            nested_data=subchilds_data,
            augmentclasses=augmentclasses,
            use_schemas=use_schemas,
        )
    return next_level_parent


# noinspection PyCallingNonCallable
def _augment_mapping(
    parent: AnAugmentedCollection,
    childs_key: Union[str, int],
    nested_data: Union[Sequence, Mapping],
    augmentclasses: Dict[str, AnAugmentedTreeItem] = None,
    use_schemas: bool = True,
) -> AnAugmentedTreeItem:
    if use_schemas:
        type_parent = _augment_by_type_defined_method(
            parent, childs_key, nested_data, augmentclasses
        )
        if type_parent is not None:
            return type_parent

        schema_parent = _augment_by_schema(
            parent, childs_key, nested_data, augmentclasses
        )
        if schema_parent is not None:
            return schema_parent
    if parent is None:
        next_level_parent = augmentclasses[AUGMENTATION_FOR_MAPPING](
            primarykey=AUGMENTATION_ROOT_KEY, primaryvalue=nested_data
        )
    else:
        child = augmentclasses[AUGMENTATION_FOR_MAPPING](
            primarykey=childs_key, primaryvalue=nested_data
        )
        parent.insert_child_at(childs_key, child)
        next_level_parent = child
    for subchilds_key, subchilds_data in nested_data.items():
        _augment(
            parent=next_level_parent,
            childskey=subchilds_key,
            nested_data=subchilds_data,
            augmentclasses=augmentclasses,
            use_schemas=use_schemas,
        )
    return next_level_parent


def _augment_value(parent: AnAugmentedCollection, childs_key, augmentclasses) -> None:
    if parent is None:
        raise TypeError(
            "A non sequence (list, tuple) or mapping (dict) `datastructure` "
            "needs a parent"
        )
    if not parent.has_primekey(childs_key):
        child = augmentclasses[AUGMENTATION_FOR_VALUES](primarykey=childs_key)
        parent.insert_child_at(childs_key, child)


def _augment(
    parent: AnAugmentedCollection,
    childskey: Union[str, int],
    nested_data: Union[Sequence, Mapping],
    augmentclasses: Dict[str, AnAugmentedTreeItem] = None,
    use_schemas: bool = True,
) -> AnAugmentedTreeItem:
    """
    Augments nested data with `AnAugmentedTreeItem`.

    Args:
        parent(AnAugmentedCollection):
            parent of the given `nested_data`

        childskey(Union[str, int]):
            key of the given `nested_data` within `parent`

        nested_data (Union[Sequence, Mapping]):
            nested data to be augmented with `AnAugmentedTreeItem`.

        augmentclasses(Dict[str, AnAugmentedTreeItem]):
            `AnAugmentedTreeItem`-classes to be used for augmentation

        use_schemas:
            As default schemas are used.

    Returns:
        AnAugmentedTreeItem
    """
    # If the instance is a dicitonary each (key, value) pair gets a `TreeItem`
    # if `datastructure` is a mapping
    #   check each item for being a value, mapping or sequence. Sequences
    #   has to be checked if they consist of data or nested deeper.
    if augmentclasses is None:
        augmentclasses = get_augmentation_classes()
    if isinstance(nested_data, AnAugmentedTreeItem):
        return _augment(
            parent, childskey, nested_data.primevalue, augmentclasses, use_schemas
        )
    elif isinstance(nested_data, Mapping):
        return _augment_mapping(
            parent, childskey, nested_data, augmentclasses, use_schemas
        )
    # if `datastructure is a sequence it has to be checked deeper.
    elif isinstance(nested_data, Sequence) and not isinstance(nested_data, str):
        return _augment_sequence(
            parent, childskey, nested_data, augmentclasses, use_schemas
        )
    # If this point is reached, a value was given into this method. Within this model
    # a parent is mandatory for a value; no parent is a major fault within the code.
    _augment_value(parent, childskey, augmentclasses)


def augment_datastructure(
    nested_data: Union[Sequence, Mapping],
    parent: AnAugmentedCollection = None,
    augmentclasses: Dict[str, AnAugmentedTreeItem] = None,
    use_schemas: bool = True,
):
    """
    Augments nested data with `AnAugmentedTreeItem`.

    Args:
        nested_data (Union[Sequence, Mapping]):
            nested data to be augmented with `AnAugmentedTreeItem`.

        parent(AnAugmentedCollection, optional):
            parent of the given `nested_data`

        augmentclasses(Dict[str, AnAugmentedTreeItem], optional):
            `AnAugmentedTreeItem`-classes to be used for augmentation

        use_schemas(bool, optional):
            Defines whether schemas should be used or not.
            Default = `True`; schemas are used.

    Returns:
        AnAugmentedTreeItem
    """
    parent = _augment(
        nested_data=nested_data,
        parent=parent,
        childskey=AUGMENTATION_ROOT_KEY,
        augmentclasses=augmentclasses,
        use_schemas=use_schemas,
    )
    return parent


def _augment_by_type_defined_method(
    parent: AnAugmentedCollection,
    childskey: Union[str, int],
    datastructure: Any,
    augmentclasses: dict,
) -> Optional[AnAugmentedTreeItem]:
    try:
        schema_uid = datastructure[MappingSchema.IDENTIFIER]
    except KeyError:
        return None
    try:
        target = get_augmentation_method_for_type(schema_uid)
    except KeyError:
        return None
    parent = target(parent, childskey, datastructure, augmentclasses)
    return parent


def _augment_by_schema(
    parent: AnAugmentedTreeItem,
    childskey: Union[str, int],
    datastructure: Any,
    augmentclasses: dict,
    do_recursion: bool = True,
) -> Optional[AnAugmentedTreeItem]:

    schema_uid, schema = _find_schema(datastructure)
    if schema is None:
        return None

    kwargs = {
        TreeItemParameters.PRIMARYKEY: None,
        TreeItemParameters.PRIMARYNAME: None,
        TreeItemParameters.PRIMARYVALUE: datastructure,
        TreeItemParameters.OUTERVALUEKEY: None,
        TreeItemParameters.METADATAKEYS: None,
        TreeItemParameters.REAL_KEY: childskey,
    }

    if MappingSchema.PRIMARYKEY in schema:
        fieldkey_to_be_used_as_key = schema[MappingSchema.PRIMARYKEY]
        kwargs[TreeItemParameters.PRIMARYKEY] = KeyLink(fieldkey_to_be_used_as_key)
    else:
        kwargs[TreeItemParameters.PRIMARYKEY] = childskey

    if MappingSchema.PRIMARYNAME in schema:
        fieldkey_to_be_used_as_name = schema[MappingSchema.PRIMARYNAME]
        kwargs[TreeItemParameters.PRIMARYNAME] = KeyLink(fieldkey_to_be_used_as_name)

    if MappingSchema.OUTERVALUES in schema:
        field_containing_the_outervalues = schema[MappingSchema.OUTERVALUES]
        kwargs[TreeItemParameters.OUTERVALUEKEY] = field_containing_the_outervalues
    elif MappingSchema.METAFIELDKEYS in schema:
        fields_defining_invisible_values = schema[MappingSchema.METAFIELDKEYS]
        kwargs[TreeItemParameters.METADATAKEYS] = fields_defining_invisible_values

    if MappingSchema.META_ATTRIBUTES in schema:
        fields_used_for_meta_attributes = schema[MappingSchema.META_ATTRIBUTES]
        kwargs[TreeItemParameters.META_ATTRIBUTES] = fields_used_for_meta_attributes

    if schema_uid in augmentclasses:
        schema_class = augmentclasses[schema_uid]
    else:
        schema_class = augmentclasses[AUGMENTATION_FOR_MAPPING]
    child_with_schema = schema_class(**kwargs)
    if parent is not None:
        parent.insert_child_at(childskey, child_with_schema)
    parent_of_next_level = child_with_schema
    if do_recursion:
        outervalues_of_child = child_with_schema.outervalues
        for childs_key, childs_data in _iter_nested_data_items(outervalues_of_child):
            _augment_child(
                parent=parent_of_next_level,
                childs_key=childs_key,
                nested_data=childs_data,
                augmentclasses=augmentclasses,
                use_schemas=True,
            )
    return parent_of_next_level


def _make_tree_table(
    treeitem: AnAugmentedTreeItem,
    additional_columns: List = None,
    show_hidden: bool = False,
    level: int = 0,
):
    table = []
    primarykey = treeitem.primekey
    primaryname = treeitem.primename
    if primaryname is None:
        primaryname = ""
    leaf_type = treeitem.leaf_type
    parents_leaf_type = None
    if treeitem.parent is not None:
        parents_leaf_type = treeitem.parent.leaf_type

    additional_values = []
    if additional_columns is not None:
        additional_values = [treeitem.data(column) for column in additional_columns]

    row = [level, parents_leaf_type, leaf_type, primarykey, primaryname]
    row += additional_values
    table.append(row)
    for child in treeitem.children:
        check_anything_with_potential_string_as_key = child.parent is not None
        if check_anything_with_potential_string_as_key:
            if not show_hidden:
                childs_key = str(child.data(PRIMARYKEY_KEY))
                try:
                    if childs_key[0] == IGNORE_PREFIX:
                        continue
                except IndexError:
                    pass
        sub_table = _make_tree_table(child, additional_columns, show_hidden, level + 1)
        table.extend(sub_table)
    return table


def dumps_atree(
    treeitem: AnAugmentedTreeItem,
    additional_column_names: List = None,
    show_hidden=False,
    indent="  ",
    prefix="",
):
    """
    Dumps a string of a tree in a simple manner.

    Notes:
        - if the item is within a Sequence the separator between primekey
          and primename will be a dot '.'; else a colon ':'
        - by using schemas the default indexing by integers of Sequences
          can be changed to key-names of a Mapping.

    Args:
        treeitem (AnAugmentedTreeItem):
            Tree item to be printed.

        additional_column_names (str):
            Additional columns which should be shown.

        show_hidden (bool):
            If `True` leading underline keys will be shown. Default =
            `False`

        indent (str):
            Indentation characters which will be used.

        prefix (str):
            Additional string with which line begins.
    """
    if additional_column_names is None:
        additional_column_names = []

    raw_tree_table = _make_tree_table(treeitem, additional_column_names, show_hidden)
    table_columns = ["level", "parents_leaf_type", "leaf_type", "primekey", "primename"]
    table_columns += additional_column_names
    tree_table = DataFrame(raw_tree_table, columns=table_columns)
    tree_table["level"] = tree_table["level"].fillna(0)

    # This section handles exceptions of trees for which a table text is
    # not required.
    first_row = tree_table.iloc[0]
    # Empty collections > print > exit
    if first_row.primekey == AUGMENTATION_ROOT_KEY:
        row_count = len(tree_table)
        is_exception_of_empty_collection = (
            row_count == 1
            and first_row.primename is ""
            and first_row.leaf_type >= LeafType.SEQUENCE
        )
        if is_exception_of_empty_collection:
            if first_row.leaf_type == LeafType.SEQUENCE:
                return prefix + "empty sequence []"
            if first_row.leaf_type == LeafType.MAPPING:
                return prefix + "empty mapping {}"
            return prefix + "Cannot determine collection type to print."
        if first_row.leaf_type == LeafType.SEQUENCE:
            tree_table.loc[0, "primekey"] = "[..]"
        elif first_row.leaf_type == LeafType.MAPPING:
            tree_table.loc[0, "primekey"] = "{..}"
    # Only a value item > print > exit
    if first_row.leaf_type <= LeafType.VALUE:
        return "{}{}".format(prefix, first_row.primename)

    # Within this section the headcolumn consisting of primekey: primevalue
    # is constructed.
    formatted_headcolumn_items = []
    end_of_line_char = "\n"
    for index, tree_table_row in tree_table.iterrows():
        primekey_primename_seperator = ":"
        if tree_table_row.parents_leaf_type == LeafType.SEQUENCE:
            primekey_primename_seperator = "."
        elif tree_table_row.parents_leaf_type is None:
            primekey_primename_seperator = " "
        elif np.isnan(tree_table_row.parents_leaf_type):
            primekey_primename_seperator = " "
        repeat_count = tree_table_row.level
        row_indent = prefix
        row_indent += indent * repeat_count
        items_primekey = tree_table_row.primekey
        items_primename = tree_table_row.primename
        if items_primename is None:
            items_primename = ""
        if items_primename is None:
            items_primename = ""
        items_primename_output = str(items_primename)
        items_primename_is_multiple_line = end_of_line_char in items_primename_output
        if items_primename_is_multiple_line:
            replacement = end_of_line_char + row_indent
            indentation_char = indent[0]
            # +1 for the whitespace
            primekeylength = len(items_primekey + primekey_primename_seperator)+1
            replacement += indentation_char * primekeylength
            items_primename_output = items_primename_output.replace(
                end_of_line_char, replacement
            )
        items_head_column = "{}{}{} {}".format(
            row_indent,
            items_primekey,
            primekey_primename_seperator,
            items_primename_output,
        )
        formatted_headcolumn_items.append(items_head_column)

    formatted_headcolumn = DataFrame(formatted_headcolumn_items, columns=["headcolumn"])
    additional_columns = tree_table[additional_column_names]
    tree_table = formatted_headcolumn.join(additional_columns)

    string_tree_table = tree_table.astype(str)

    # replace 'None' entries within additional columns with empty string.
    for column_name in additional_column_names:
        column = string_tree_table[column_name]
        string_tree_table[column_name] = column.str.replace("None", "")

    # This section determines the max widths of the columns
    max_widths_of_columns = []
    for column_name in string_tree_table.columns:
        column_widths = string_tree_table[column_name].str.len()
        max_columns_width = column_widths.max()
        max_widths_of_columns.append(max_columns_width)

    headcolumn_width = max_widths_of_columns[0]
    widths_of_additional_columns = max_widths_of_columns[1:]

    # finally within this section the resulting text table is constructed.
    returned_text_table = ""
    if additional_column_names:
        column_titels = "".ljust(headcolumn_width + 3, " ")
        for index, column_name in enumerate(additional_column_names):
            if column_name == PRIMARYVALUE_KEY:
                column_name = "Primevalue"
            elif column_name == PRIMARYNAME_KEY:
                column_name = "Primename"
            elif column_name == PRIMARYKEY_KEY:
                column_name = "Primekey"
            column_width = widths_of_additional_columns[index]
            if len(column_name) > column_width:
                column_name = column_name[: column_width - 1] + "."
            column_titels += "{0: ^{1}}   ".format(column_name, column_width)
        returned_text_table += column_titels + "\n"

    for rowindex, tree_table_row in string_tree_table.iterrows():
        headcolumn_value = tree_table_row[0]
        headcolumn_item = "{0: <{1}}".format(headcolumn_value, headcolumn_width)
        if additional_column_names:
            additional_items = []
            for index, column_value in enumerate(tree_table_row[1:]):
                column_width = widths_of_additional_columns[index]
                column_item = "{0: <{1}}".format(column_value, column_width)
                additional_items.append(column_item)
            additional_print_items = " ' ".join(additional_items)
            additional_print_items = " ' " + additional_print_items
        else:
            additional_print_items = ""
        returned_text_table += "{}{}\n".format(headcolumn_item, additional_print_items)
    return returned_text_table


def print_atree(
    treeitem: AnAugmentedTreeItem,
    additional_columns: List = None,
    show_hidden=False,
    indent="  ",
    prefix="",
):
    """
    Pretty prints a tree in a simple manner.

    Notes:
        - if the item is within a Sequence the separator between primekey
          and primename will be a dot '.'; else a colon ':'
        - by using schemas the default indexing by integers of Sequences
          can be changed to key-names of a Mapping.

    Args:
        treeitem (AnAugmentedTreeItem):
            Tree item to be printed.

        additional_columns (str):
            Additional columns which should be shown.

        show_hidden (bool):
            If `True` leading underline keys will be shown. Default =
            `False`

        indent (str):
            Indentation characters which will be used.

        prefix (str):
            Additional string with which line begins.
    """
    print(dumps_atree(treeitem, additional_columns, show_hidden, indent, prefix))
