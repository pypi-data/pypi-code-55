class RepositoryDeclaration:
    __slots__ = ('name', 'alias')

    def __init__(self, name: str, alias: str):
        self.name = name
        self.alias = alias

    def __repr__(self):
        return f"<Repository {self.alias} ('{self.name}')>"


class StackDeclaration:
    __slots__ = ('name', 'repository_name', 'alias', 'aliased_repository')

    def __init__(self, stack_name: str, repository_name: str, alias: str, aliased_repository: bool):
        self.name = stack_name
        self.repository_name = repository_name
        self.alias = alias
        self.aliased_repository = aliased_repository

    def __repr__(self):
        return f"<Stack {self.alias} ('{self.repository_name}/{self.name}')"
