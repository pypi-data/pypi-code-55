from sardine.exceptions.lang.lang_exception import SardineLangException


class UnknownToken(SardineLangException):

    def __init__(self, whole_line: str, line: str, n_line: int):
        n_char = len(whole_line) - len(line)
        msg = f"\nUnknown token on line {n_line + 1}, char {(n_char) + 1}:\n" \
              f"\t{whole_line}\n\t{' ' * n_char}^"
        super().__init__(msg)

    def __repr__(self):
        return "UnknownToken"
