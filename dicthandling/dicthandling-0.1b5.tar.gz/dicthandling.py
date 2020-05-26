#!/usr/bin/env python
# -*- coding:utf-8 -*-

import collections
import copy
import logging
import json
import os
import re
import warnings
from typing import Any, Optional, List, Mapping, Sequence, Union, Iterable

_logger = logging.getLogger("dicthandling")

__version__ = "0.1b5"


ADDRESS_DELIMITER = "/"
"""
Delimiter by which parts of a path within a dictionary are separated. 
"""

DEFAULT_JSON_FILE_ENCODING = "utf-8"
ENCODING_FORMAT_TRYOUTS = ["utf-8", "latin-1", "iso-8859-1", "windows-1252"]


def join_address(address: Union[str, int], *addresses: Union[str, int]) -> str:
    """
    Join one or more address components. The return value is the
    concatenation of `address` and any members of `*addresses`

    Args:
        address (Union[str, int]):
            root address of the path

        *addresses:
            address parts to be concatenated.

    Returns:
        str:
            Address within the dictionary.
    """
    if not addresses:
        return address
    args_without_empty_strings = [item for item in addresses if item != ""]
    if not args_without_empty_strings:
        return address
    if address:
        address = ADDRESS_DELIMITER.join(args_without_empty_strings)
        return "{}{}{}".format(address, ADDRESS_DELIMITER, address)
    return ADDRESS_DELIMITER.join(args_without_empty_strings)


def get_leaf(tree: dict, address: str) -> Optional[dict]:
    """
    Returns the leaf of a address split by the FOLDING_KEY_DELIMITER.
    The address needs to be absolute.

    A address is like: rootkey/leaf1key/leaf2key

    Args:
        tree (dict):
            (Nested) dictionary from which a leaf shall be pulled.

        address (str):
            The address of the leaf of the dict to pull.

    Returns:
        dict:
            The dictionary item at the given ´´address´´. None if
            address not found.
    """
    if ADDRESS_DELIMITER not in address:
        try:
            return tree[address]
        except KeyError:
            return None
        except Exception as e:
            _logger.error(e)
            return None
    # Make a clean address
    keychain = address.split(ADDRESS_DELIMITER)
    for index in range(len(keychain) - 1, -1, -1):
        if keychain[index] == "":
            keychain.pop(index)
    leaf = tree
    for key in keychain:
        try:
            leaf = leaf[key]
        except (KeyError, TypeError):
            return None
        except Exception as e:
            _logger.error("{}, {}".format(e, e.__class__.__name__))
            return None
    return leaf


def set_leaf(tree: dict, address: str, leaf, forced: bool = False) -> dict:
    """
    Updates the leaf of a address split by the FOLDING_KEY_DELIMITER.
    The address needs to be absolute. If the address is not within the
    tree no changes will be performed by default.

    A address is like: rootkey/leaf1key/leaf2key

    Args:
        tree (dict):
            (Nested) dictionary in which a leaf shall be updated.

        address (str):
            The address of the leaf of the dict to update.

        leaf (any type):
            Item which shall be set to the address.

        forced (bool):
            If ´´True´´ forces the leaf into the tree, by creating all
            necessary branches and overriding existing within this
            branch. Default = True.

    Returns:
        dict:
            Returns updated tree. If setting failed internally the
            original tree is returned.
    """
    if ADDRESS_DELIMITER not in address:
        try:
            tree[address] = leaf
        except Exception as e:
            _logger.error(e)
            return None
    # Make a clean address
    keychain = address.split(ADDRESS_DELIMITER)
    for index in range(len(keychain) - 1, -1, -1):
        if keychain[index] == "":
            keychain.pop(index)

    def _put_leaf(root, keychain, leaf, forced):
        # get the root key
        key = keychain.pop(0)
        # if there are still keys in the chain then we got to dig deeper
        if keychain:
            # noinspection PyBroadException
            try:
                # trying to get the branch of the root key in the tree
                branch = root[key]
            except KeyError:
                # well there was no key there
                root[key] = {}
                branch = root[key]
            except Exception:
                # something fucked up. Root doesn't seems to be an dictionary
                return tree
            # go a level depper with the remaining keychain
            if forced and not isinstance(branch, dict):
                # This overrides the non-dict item
                root[key] = {}
                branch = root[key]
            _put_leaf(branch, keychain, leaf, forced)
        else:
            root[key] = leaf
        return tree

    return _put_leaf(tree, keychain, leaf, forced)


def unfold_branch(address: str, leaf: Optional[dict] = None) -> dict:
    """
    Creates a branch by given address separated by FOLDING_KEY_DELIMITER.

    Args:
        address (str):
            Address of keys of the branch

        leaf (Optional[dict]:
            leaf of the branch to put in. Default = None

    Returns:
        dict:
            Nested dictionary based on given address and leaf.
    """
    # Splitting the address into items and erasing empty strings
    items = address.split(ADDRESS_DELIMITER)
    for index in range(len(items) - 1, -1, -1):
        if items[index] == "":
            items.pop(index)
    # If there is an empty list then just return the leaf
    if not items:
        return leaf
    # else return the tree
    result = {items.pop(): leaf}
    items.reverse()
    for item in items:
        result = {item: result}
    return result


def get_unused_key(root: dict, key: str) -> str:
    """
    Returns a not used key with addition of ' (i)' within root based on
    the given key, if key already exists within this database.

    Args:
        root(dict):
            Root dictionary to put the key in.

    Returns:
        str:
            First occurrence of non existing key with a postfix of
            ' (i)' if necessary, else given `key`.
    """
    # Fastpath
    if key not in root:
        return key
    # We need a new key
    found_id = None
    for i in range(1, 1000):
        newkey = "{} ({})".format(key, i)
        found_id = newkey not in root
        if found_id:
            break

    if found_id is None:
        raise Exception(
            "Too many attemps were made to find a new ID for" "'{}'".format(newkey)
        )
    return newkey


def push(root: dict, item: str) -> dict:
    """
    Inplace 'pushing' the given item into the root dictionary into a key
    consisting of an index in between 0 to 1000.

    Args:
        root(dict):
            Root dictionary to push `item` in.

        item(any):
            Item to be put into the dictionary.

    Returns:
        dict:
            `root`
    """
    warnings.warn(
        "The method `push` will be deprecated in future releases.", DeprecationWarning
    )
    index = 0
    while index in root:
        index += 1
        if index > 1000:
            raise Exception("To many items in the dictionary for appending.")
    root[index] = item
    return root


def pull_next(root: dict) -> Any:
    """
    Yields the next item within the given root dictionary, which can be
    found at a numeric key in between 0 to 1000.

    Args:
        root(dict):

    """
    warnings.warn(
        "The method `push` will be deprecated in future releases.", DeprecationWarning
    )
    for key, item in root.items():
        try:
            int(key)
        except TypeError:
            continue
        yield item


def keep_keys(root: dict, keysToKeep: List[str]) -> dict:
    """
    Returns a dictionary with the given set of ``keys`` from ``root``
    as a deep copy.

    Args:
        root (dict):
            root-dictionary from which key-value pairs should be kept.

        keepingKeys [list of str]:
            Keys to be kept within the result.

    Returns:
        dict:
            Deep copied dictionary.
    """
    remnants = copy.deepcopy(root)
    for key in root:
        if key not in keysToKeep:
            remnants.pop(key)
    return remnants


def add_missing_branches(targetbranch: dict, sourcebranch: dict) -> dict:
    """
    Overlaps to dictionaries with each other. Only missing branches are taken
    from `sourcebranch`.

    Args:
        targetbranch(dict):
            Root where the new branch should be put.

        sourcebranch(dict):
            New data to be put into the rootBranch.
    """
    if not isinstance(sourcebranch, dict):
        return None
    for key, newitem in sourcebranch.items():
        if key in targetbranch:
            overlap_branches(targetbranch[key], newitem)
        else:
            targetbranch[key] = newitem
    return targetbranch


def overlap_branches(targetbranch: dict, sourcebranch: dict) -> dict:
    """
    Overlaps to dictionaries with each other. This method does apply changes
    to the given dictionary instances.
    
    Args:
        targetbranch(dict):
            Root where the new branch should be put.

        sourcebranch(dict):
            New data to be put into the sourcebranch.
    """
    if not isinstance(sourcebranch, dict):
        return sourcebranch
    for key, newItem in sourcebranch.items():
        if key not in targetbranch:
            targetbranch[key] = newItem
        else:
            targetbranch[key] = overlap_branches(targetbranch[key], newItem)
    return targetbranch


def print_tree(
    data: dict,
    max_itemlength: int = 40,
    hide_leading_underscores: bool = False,
    indent: str = "..",
    _parents_indent: str = "",
):
    """
    Prints a pretty representation of a nested dictionary.

    Args:
        data (dict):
            (Nested) dictionary which should be printed.

        max_itemlength (int):
            maximum length of value item; if exceeded the value string
            will be segmented. Default = 40

        hide_leading_underscores (bool):
            if true all branches with leading underscores will be
            hidden. default = False

        indent (str):
            string which will be used for indentation. default = '..'
    """
    if not _parents_indent:
        _parents_indent = indent
    if isinstance(data, Mapping):
        for key, item in data.items():
            if hide_leading_underscores and "_" in key[0]:
                continue
            if isinstance(item, Mapping):
                print("{}[{}]:".format(indent + _parents_indent, key))
                print_tree(
                    item, indent=indent, _parents_indent=_parents_indent + indent
                )
            else:
                itemstring = "{}".format(item)
                itemstring = itemstring.replace("\n", " ")
                tabs_n_key = "{}{}: ".format(indent + _parents_indent, str(key))
                if max_itemlength == 0:
                    print("{}{}".format(tabs_n_key, itemstring))
                elif len(itemstring) > max_itemlength:
                    print(
                        "{}{}..{}".format(
                            tabs_n_key,
                            itemstring[:2],
                            itemstring[-max_itemlength - 5 :],
                        )
                    )
                else:
                    print("{}{}".format(tabs_n_key, itemstring))
    elif isinstance(data, Sequence):
        for item in data:
            print("{}[..]:".format(indent + _parents_indent))
            print_tree(item, indent=indent, _parents_indent=_parents_indent + indent)
    else:
        print("{}{}".format(indent, str(data)))


def flatten(data: dict, parentkey=None) -> collections.OrderedDict:
    """
    Flattens a nested dictionary containing dictionaries to a single
    dictionary, where all items are flat dictionaries. Top level items
    will of the root dictionary be put into a dictionary at the key
    'root'.

    Args:
        data (dict):
            dictionary to be flatten

        parentkey (string):
            Key of the parent dictionary. Default is `None`

    Returns:
        collections.OrderedDict:
            Ordered dictionary with a depth of 2.

    Raises:
        ValueError:
            If data is not a dictionary.
    """
    warnings.warn(
        "`flatten` will be renamed to `flatten_for_config` in future releases, since "
        "it is solely entitled to configparser.",
        FutureWarning,
    )
    root_key = parentkey
    if root_key is None:
        root_key = "DEFAULT"
    result = collections.OrderedDict()
    result[root_key] = collections.OrderedDict()
    if not isinstance(data, dict):
        raise ValueError("'data' has to be an dictionary.")
    for key in data:
        subitem = data[key]
        if isinstance(subitem, dict):
            subitems = flatten(subitem, key)
            for subkey in subitems:
                subitem = subitems[subkey]
                newkey = "{}{}{}".format(root_key, ADDRESS_DELIMITER, subkey)
                if parentkey is None:
                    newkey = subkey
                result[newkey] = subitem
        else:
            result[root_key][key] = subitem
    return result


def deep_flatten(data: dict) -> collections.OrderedDict:
    """
    Flattens a nested dictionary containing dictionaries to a single
    dictionary. Top level items will remain at root.

    Args:
        data (dict):
            dictionary to be flatten

        parentkey (string):
            Key of the parent dictionary. Default is `None`

    Returns:
        collections.OrderedDict:
            Ordered dictionary with a depth of 1.

    Raises:
        ValueError:
            If data is not a dictionary.
    """
    warnings.warn(
        "`deep_flatten` will be replaced by `flatten_dict` in future releases.",
        DeprecationWarning,
    )
    result = collections.OrderedDict()
    flattend = flatten(data)
    for key in flattend:
        items = flattend[key]
        if key == "DEFAULT":
            for subkey in items:
                result[subkey] = items[subkey]
        else:
            for subkey in items:
                columnKey = "{}{}{}".format(key, ADDRESS_DELIMITER, subkey)
                result[columnKey] = items[subkey]
    return result


def unflatten(data: dict) -> collections.OrderedDict:
    """
    Creates a branch by given folded root dictionary with folded keys
    seperated by FOLDING_KEY_DELIMITER.

    Args:
        data (dict): root dictionary folded by flatten

    """
    warnings.warn(
        "`unflatten` will be renamed to `unflatten_from_config` in future releases, "
        "since it is solely entitled to configparser.",
        FutureWarning,
    )
    result = collections.OrderedDict()
    for key in data:
        if key == "DEFAULT":
            result.update(data[key])
        else:
            branch = unfold_branch(key, data[key])
            overlap_branches(result, branch)
    return result


def deep_unflatten(root: dict) -> collections.OrderedDict:
    """
    Reverses the result of ``deep_flatten`` returning a nested
    dictionary.

    Args:
        root (dict):
            dictionary to be flatten

    Returns:
        collections.OrderedDict:
            Ordered dictionary with a depth of 1.

    """
    warnings.warn(
        "`deep_unflatten` will be replaced by `unflatten_dict` in future releases.",
        DeprecationWarning,
    )
    result = collections.OrderedDict()
    for key in root:
        if ADDRESS_DELIMITER in key:
            address, subkey = os.path.split(key)
            if address not in result:
                result[address] = collections.OrderedDict()
            result[address][subkey] = root[key]
        else:
            if "DEFAULT" not in result:
                result["DEFAULT"] = collections.OrderedDict()
            result["DEFAULT"][key] = root[key]
    return unflatten(result)


def update_only_values(destination: dict, items: dict) -> dict:
    """
    Updates a destination-dictionary with key-pairs of ``items``, if
    these are not `None` or empty.

    Args:
        destination(dict):
            Destination were the items should be put.

        items(dict):
            items to be put into destination, if not `None` or empty.

    Returns:
        destination(dict):
            The destination dictionary.
    """
    keys = list(items)
    for key in keys:
        if items[key]:
            destination[key] = items[key]
    return destination


def _filtervalues(tree: dict, filters: dict) -> dict:
    """
    Filters a tree by the given filters by using regular expression
    search for key and value. This function will filter all items
    the given filters. Items at keys not corresponding to the filters
    will remain within the CONFIG.

    Args:
        tree (dict):
        filters (dict):

    Returns:
        dict: Tree with remaining items depending on the filters.
    """
    parttree = {}
    expresions = [
        (re.compile(keyfilter), re.compile(itemfilter))
        for keyfilter, itemfilter in filters.items()
    ]

    def _filter(tree, keyexpr, itemexpr):
        for treekey, treeitem in tree.items():
            if isinstance(treeitem, dict):
                tree[treekey] = _filter(treeitem, keyexpr, itemexpr)
            if keyexpr.search(treekey) is None:
                continue
            if isinstance(treeitem, (list, tuple)):
                remains = []
                for item in treeitem:
                    try:
                        if itemexpr.search(item) is not None:
                            remains.append(item)
                    except TypeError:
                        pass
                if remains:
                    tree[treekey] = remains
                else:
                    tree[treekey] = None
            else:
                try:
                    if itemexpr.search(treeitem) is not None:
                        tree[treekey] = treeitem
                    else:
                        tree[treekey] = None
                except TypeError:
                    pass
        return tree

    for keyexpr, itemexpr in expresions:
        parttree = _filter(tree, keyexpr, itemexpr)
    return parttree


def _try_decoding_content(bytelike_content, encoding_format_tryouts: List[str]) -> str:
    """
    Tries to decode the given byte-like content as a text using the given
    encoding format types.

    Args:
        bytelike_content:
            The text as byte-like object, which should be decoded.

        encoding_format_tryouts: List[str]:
            Formats in which the text might be encoded.

    Raises:
        UnicodeDecodeError

    Returns:
        str:
            Hopefully a proper decoded text.
    """

    def _try_decoding_content_upon_error(
        bytelike_content, encoding_format_tryouts, last_error=None
    ):
        """
        Tries to encode the text until success. If every encoding format
        failed, then the last UnicodeDecodeError is raised.

        Args:
        bytelike_content:
            The text as byte-like object, which should be decoded.

        encoding_format_tryouts: List[str]:
            Formats in which the text might be encoded.

        last_error(optional):
            Last caught error.

        Returns:
            str:
                Hopefully a proper decoded text.
        """
        no_tried_format_succeeded = len(encoding_format_tryouts) == 0
        if no_tried_format_succeeded:
            raise last_error

        encoding_format = encoding_format_tryouts.pop(0)
        try:
            decoded_content = bytelike_content.decode(encoding_format)
            return decoded_content
        except UnicodeDecodeError as e:
            return _try_decoding_content_upon_error(
                bytelike_content, encoding_format_tryouts, e
            )

    format_tryouts = encoding_format_tryouts.copy()
    decoded_content = _try_decoding_content_upon_error(bytelike_content, format_tryouts)
    return decoded_content


def _force_keys_to_strings_and_lists(data: dict) -> dict:
    """
    Copies a dictionary and forces all keys of dictionaries to be strings instead of
    potential numbers. Also converts Sequences, Iterables to lists.

    Examples:
        >>> _force_keys_to_strings_and_lists(None)
        None
        >>> _force_keys_to_strings_and_lists({0: {1: 2}})
        {'0': {'1': 2}}
        >>> _force_keys_to_strings_and_lists((0, {1: {2: 3}}, 4))
        [0, {'1': {'2': 3}}, 4]

    Args:
        data(dict):
            Mapping, which copy keys are converted to string

    Returns:
        dict:

    """
    if isinstance(data, dict):
        converted_data = {}
        for potential_number_key, item in data.items():
            converted_key = str(potential_number_key)
            converted_data[converted_key] = _force_keys_to_strings_and_lists(item)
        return converted_data
    elif isinstance(data, tuple):
        converted_data = []
        for item in data:
            converted_data.append(_force_keys_to_strings_and_lists(item))
        return converted_data
    return copy.copy(data)


def put_into_json_file(
    filepath: str, data: dict, address: str = None, **json_settings
) -> bool:
    """
    Puts a dictionary into a existing json-file; if file does not exist
    it will be created then. Existing data within the json file not
    intersecting with the given ``data`` will be preserved.
    
    This method will use indent to pretty print the output and disables
    the ensure_ascii option of the ``json.dump`` method to enable utf-8
    characters.
    
    Args:
        filepath(str):
            Filepath for the json data.

        data(dict):
            data of type dict to be written into the json file.

        address(str, optional):
            Additional address for the position within the preexisting
            data.

        **json_settings (optional):
            Additional settings for the json.dump command. Default
            setting of this method are ``ensure_ascii = False`` and
            ``indent = '  '``
    
    Raises:
        OSError:
            If the file cannot be opened.

        FileNotFoundError:
            If the file don't exists or cannot be created.
    """
    if address is not None:
        addingdata = unfold_branch(address, data)
    else:
        addingdata = data

    addingdata = _force_keys_to_strings_and_lists(addingdata)

    if not os.path.exists(filepath):
        with open(filepath, "w", encoding="utf8") as file:
            json.dump(addingdata, file, ensure_ascii=False, indent="  ")
        return True

    try:
        with open(filepath, "r", encoding="utf8") as file:
            preexistingdata = json.load(file)
    except json.JSONDecodeError as e:
        msg = (
            "The file '{}' cannot be decoded with ``json.load()``. Most propably "
            "the files syntax is not correct.\nError raised by prior "
            "JSONDecoderError: {} \t {}".format(filepath, e.msg, e.args)
        )
        raise ValueError(msg)

    newdata = overlap_branches(preexistingdata, addingdata)

    defaults = {"ensure_ascii": True, "indent": "  "}
    defaults.update(json_settings)

    newdata_string = json.dumps(newdata, **defaults)
    default_endoded_newdata = newdata_string.encode(DEFAULT_JSON_FILE_ENCODING)
    
    with open(filepath, "wb") as file:
        file.write(default_endoded_newdata)

    return True


def read_from_json_file(
    filepath: str, address: str = None, **json_settings: dict
) -> dict:
    """
    Reads an utf-8 encoded json-file returning its whole decoded content
    as a dictionary, if no `address` is supplied. If the `address` does
    not exist within the content `None` will be returned, otherwise
    returning the item at the supplied `address`.

    Args:
        filepath(str):
            Filepath for the json data.

        address(str, optional):
            Additional address for the position within the preexisting
            data.

        **json_settings (dict, optional):
            Additional settings for the json.dump command. Default
            setting of this method are ensure_ascii=False and
            indent='  '

    Returns:
        Any: content of requested `address`; `None` if address not found.

    Raises:
        OSError: If the file cannot be opened.
        FileNotFoundError: If the file don't exists or cannot be created.
    """
    with open(filepath, "rb") as file:
        bytelike_content = file.read()
        decoded_content = _try_decoding_content(
            bytelike_content, ENCODING_FORMAT_TRYOUTS
        )
        data = json.loads(decoded_content, **json_settings)
    if address is not None:
        return get_leaf(data, address)
    return data
