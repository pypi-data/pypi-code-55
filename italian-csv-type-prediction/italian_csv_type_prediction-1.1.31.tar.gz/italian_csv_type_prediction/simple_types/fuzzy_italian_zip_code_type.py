from .integer_type import IntegerType
from .italian_zip_code_type import ItalianZIPCodeType
from ..datasets import load_caps


class FuzzyItalianZIPCodeType(ItalianZIPCodeType):

    def convert(self, candidate) -> str:
        """Convert given candidate to CAP."""
        return super().convert(candidate).zfill(5)