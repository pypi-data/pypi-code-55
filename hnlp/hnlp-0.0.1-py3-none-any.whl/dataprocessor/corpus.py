from dataclasses import dataclass
from pathlib import Path
from pnlp import Reader


@dataclass
class Corpus:

    name_or_path: str
    pattern: str = ".*"

    def __post_init__(self):
        reader = Reader(pattern)

    def __iter__(self):
        for line in reader(self.name_or_path):
            yield line
