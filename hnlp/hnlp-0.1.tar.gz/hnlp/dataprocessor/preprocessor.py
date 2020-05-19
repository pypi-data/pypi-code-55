from dataclasses import dataclass, field
from pnlp import Text
from typing import List


@dataclass
class Preprocessor:

    # clean, replace ...

    text: str
    pats: list = field(default_factory=list)

    def __post_init__(self):
        self.pt = Text(self.text, self.pats)

    def __call__(self) -> str:
        return "".join(self.pt.extract.mats)
