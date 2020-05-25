"""Utilities for formatting nested terramare exceptions."""

import enum
from typing import Callable, Generic, List, Mapping, Optional, TypeVar, Union, cast

import attr

from .tree import KeyTree, KeyTreeElement

E = TypeVar("E", bound=Exception)
K = TypeVar("K")


Cause = Union[E, Mapping[str, E]]


@enum.unique
class ErrorDisplayStrategy(enum.Enum):
    """
    Strategy for displaying an exception.

    These aren't particularly well-named, and serve two different purposes:

    - Determining whether an exception's message can be omitted, because
      either:
      - Its cause is a single exception;
      - It is part of a collection of labelled exceptions.
    - Removing "less interesting" exceptions from a collection.

    However, it's non-trivial to split these out, as identifying "less
    interesting" exceptions requires information from both the code raising the
    exception and the code catching it.
    """

    ALWAYS_DISPLAY = enum.auto()
    DEFAULT = enum.auto()
    EAGERLY_COLLAPSE = enum.auto()
    ALWAYS_COLLAPSE = enum.auto()


@attr.s(auto_attribs=True, frozen=True)
class ExceptionData(Generic[K, E]):
    """
    Interface for tree formatted exceptions.

    :var key: Key used for determining exception uniqueness. An exception's
        details will only be displayed once even if it occurs multiple times.
    :var cause: Cause of the exception, either another exception or a labelled
        collection of exceptions.
    :var msg: Exception message.
    :var display_strategy: Strategy for determining how to display the
        exception.
    """

    key: K
    cause: Cause[E]
    msg: str
    display_strategy: ErrorDisplayStrategy


def format_exception(
    exception: E, get_metadata: Callable[[E], ExceptionData[K, E]]
) -> str:
    """Recursively format a tree of exceptions."""

    def get_tree_(
        root: E, prefix: Optional[str] = None, is_root: bool = False
    ) -> KeyTree[K]:
        """Convert an exception to a tree of messages."""

        metadata = get_metadata(root)

        def get_msg(is_leaf: bool) -> str:
            if prefix is None:
                return metadata.msg
            if (
                metadata.display_strategy == ErrorDisplayStrategy.ALWAYS_DISPLAY
                or is_leaf
                or is_root
            ):
                # Always display the message of a leaf or the root, as otherwise
                # the exception doesn't make much sense.
                return f"{prefix}: {metadata.msg}"
            return prefix

        if not isinstance(metadata.cause, Exception):
            children = cast(Mapping[str, E], metadata.cause)
            # Select "interesting" children - those that can't be eagerly
            # collapsed. If none of the children are interesting, select them
            # all.
            strategies = {
                key: get_metadata(child).display_strategy
                for key, child in children.items()
            }
            children = {
                key: children[key] for key in _get_interesting_children(strategies)
            }
            if len(children) != 1 or any(
                strategies[key]
                not in {
                    ErrorDisplayStrategy.ALWAYS_COLLAPSE,
                    ErrorDisplayStrategy.EAGERLY_COLLAPSE,
                }
                for key in children
            ):
                return KeyTree(
                    KeyTreeElement(metadata.key, get_msg(len(children) == 0)),
                    [get_tree_(child, f"[{key}]") for key, child in children.items()],
                )
            else:
                child = list(children.values())[0]
        else:
            child = cast(E, metadata.cause)

        if metadata.display_strategy == ErrorDisplayStrategy.ALWAYS_DISPLAY or is_root:
            return KeyTree(
                KeyTreeElement(metadata.key, get_msg(False)), [get_tree_(child)]
            )
        # If an exception is caused by a single other exception, and the
        # message doesn't need to be displayed, don't include that exception
        # in the tree at all. Instead, replace it by its cause.
        return get_tree_(child, prefix)

    return get_tree_(exception, is_root=True).pretty_print()


def _get_interesting_children(
    strategies: Mapping[str, ErrorDisplayStrategy]
) -> List[str]:
    ranking = [
        ErrorDisplayStrategy.EAGERLY_COLLAPSE,
        ErrorDisplayStrategy.ALWAYS_COLLAPSE,
    ]
    for i in range(len(ranking)):
        interesting = [
            key for key, strategy in strategies.items() if strategy not in ranking[i:]
        ]
        if interesting:
            return interesting
    return list(strategies.keys())
