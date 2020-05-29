import sys
if sys.platform == 'skulpt':
    class Predicate(object):
        def __init__(self, fn):
            self.fn = fn

        def __call__(self, *args, **kwargs):
            return self.fn(*args, **kwargs)

        def __and__(self, other):
            return AndPredicate(self, other)

        def __rand__(self, other):
            return AndPredicate(other, self)

        def __or__(self, other):
            return OrPredicate(self, other)

        def __ror__(self, other):
            return OrPredicate(other, self)

        def __invert__(self):
            return InvertedPredicate(self)

        def after(self, transform):
            return PostPredicate(self, transform)
else:
    from functools import update_wrapper
    from typing import Callable

    class Predicate(Callable):
        def __init__(self, fn):
            self.fn = fn
            update_wrapper(self, fn)

        def __call__(self, *args, **kwargs):
            return self.fn(*args, **kwargs)

        def __and__(self, other):
            return AndPredicate(self, other)

        def __rand__(self, other):
            return AndPredicate(other, self)

        def __or__(self, other):
            return OrPredicate(self, other)

        def __ror__(self, other):
            return OrPredicate(other, self)

        def __invert__(self):
            return InvertedPredicate(self)

        def after(self, transform):
            return PostPredicate(self, transform)


class ComposedPredicate(Predicate):
    def __init__(self, fn, left, right):
        super().__init__(fn)
        self.left = left
        self.right = right


class TransformedPredicate(Predicate):
    def __init__(self, fn, prev):
        super().__init__(fn)
        self.prev = prev


class AndPredicate(ComposedPredicate):
    def __init__(self, left, right):
        def composed(*args, **kwargs):
            return left(*args, **kwargs) and right(*args, **kwargs)

        super().__init__(composed, left, right)


class OrPredicate(ComposedPredicate):
    def __init__(self, left, right):
        def composed(*args, **kwargs):
            return left(*args, **kwargs) or right(*args, **kwargs)

        super().__init__(composed, left, right)


class InvertedPredicate(TransformedPredicate):
    def __init__(self, prev):
        def transformed(*args, **kwargs):
            return not prev(*args, **kwargs)

        super().__init__(transformed, prev)


class PostPredicate(TransformedPredicate):
    def __init__(self, prev, transform):
        def transformed(*args, **kwargs):
            return prev(transform(*args, **kwargs))

        super().__init__(transformed, prev)
