from typing import List, Union

from sardine.exceptions.lang.lang_exception import SardineLangException


class UnexpectedTokenFound(SardineLangException):

    def __init__(self, unexpected_token_type: str, expected_types: Union[str, List[str]]):
        msg = f"Unexpected token type {unexpected_token_type}."
        if isinstance(expected_types, str):
            msg += f" Was expecting {expected_types}"
        else:
            msg += f" Was expecting one of the following: {expected_types}"
        super().__init__(msg)
