# only for skulpt
class ArgumentsChecker:
    def __init__(self, predicates):
        self.predicates = predicates

    def __call__(self, fn):
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)
        return wrapper
