class Token:
    __slots__ = ('type', 'value')

    def __init__(self, type: str, value: str):
        self.type = type
        self.value = value

    def __repr__(self) -> str:
        return f"<Token type={self.type}, value={self.value} >"
