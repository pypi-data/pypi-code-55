import copy
import random
import abjad


class _AdriftContainer():
    r"""xxx
    """

    ### INITIALISER ###

    def __init__(self,
                 container: abjad.Container,
                 *,
                 head_position: int = 0,
                 ):
        r'Initialises self.'
        self._initial_container = copy.deepcopy(container)

    ### SPECIAL METHODS ###

    def __call__(self):
        r"""Calls the drifting process for one iteration, returning an
        ``abjad.Selection``.
        """
        self._fade_process()
        return self.current_container

    ### PUBLIC METHODS ###

    def output_all(self):
        r'xxx'
        pass

    ### PRIVATE METHODS ###

    def _fade_process(self):
        r'xxx'
        pass

    def _remove_random_leaf(self):
        r'xxx'
        pass

    def _add_random_leaf(self):
        r'xxx'
        pass

    ### PUBLIC PROPERTIES ###

    @property
    def current_container(self):
        r"""Read-only property, returns the index of the previously output
        element.
        """
        return copy.deepcopy(self._current_container)
