import json
from typing import Any, Collection, Mapping, Sequence

from bento.finding import Finding
from bento.formatter.base import FindingsMap, Formatter


class Json(Formatter):
    """Formats output as a single JSON blob."""

    IGNORED_FIELDS = {"filtered"}

    @staticmethod
    def to_dict(finding: Finding) -> Mapping[str, Any]:
        d = finding.to_dict(Json.IGNORED_FIELDS, add_syntactic_id=True)
        return d

    @staticmethod
    def to_py(findings: FindingsMap) -> Sequence[Mapping[str, Any]]:
        return [Json.to_dict(v) for violations in findings.values() for v in violations]

    def dump(self, findings: FindingsMap) -> Collection[str]:
        return [json.dumps(self.to_py(findings))]
