from arpeggio import ZeroOrMore, EOF, Sequence, OrderedChoice
from arpeggio import RegExMatch as _


def os_release():
    return ZeroOrMore([variable, comment, ''], sep='\n'), EOF


def comment():
    return _(r'#.*$')


def variable():
    def id():
        return _(r'[a-zA-Z_][a-zA-Z_0-9]*')

    def quoted_string():
        def double_quoted():
            return '"', _(r'((\\")|[^"])*'), '"'

        def single_quoted():
            return "'", _(r"((\\')|[^'])*"), "'"

        # a sequence containing a single item -- the ordered choice
        return Sequence(
            [double_quoted, single_quoted],
            skipws=False
        )

    def unquoted_string():
        return _(r'[a-zA-Z_0-9]*')

    def value():
        return [unquoted_string,
                (_(r'\s*'), quoted_string)]

    return id, '=', value
