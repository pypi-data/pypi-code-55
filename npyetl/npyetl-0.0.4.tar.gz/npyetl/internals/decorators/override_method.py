from typing import(
    Callable
)

def override(interfaceClass: type):
    def overrider(method: Callable):
        try:
            assert(method.__name__ in dir(interfaceClass))
        except AttributeError:
            pass
        return method
    return overrider