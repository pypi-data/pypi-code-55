from .simple_type import SimpleTypePredictor
from ..utils import normalize

class FloatType(SimpleTypePredictor):

    def __init__(self):
        """Create new float type predictor based on regex."""
        pass

    def convert(self, candidate, **kwargs):
        candidate = str(normalize(candidate)).replace(",", ".")
        candidate = candidate.replace('.', "", (candidate.count('.')-1))
        return float(candidate)

    def validate(self, candidate, **kwargs) -> bool:
        """Return boolean representing if given candidate matches regex for float values."""
        if str(candidate) == "0":
            return True
        if str(candidate).startswith("0") and not str(candidate).replace(",", ".").startswith("0."):
            return False
        try:
            self.convert(candidate)
            return True
        except (ValueError, OverflowError):
           return False
