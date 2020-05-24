from typing import Dict, List
from .digits import Digits
from .length import Length
from .symbols import Symbols
from .feature import Feature
from .spaces import Spaces
from .words import Words


class AnyFeature:
    def __init__(self):
        self._features = [
            feature()
            for feature in (
                Digits, Length, Symbols, Spaces, Words
            )
        ]

    @property
    def supported_features(self):
        """Return list of currently supported features."""
        return [
            feature.name
            for feature in self._features
        ]

    @property
    def features(self) -> List[Feature]:
        return self._features

    def score_values(self, values: List) -> Dict[str, List[bool]]:
        return [
            [feature.score(v) for v in values]
            for feature in self._features
        ]

    def scores(self, values: List) -> Dict[str, List[bool]]:
        """Return prediction from all available type."""
        return dict(zip(self.supported_features, self.score_values(values)))
