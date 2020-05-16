import random
import uuid


def _string():
    return uuid.uuid4().hex


def _int():
    return random.randint(0, 100000)


class Fixture:
    factories = {
        str: _string,
        int: _int
    }

    def __init__(self):
        pass

    def create(self, cls):
        factory = self.factories.get(cls)
        if factory:
            return factory()
        raise ValueError('Unsupported type %s' % cls)
