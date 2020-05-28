"""implement an enumeration class.
"""

__version__="5.1" #VERSION#

# pylint: disable=invalid-name

def NewEnum(global_dict, name_, list_):
    """create a enumeration class from a given list of elements.

    Note that you should *always* select for the "name_" parameter the same
    name as the identifier the created class is assigned to.  The returned
    object is a class object, it is not meant and does not need to be
    instantiated.
    Here are some examples:

    >>> NewEnum(globals(), "C", ["x","y","z"])
    >>> C.x
    C.x
    >>> repr(C.x)
    'C.x'
    >>> str(C.x)
    'x'
    >>> a=C.x
    >>> a==C.y
    False
    >>> a==C.x
    True
    >>> a==C.a
    Traceback (most recent call last):
        ...
    AttributeError: type object 'C' has no attribute 'a'
    >>> C.fromstring("y")
    C.y
    >>> C.fromstring("y")==C.y
    True
    >>> C.x=1
    Traceback (most recent call last):
        ...
    AssertionError: class C is immutable
    >>> type(C)
    <class '__main__.CMeta'>
    >>> type(C.x)
    <class '__main__.CValue'>
    >>> x=CValue("x")
    >>> x==C.x
    True
    >>> x=CValue("a")
    Traceback (most recent call last):
        ...
    ValueError: unknown attribute: a
    >>> for s in C:
    ...   print(s)
    ...
    x
    y
    z
    """
    valname_= "%sValue" % name_
    metaname_= "%sMeta" % name_
    class MyEnumVal():
        """Implement enumeration value.

        Since this class is not returned to the enclosing scope, the user
        cannot instantiate an object of this class directly. However, the
        method "fromstring" of class MyEnum enables the user to do so, if he
        wants. The only purpose of this class is that for each possible
        enumeration value it is instantiated once and this object is stored as
        a class attribute in the MyEnum class.
        """
        _known = dict(zip(list_,list(range(len(list_)))))
        _rknown= dict(zip(list(range(len(list_))),list_))
        def __init__(self, name):
            if name not in MyEnumVal._known:
                raise ValueError("unknown attribute: %s" % name)
            self._val= MyEnumVal._known[name]
        def __hash__(self):
            return id(self._val)
        # pylint: disable= protected-access
        def __lt__(self, other):
            if not isinstance(other, MyEnumVal):
                raise TypeError("error, other must be of type %s" % valname_)
            return self._val <  other._val
        def __le__(self, other):
            if not isinstance(other, MyEnumVal):
                raise TypeError("error, other must be of type %s" % valname_)
            return self._val <= other._val
        def __eq__(self, other):
            if not isinstance(other, MyEnumVal):
                raise TypeError("error, other must be of type %s" % valname_)
            return self._val == other._val
        def __ne__(self, other):
            if not isinstance(other, MyEnumVal):
                raise TypeError("error, other must be of type %s" % valname_)
            return self._val != other._val
        def __gt__(self, other):
            if not isinstance(other, MyEnumVal):
                raise TypeError("error, other must be of type %s" % valname_)
            return self._val >  other._val
        def __ge__(self, other):
            if not isinstance(other, MyEnumVal):
                raise TypeError("error, other must be of type %s" % valname_)
            return self._val >= other._val
        # pylint: enable= protected-access
        def index(self):
            """return the value of the internal index."""
            return self._val
        def __repr__(self):
            return "%s.%s" % (name_, MyEnumVal._rknown[self._val])
        def __str__(self):
            return "%s" % MyEnumVal._rknown[self._val]
    # Set the name of the MyEnumVal class:
    MyEnumVal.__name__= valname_
    MyEnumVal.__qualname__= valname_
    class MyMeta(type):
        """This class controls the instantiation of the MyEnum class object.

        It has two purposes:

        - initialize the attributes of the MyEnum class object with instances
          of MyEnumVal objects.
        - forbid changing attributes of the MyEnum class object.
        """
        def __new__(mcs, _, bases, dictionary):
            for v in list_:
                dictionary[v]= MyEnumVal(v)
            return type.__new__(mcs, name_, bases, dictionary)
        def __setattr__(cls, name, value):
            raise AssertionError("class %s is immutable" % name_)
        def __iter__(cls):
            for s in list_:
                yield getattr(cls, s)
    # The class object MyEnum is actually an instance of the type MyMeta
    # so we give MyMeta a nice name here:
    MyMeta.__name__= metaname_
    MyMeta.__qualname__= metaname_
    class MyEnum(metaclass=MyMeta):
        """implement a enumeration type.

        Note that this class is not meant to be instantiated. It is only
        here to be returned as a class object.

        It has an attribute for each value of the enumeration of the type
        MyEnumVal.
        """
        # pylint: disable=too-few-public-methods
        def __init__(self,*args,**kwargs):
            """this class is not meant to instantiate objects."""
            raise NotImplementedError
        @classmethod
        def fromstring(cls, st):
            """Create a new MyEnumVal object from a given string.

            Here is an example:
            >>> C= EnumClass("C",["x","y","z"])
            >>> C.fromstring("y")
            C.y
            >>> C.fromstring("a")
            Traceback (most recent call last):
                ...
            ValueError: unknown attribute: a
            """
            return MyEnumVal(st)
    global_dict[name_]= MyEnum
    global_dict[metaname_]= MyMeta
    global_dict[valname_]= MyEnumVal

def _test():
    # pylint: disable= import-outside-toplevel
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
