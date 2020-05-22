from typing import Callable


class ArgChainFnError(KeyError):
    """Errors for when you try and access a non-existing step"""


class ArgChain:
    def __init__(self, path: str, transform: Callable = None):
        self.path = path
        self.transform = transform

    def _get_value_from_previous(self, pipeline):
        try:
            computed_val = pipeline._steps_dict[self.path].__result__
            return computed_val
        except KeyError:
            raise ArgChainFnError(f"Unable to chain arguments for given step: {self.path}")

    def _apply_given_transform(self, value):
        if self.transform is not None:
            return self.transform(value)
        else:
            return value

    def __call__(self, pipeline):
        previous_result = self._get_value_from_previous(pipeline)
        output = self._apply_given_transform(previous_result)
        return output

