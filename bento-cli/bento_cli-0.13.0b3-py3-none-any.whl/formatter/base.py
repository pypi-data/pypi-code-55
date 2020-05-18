from abc import ABC, abstractmethod
from typing import Any, Collection, Dict, List, Mapping

import attr

from bento.base_context import BaseContext
from bento.finding import Finding

FindingsMap = Mapping[str, Collection[Finding]]


@attr.s(auto_attribs=True)
class Formatter(ABC):
    """
    Converts tool violations into printable output
    """

    context: BaseContext
    config: Dict[str, Any]

    BOLD = "\033[1m"
    END = "\033[0m"

    @abstractmethod
    def dump(self, findings: FindingsMap) -> Collection[str]:
        """Formats the list of violations for the end user."""
        pass

    @staticmethod
    def path_of(violation: Finding) -> str:
        return violation.path

    @staticmethod
    def by_path(findings: FindingsMap) -> List[Finding]:
        collapsed = (v for violations in findings.values() for v in violations)
        return sorted(collapsed, key=(lambda v: v.path))
