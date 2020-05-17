from typing import Union, List, Dict

from sardine.exceptions.lang.manifest.cannot_redefine_alias import CannotRedefineAlias
from sardine.exceptions.lang.manifest.repository_alias_not_found import RepositoryAliasNotFound
from sardine.lang.parser.objects import RepositoryDeclaration, StackDeclaration
from sardine.types import STACK_DECLARATIONS_TYPE


class StackManifestBuilder:

    @classmethod
    def build(cls, declarations: Dict[str, List[Union[RepositoryDeclaration,
                                                      StackDeclaration]]]) -> STACK_DECLARATIONS_TYPE:
        repository_naming_mapping = cls.build_repository_naming_mapping(declarations['repositories'])  # type: ignore
        resolved_stack_declarations = cls.resolve_aliases(declarations['stacks'],
                                                          repository_naming_mapping)  # type: ignore
        return {declaration.alias: declaration for declaration in resolved_stack_declarations}

    @classmethod
    def resolve_aliases(cls, stack_declarations: List[StackDeclaration],
                        repository_naming_mappings: Dict[str, str]) -> List[StackDeclaration]:
        for declaration in stack_declarations:
            if declaration.aliased_repository:
                if declaration.repository_name not in repository_naming_mappings:
                    raise RepositoryAliasNotFound(declaration.repository_name)
                declaration.repository_name = repository_naming_mappings[declaration.repository_name]
        return stack_declarations

    @classmethod
    def build_repository_naming_mapping(cls, repository_declarations: List[RepositoryDeclaration]) -> Dict[str, str]:
        naming_mapping = {}
        for declaration in repository_declarations:
            name, alias = declaration.name, declaration.alias
            if alias in naming_mapping:
                raise CannotRedefineAlias(alias)
            naming_mapping[alias] = name
            naming_mapping[name] = name
        return naming_mapping
