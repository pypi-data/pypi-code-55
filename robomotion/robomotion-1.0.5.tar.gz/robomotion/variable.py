class Variable:
    def __init__(self, scope: str='', name: str='', title: str='', type: str='', csScope: bool=False, customScope: bool=False, jsScope: bool=False, messageScope: bool=False):
        self.__scope = scope
        self.__name = name
        self.__title = title
        self.__type = type
        self.__csScope = csScope
        self.__customScope = customScope
        self.__jsScope = jsScope
        self.__messageScope = messageScope

    @property
    def scope(self) -> str:
        return self.__scope

    @property
    def name(self) -> str:
        return self.__name

    @property
    def title(self) -> str:
        return self.__title

    @property
    def type(self) -> str:
        return self.__type

    @property
    def csScope(self) -> str:
        return self.__csScope

    @property
    def customScope(self) -> str:
        return self.__customScope

    @property
    def jsScope(self) -> str:
        return self.__jsScope

    @property
    def messageScope(self) -> str:
        return self.__messageScope


class Credentials:
    def __init__(self, vaultId: str='', itemId: str='', title: str='', category: int=0):
        self.__vaultId = vaultId
        self.__itemId = itemId
        self.__title = title
        self.__category = category

    @property
    def vaultId(self) -> str:
        return self.__vaultId

    @property
    def itemId(self) -> str:
        return self.__itemId

    @property
    def title(self) -> str:
        return self.__title

    @property
    def category(self) -> int:
        return self.__category


class Enum:
    def __init__(self, enum: [], enumNames: [], type: str, value: str):
        self.__enum = enum
        self.__enumNames = enumNames
        self.__type = type
        self.__value = value

    @property
    def enum(self):
        return self.__enum

    @property
    def enumNames(self):
        return self.__enumNames

    @property
    def type(self):
        return self.__type

    @property
    def value(self):
        return self.__value


class String:
    def __init__(self):
        self.__value = ''
        self.__title = ''

    def __repr__(self) -> str:
        return self.__value

    @property
    def title(self) -> str:
        return self.__title


class Integer:
    def __init__(self):
        self.__value = 0
        self.__title = ''

    def __repr__(self) -> int:
        return self.__value

    @property
    def title(self) -> str:
        return self.__title


class Boolean:
    def __init__(self):
        self.__value = False
        self.__title = ''

    def __repr__(self) -> int:
        return self.__value

    @property
    def title(self) -> str:
        return self.__title
