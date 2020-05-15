import abjad


def respell_chord(chord: abjad.Chord):
    r"""Returns an ``abjad.Container`` with n repetitions of an input
    container.

    ..  container:: example

        The required arguments are an ``abjad.Container`` (or child class) and
        and integer n for the number of repetitions.

        >>> container = abjad.Container(r"c'4 d'4 e'4")
        >>> output_container = auxjad.repeat_container(container, 3)
        >>> abjad.f(output_container)
        {
            %%% \time 3/4 %%%
            c'4
            d'4
            e'4
            c'4
            d'4
            e'4
            c'4
            d'4
            e'4
        }
    """
    if not isinstance(chord, abjad.Chord):
        raise TypeError("'chord' must be 'abjad.Chord'")

    pitch_accidentals = [pitch.accidental for pitch in chord.written_pitches]

############################################################################
    # for i in range(len(chord.note_heads) - 1):
    #     for j in range(i + 1, len(chord.note_heads)):
    #         pass

    # instead of pass, compare and rewrite pitch_accidentals[n] as
    # abjad.Accidental('f') or abjad.Accidental('s')

    respelt_pitches = []
    for pitch, accidental in zip(chord.written_pitches, pitch_accidentals):
        if accidental == abjad.Accidental('f'):
            respelt_pitches.append(pitch._respell_with_flats())
        elif accidental == abjad.Accidental('s'):
            respelt_pitches.append(pitch._respell_with_sharps())
        else:
            respelt_pitches.append(pitch)

    chord.written_pitches = respelt_pitches




chord = abjad.Chord("<a cs' ef' f' gf' as'>4")
abjad.f(chord)
respell_chord(chord)
abjad.f(chord)
