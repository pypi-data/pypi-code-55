from typing import Union, List, Dict

from sardine.exceptions.lang.parser.unexpected_token_found import UnexpectedTokenFound
from sardine.lang.mappings import DEFAULT_REPOSITORY_ALIAS
from sardine.lang.parser.objects import RepositoryDeclaration, StackDeclaration
from sardine.lang.tokenizer.objects import Token
import sardine.lang.tokenizer.tokens as ttypes


class Parser:

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens

    def parse(self) -> Dict[str, List[Union[RepositoryDeclaration, StackDeclaration]]]:
        declarations: Dict[str, List[Union[RepositoryDeclaration, StackDeclaration]]] = {'repositories': [],
                                                                                         'stacks': []}
        while self.tokens:
            declaration = self._parse_declaration()
            if isinstance(declaration, RepositoryDeclaration):
                declarations['repositories'].append(declaration)
            else:
                declarations['stacks'].append(declaration)
        return declarations

    def _parse_declaration(self) -> Union[RepositoryDeclaration, StackDeclaration]:
        if self.peek(ttypes.USE_TOKEN):
            return self._parse_repository_declaration()
        return self._parse_stack_declaration()

    def _parse_repository_declaration(self) -> RepositoryDeclaration:
        self.consume(ttypes.USE_TOKEN)
        name = self.consume(ttypes.REPOSITORY_NAME_TOKEN).value
        alias = DEFAULT_REPOSITORY_ALIAS
        if self.peek(ttypes.AS_TOKEN):
            self.consume(ttypes.AS_TOKEN)
            alias = self.consume(ttypes.ALIAS_TOKEN).value
        return RepositoryDeclaration(name, alias)

    def _parse_stack_declaration(self) -> StackDeclaration:
        self.consume(ttypes.LOAD_TOKEN)
        name = self.consume(ttypes.STACK_NAME_TOKEN).value
        aliased_repository = True
        if self.peek(ttypes.FROM_TOKEN):
            self.consume(ttypes.FROM_TOKEN)
            repository = self.consume([ttypes.ALIAS_TOKEN, ttypes.REPOSITORY_NAME_TOKEN])
            if repository.type == ttypes.REPOSITORY_NAME_TOKEN:
                aliased_repository = False
            repository_value = repository.value
        else:
            repository_value = DEFAULT_REPOSITORY_ALIAS

        if self.peek(ttypes.AS_TOKEN):
            self.consume(ttypes.AS_TOKEN)
            alias = self.consume(ttypes.ALIAS_TOKEN).value
        else:
            alias = name

        return StackDeclaration(name, repository_value, alias, aliased_repository)

    def consume(self, expected_type: Union[str, List[str]]) -> Token:
        token = self.tokens.pop(0)
        if self._check_type(expected_type, token):
            return token
        else:
            raise UnexpectedTokenFound(token.type, expected_type)

    def peek(self, expected_type: Union[str, list]) -> bool:
        return bool(self.tokens and self._check_type(expected_type, self.tokens[0]))

    @staticmethod
    def _check_type(expected_type: Union[str, list], token) -> bool:
        expected_type = [expected_type] if type(expected_type) is str else expected_type
        return token.type in expected_type
