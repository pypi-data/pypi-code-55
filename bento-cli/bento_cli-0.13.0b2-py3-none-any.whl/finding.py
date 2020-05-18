import binascii
import textwrap
from typing import Any, Mapping, Optional, Set

import attr
import pymmh3 as mmh3


@attr.s(frozen=True, hash=False)
class Finding:
    """
    N.B.: line and column are 1-based, not 0-based
    """

    BASELINE_IGNORED_FIELDS = {
        "line",
        "column",
        "end_line",
        "end_column",
        "filtered",
        "link",
    }

    tool_id = attr.ib(type=str)
    check_id = attr.ib(type=str)
    path = attr.ib(type=str)
    # cmp is deprecated, but we need to use it for compatibility with 18.x.
    line = attr.ib(type=int, hash=None, cmp=False)
    column = attr.ib(type=int, hash=None, cmp=False)
    message = attr.ib(type=str, hash=None, cmp=False)
    severity = attr.ib(type=int, hash=None, cmp=False)
    syntactic_context = attr.ib(type=str, converter=textwrap.dedent)
    semantic_context = None
    filtered = attr.ib(type=Optional[bool], default=None, hash=None, cmp=False)
    end_line = attr.ib(
        type=Optional[int], default=None, hash=None, cmp=False, kw_only=True
    )
    end_column = attr.ib(
        type=Optional[int], default=None, hash=None, cmp=False, kw_only=True
    )
    link = attr.ib(type=Optional[str], default=None, hash=None, cmp=False, kw_only=True)
    metadata = attr.ib(
        type=Optional[Mapping[str, Any]],
        default=None,
        hash=None,
        cmp=False,
        kw_only=True,
    )

    def syntactic_identifier_int(self) -> int:
        # Use murmur3 hash to minimize collisions

        str_id = str((self.check_id, self.path, self.syntactic_context))
        return mmh3.hash128(str_id)

    def syntactic_identifier_str(self) -> str:
        id_bytes = int.to_bytes(
            self.syntactic_identifier_int(), byteorder="big", length=16, signed=False
        )
        return str(binascii.hexlify(id_bytes), "ascii")

    def __hash__(self) -> int:
        # attr.s equality uses all elements of syntactic_identifier, so
        # hash->equality contract is guaranteed
        return self.syntactic_identifier_int()

    def to_dict(
        self, ignored_fields: Set[str], add_syntactic_id: bool = False
    ) -> Mapping[str, Any]:
        d = attr.asdict(self)
        d = {k: v for k, v in d.items() if k not in ignored_fields and v is not None}
        if add_syntactic_id:
            d["syntactic_id"] = self.syntactic_identifier_str()
        return d

    def to_baseline_dict(self) -> Mapping[str, Any]:
        return self.to_dict(Finding.BASELINE_IGNORED_FIELDS, add_syntactic_id=False)
