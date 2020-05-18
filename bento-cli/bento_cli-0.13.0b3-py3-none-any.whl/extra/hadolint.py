import json
import re
from typing import Any, Dict, Iterable, List, Optional, Pattern, Type

from semantic_version import SimpleSpec

from bento.finding import Finding
from bento.parser import Parser
from bento.tool import JsonR, output, runner
from bento.util import fetch_line_in_file


class HadolintParser(Parser[JsonR]):
    def to_violation(self, result: Dict[str, Any]) -> Finding:
        start_line = result["line"]
        column = result["column"]
        check_id = result["code"]
        message = result["message"]
        path = result["file"]

        path = self.trim_base(path)

        level = result["level"]
        severity = 0
        if level == "error":
            severity = 2
        elif level == "warning":
            severity = 1

        if "DL" in check_id or check_id in ["SC2046", "SC2086"]:
            link = f"https://github.com/hadolint/hadolint/wiki/{check_id}"
        elif "SC" in check_id:
            link = f"https://github.com/koalaman/shellcheck/wiki/{check_id}"
        else:
            link = ""

        line_of_code = (
            fetch_line_in_file(self.base_path / path, start_line) or "<no source found>"
        )

        if check_id == "DL1000":
            message = "Dockerfile parse error. Invalid docker instruction."

        return Finding(
            tool_id=HadolintTool.TOOL_ID,
            check_id=check_id,
            path=path,
            line=start_line,
            column=column,
            message=message,
            severity=severity,
            syntactic_context=line_of_code,
            link=link,
        )

    def parse(self, results: JsonR) -> List[Finding]:
        return [self.to_violation(r) for r in results]


class HadolintTool(runner.Docker, output.Json):
    TOOL_ID = "hadolint"
    DOCKER_IMAGE = "hadolint/hadolint:v1.17.2-8-g65736cb"
    DOCKERFILE_FILTER = re.compile(".*Dockerfile.*", re.IGNORECASE)
    BINARY_NAME = "hadolint"
    BINARY_SPEC = SimpleSpec("~=1.17.2")
    VERSION_MATCH = re.compile(r"Haskell Dockerfile Linter ([\d.]+).*")

    def binary_command(self) -> Optional[List[str]]:
        return (
            []
            if self.has_allowed_binary_version(
                self.BINARY_NAME, self.BINARY_SPEC, match=self.VERSION_MATCH
            )
            else None
        )

    @property
    def parser_type(self) -> Type[Parser]:
        return HadolintParser

    @classmethod
    def tool_id(cls) -> str:
        return cls.TOOL_ID

    @classmethod
    def tool_desc(cls) -> str:
        return "Finds bugs in Docker files (requires Docker)"

    @property
    def file_name_filter(self) -> Pattern:
        return self.DOCKERFILE_FILTER

    @property
    def project_name(self) -> str:
        return "Docker"

    @property
    def docker_image(self) -> str:
        return self.DOCKER_IMAGE

    @property
    def docker_command(self) -> List[str]:
        return ["hadolint", "--format", "json"]

    @property
    def remote_code_path(self) -> str:
        return "/mnt"

    def is_allowed_returncode(self, returncode: int) -> bool:
        return returncode == 0 or returncode == 1

    def run(self, files: Iterable[str]) -> JsonR:
        result = self.run_command(files).stdout
        return json.loads(result)
