import copy
import random
import abjad


class AdriftFadeIn():
    r"""xxx
    """

    ### INITIALISER ###

    def __init__(self,
                 container: abjad.Container,
                 ):
        super().__init__(container)

    ### PRIVATE METHODS ###

    def _fade_process(self):
        r"""Custom fade in process.
        """
        pass

    def _create_empty_container(self):
        r'xxx'
        self._current_container = abjad.Container()
        duration = abjad.inspect(self._initial_container).duration()
        multimeasure_rest = abjad.MultimeasureRest(
            (4, 4),
            multiplier=abjad.Multiplier(duration),
        )
        abjad.attach(abjad.TimeSignature(duration), multimeasure_rest)
        self._current_container.append(multimeasure_rest)
