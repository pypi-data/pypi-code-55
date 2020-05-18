import json
import re
from abc import abstractmethod
from pathlib import Path
from typing import Iterable, List, Mapping, Optional, Pattern

from semantic_version import SimpleSpec

from bento.finding import Finding
from bento.parser import Parser
from bento.tool import JsonR, output, runner
from bento.util import fetch_line_in_file

SEVERITIES = {"ERROR": 2, "WARNING": 1, "INFO": 0}


class BaseSemgrepParser(Parser[JsonR]):
    @classmethod
    @abstractmethod
    def tool_id(cls) -> str:
        pass

    def parse(self, results: JsonR) -> List[Finding]:
        violations: List[Finding] = []
        for check in results:
            check_id = check["check_id"]
            path = self.trim_base(check["path"])
            start_line = check["start"]["line"]
            start_col = check["start"]["col"]
            end = check.get("end", {})
            check_extra = check.get("extra", {})
            # Custom way to get check_name for sgrep-lint:0.1.10
            message = check_extra.get("message")
            source = (
                fetch_line_in_file(self.base_path / path, start_line)
                or "<no source found>"
            ).rstrip()
            severity = SEVERITIES.get(check_extra.get("severity", "ERROR"), 2)
            violation = Finding(
                tool_id=self.tool_id(),
                check_id=check_id,
                metadata=check_extra.get("metadata"),
                path=path,
                line=start_line,
                column=start_col,
                message=message,
                severity=severity,
                syntactic_context=source,
                end_line=end.get("line"),
                end_column=end.get("col"),
            )

            violations.append(violation)
        return violations


class BaseSemgrepTool(runner.Docker, output.Json):
    DOCKER_IMAGE = "returntocorp/semgrep:0.7.0"
    FILE_NAME_FILTER = re.compile(r".*")
    BINARY_NAME = "semgrep"
    BINARY_SPEC = SimpleSpec(">=0.6.0")

    @property
    @abstractmethod
    def config_str(self) -> str:
        """
        Returns the configuration argument to pass to sgrep
        """
        pass

    def get_config_path(self) -> Optional[Path]:
        """
        Returns the path to the sgrep configuration file _if it is a path_.
        Returns None otherwise.
        """
        return None

    def binary_command(self) -> Optional[List[str]]:
        return (
            [self.BINARY_NAME]
            if self.has_allowed_binary_version(self.BINARY_NAME, self.BINARY_SPEC)
            else None
        )

    @property
    def docker_image(self) -> str:
        return self.DOCKER_IMAGE

    @property
    def remote_code_path(self) -> str:
        return "/home/repo"

    @property
    def additional_file_targets(self) -> Mapping[Path, str]:
        config_path = self.get_config_path()
        if config_path:
            return {config_path: self.config_str}
        else:
            return {}

    @property
    def docker_command(self) -> List[str]:
        return ["--config", self.config_str, "--json"]

    @property
    def file_name_filter(self) -> Pattern:
        return self.FILE_NAME_FILTER

    @property
    def project_name(self) -> str:
        return "Python/JS"

    @classmethod
    def tool_desc(cls) -> str:
        return "Runs checks from r2c's check registry (experimental; requires Docker)"

    def run(self, files: Iterable[str]) -> JsonR:
        output_str = self.run_command(files).stdout.split("\n")
        stdout = output_str[-2]  # last line is blank
        output = json.loads(stdout)
        return output.get("results", [])
