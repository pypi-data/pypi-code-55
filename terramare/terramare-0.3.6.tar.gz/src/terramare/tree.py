"""Tree data structure."""

from typing import Generic, List, Tuple, TypeVar

import attr

K = TypeVar("K")


@attr.s(auto_attribs=True, frozen=True)
class KeyTreeElement(Generic[K]):
    """Element of a KeyTree."""

    key: K
    msg: str


@attr.s(auto_attribs=True, frozen=True)
class KeyTree(Generic[K]):
    """Tree data structure with per-element keys to identify duplicates."""

    element: KeyTreeElement[K]
    children: List["KeyTree[K]"]

    def pretty_print(self, max_width: int = 100) -> str:
        """Pretty-print the tree."""
        seen: List[Tuple[str, K]] = []
        return _pretty_print_recursive(self, seen, max_width=max_width, depth=0)


def _pretty_print_recursive(
    root: KeyTree[K], seen: List[Tuple[str, K]], max_width: int, depth: int,
) -> str:
    def inner(seen: List[Tuple[str, K]]) -> str:
        if not root.children:
            return root.element.msg
        if len(root.children) == 1 and not root.children[0].children:
            # If there's only a single child, and it has no children itself,
            # display this element and its child on a single line...
            rv = root.element.msg + ": " + root.children[0].element.msg
            if 2 * depth + len(rv) <= max_width:
                # Provided the line is not too long!
                return rv
        return "\n".join(
            [root.element.msg + ":"]
            + [
                child_str
                for child_str in [
                    _indent(
                        _pretty_print_recursive(
                            root=child, seen=seen, max_width=max_width, depth=depth + 1
                        ),
                        "- ",
                        "  ",
                    )
                    for child in root.children
                ]
            ]
        )

    root_str = inner([])
    if (root_str, root.element.key) in seen:
        # If this exception has already been seen in the tree, don't display
        # it in full detail - just refer to the previous occurence.
        return f"{root.element.msg} as above"
    root_str = inner(seen)
    seen.append((root_str, root.element.key))
    return root_str


def _indent(s: str, head_prefix: str, tail_prefix: str) -> str:
    return "\n".join(
        [
            (head_prefix if lineno == 0 else tail_prefix) + line
            for lineno, line in enumerate(s.splitlines())
        ]
    )
