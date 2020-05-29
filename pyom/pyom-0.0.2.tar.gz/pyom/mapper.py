from .gateway import Row


class Mapper:
    def __call__(self, params: Row) -> Row:
        return params
