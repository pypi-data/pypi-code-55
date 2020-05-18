from node import Node


def node_decorator(*args, **kwargs):
    def wrapper(cls):
        class NewCls(cls):
            def __init__(self):
                self.cls = cls

            def __getattribute__(self, s):
                if s in kwargs:
                    return kwargs[s]

                return super().__getattribute__(s)

        return NewCls
    return wrapper
