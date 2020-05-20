from typing import Dict, List


class Extractor:

    def __init__(self):
        pass

    def extract(self, candidate: str, candidate_type:str, **kwargs) -> Dict:
        raise NotImplementedError(
            "This method must be implemented in the child classes.")

    @property
    def name(self):
        """Return type identified by this predictor."""
        return self.__class__.__name__[:-9]

    def _build_placeholder(self, candidate: str, values: Dict) -> str:
        if len(values)==1:
            return "{{{0}}}".format(list(values.keys())[0])
        for key, value in values.items():
            candidate = candidate.replace(value, "{{{0}}}".format(key))
        return candidate

    def build_dictionary(self, candidate: str, values: Dict) -> str:
        return {
            "placeholder": self._build_placeholder(candidate, values),
            "values": values
        }
