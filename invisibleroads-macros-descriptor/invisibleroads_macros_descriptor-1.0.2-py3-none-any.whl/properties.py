class ClassProperty(object):

    def __init__(self, f):
        self.f = classmethod(f)

    def __get__(self, obj, Class):
        return self.f.__get__(None, Class)()


class CachedProperty(object):

    # Note that functools.cached_property is defined in Python 3.8.6+

    def __init__(self, f):
        self.f = f

    def __get__(self, obj, Class):
        if obj is None:
            return self
        value = obj.__dict__[self.f.__name__] = self.f(obj)
        return value


classproperty = class_property = ClassProperty
cachedproperty = cached_property = CachedProperty
