import random
import uuid


def _string():
    return uuid.uuid4().hex


def _int():
    return random.randint(0, 100000)


def _email():
    return '%s@%s.com' % (_string(), _string())


class Email:
    def __init__(self):
        pass


class Fixture:
    factories = {
        str: _string,
        int: _int,
        Email: _email,
    }

    def __call__(self, cls):
        return self.create(cls)

    def __init__(self):
        pass

    def create(self, cls):
        factory = self.factories.get(cls)
        if factory:
            return factory()
        raise ValueError('Unsupported type %s' % cls)
