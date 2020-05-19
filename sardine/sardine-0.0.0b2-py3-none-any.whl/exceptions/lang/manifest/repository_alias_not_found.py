from sardine.exceptions.lang.lang_exception import SardineLangException


class RepositoryAliasNotFound(SardineLangException):
    def __init__(self, alias: str):
        super().__init__(f"Repository alias not found '{alias}'")
