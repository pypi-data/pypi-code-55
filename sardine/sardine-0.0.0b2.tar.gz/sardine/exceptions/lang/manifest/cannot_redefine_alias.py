from sardine.exceptions.lang.lang_exception import SardineLangException


class CannotRedefineAlias(SardineLangException):
    def __init__(self, alias: str):
        super().__init__(f"Tried redefining alias '{alias}'")
