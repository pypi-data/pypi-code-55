import copy
import random
import abjad


class _AdriftContainer():
    r"""xxx
    """

    def __init__(self,
                 container: abjad.Container,
                 *,
                 head_position: int = 0,
                 ):
        self._initial_container = copy.deepcopy(container)

    def __call__(self):
        self._fade_process()
        return self.current_container

    @property
    def current_container(self):
        return copy.deepcopy(self._current_container)

    def output_all(self):
        pass

    def _fade_process(self):
        pass

    def _remove_random_leaf(self):
        pass

    def _add_random_leaf(self):
        pass
