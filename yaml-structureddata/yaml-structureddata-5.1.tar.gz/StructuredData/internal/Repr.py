"""Functions to print like repr(x), bit sorted.
"""

import builtins
import functools

__version__="5.1" #VERSION#

NL="\n" # newline char

# pylint: disable=invalid-name

# ---------------------------------------------------------
# doctest utilities

@functools.total_ordering
class GenericItem:
    """a generic data item.
    This may contain the data of any scalar,
    list, tuple or dictionary.
    """
    # pylint: disable=too-few-public-methods
    SORT_NONE         =  0
    SORT_BOOL         =  1
    SORT_INT          =  2
    SORT_FLOAT        =  3
    SORT_COMPLEX      =  4
    SORT_BYTES        =  5
    SORT_BYTEARRAY    =  6
    SORT_STR          =  7
    SORT_TUPLE        =  8
    SORT_LIST         =  9
    SORT_SET          = 10
    SORT_DICT         = 11
    SORT_UNKNOWN      = 12
    TAGS=("SORT_NONE", "SORT_BOOL", "SORT_INT", "SORT_FLOAT", "SORT_COMPLEX",
          "SORT_BYTES", "SORT_BYTEARRAY", "SORT_STR", "SORT_TUPLE",
          "SORT_LIST", "SORT_SET", "SORT_DICT",
          "SORT_UNKNOWN")
    def dump_lst(self, lst, seen= None):
        """dump the internal data."""
        if id(self) in seen:
            lst.append("...")
            return
        seen.add(id(self))
        st= self.__class__.TAGS[self.type]
        lst.append("%s(" % st)
        self.var.dump_lst(lst, seen)
        lst.append(")")
    def dump(self):
        """dump the internal data."""
        lst= []
        seen= set()
        self.dump_lst(lst, seen)
        print("".join(lst))
    def __repr__(self):
        """dump the internal data."""
        st= self.__class__.TAGS[self.type]
        return builtins.repr((st, builtins.repr(self.var)))
    def __init__(self, var, seen= None):
        """initialize from a given variable."""
        # pylint: disable=too-many-return-statements, too-many-branches
        # pylint: disable=too-many-statements
        cls= self.__class__
        if seen is None:
            seen= set()
        self.recursive= False
        self.var= var
        if var is None:
            self.type= cls.SORT_NONE
            return
        if isinstance(var, bool):
            self.type= cls.SORT_BOOL
            return
        if isinstance(var, int):
            self.type= cls.SORT_INT
            return
        if isinstance(var, float):
            self.type= cls.SORT_FLOAT
            return
        if isinstance(var, complex):
            self.type= cls.SORT_COMPLEX
            return
        if isinstance(var, bytes):
            self.type= cls.SORT_BYTES
            return
        if isinstance(var, bytearray):
            self.type= cls.SORT_BYTEARRAY
            return
        if isinstance(var, str):
            self.type= cls.SORT_STR
            return
        if isinstance(var, tuple):
            self.type= cls.SORT_TUPLE
            if id(var) in seen:
                self.recursive= True
                self.var= id(var) # for better sorting
                return
            seen.add(id(var))
            self.var= tuple(cls(v, seen) for v in var)
            return
        if isinstance(var, list):
            self.type= cls.SORT_LIST
            if id(var) in seen:
                self.recursive= True
                self.var= id(var) # for better sorting
                return
            seen.add(id(var))
            self.var= tuple(cls(v, seen) for v in var)
            return
        if isinstance(var, set):
            self.type= cls.SORT_SET
            if id(var) in seen:
                self.recursive= True
                self.var= id(var) # for better sorting
                return
            seen.add(id(var))
            # do also sort:
            self.var= tuple(sorted([cls(v, seen) for v in var]))
            return
        if isinstance(var, dict):
            self.type= cls.SORT_DICT
            if id(var) in seen:
                self.recursive= True
                self.var= id(var) # for better sorting
                return
            seen.add(id(var))
            # do also sort:
            d= { cls(k, seen): cls(v, seen) for k,v in var.items() }
            self.var= tuple( (k, d[k]) for k in sorted(d.keys()) )
            return
        self.type= cls.SORT_UNKNOWN
        self.var= var
    def __eq__(self, other):
        """test for equality.

        total_ordering will implement the missing comparison methods.
        """
        if not isinstance(other, self.__class__):
            raise TypeError("wrong type: %s" % builtins.repr(other))
        if self.type != other.type:
            return False
        return self.var==other.var
    def __lt__(self, other):
        """test for less-than.

        total_ordering will implement the missing comparison methods.
        """
        if not isinstance(other, self.__class__):
            raise TypeError("wrong type: %s" % builtins.repr(other))
        if self.type < other.type:
            return True
        if self.type > other.type:
            return False
        return self.var < other.var
    def _repr_string_lst(self, lst):
        """return a nice, repr() like string."""
        # pylint: disable=too-many-branches
        cls= self.__class__
        if self.type in (cls.SORT_TUPLE, \
                         cls.SORT_LIST, cls.SORT_SET):
            if self.type== cls.SORT_TUPLE:
                brackets= ('(', ')')
            elif self.type== cls.SORT_LIST:
                brackets= ('[', ']')
            elif self.type== cls.SORT_SET:
                brackets= ('{', '}')
            else:
                raise AssertionError
            if self.recursive:
                # recursive data structure, do not only print a short string:
                lst.append("%s...%s" % brackets)
                return
            first= True
            length=0
            lst.append(brackets[0])
            for elm in self.var:
                length+= 1
                if not first:
                    lst.append(", ")
                else:
                    first= False
                # pylint: disable= protected-access
                elm._repr_string_lst(lst)
            if self.type==cls.SORT_TUPLE and length==1:
                # append comma like in "(a,)":
                lst.append(",")
            lst.append(brackets[1])
            return
        if self.type== cls.SORT_DICT:
            if self.recursive:
                # recursive data structure, do not only print a short string:
                lst.append("{...}")
                return
            first= True
            lst.append('{')
            for elm in self.var:
                if not first:
                    lst.append(", ")
                else:
                    first= False
                # pylint: disable= protected-access
                elm[0]._repr_string_lst(lst)
                lst.append(": ")
                elm[1]._repr_string_lst(lst)
            lst.append('}')
            return
        lst.append(builtins.repr(self.var))
    @staticmethod
    def _repr_nice_lst(lst, maxcol=70):
        """format a repr list in a nice way."""
        col= 0
        indent= 0
        new= []
        stack= []
        force_newline= False
        for elm in lst:
            if elm in ('(','[','{'):
                if force_newline:
                    new.append(NL)
                    new.append(" " * indent)
                    col= indent
                    force_newline= False
                stack.append(indent)
                indent= col+2
                new.append(elm)
                new.append(NL)
                new.append(" " * indent)
                col= indent
                continue
            if elm in (')',']','}'):
                new.append(NL)
                new.append(" " * (indent-2))
                new.append(elm)
                col= indent-1
                indent= stack.pop()
                force_newline= True
                continue
            if elm==', ':
                if (col > maxcol) or force_newline:
                    new.append(',')
                    new.append(NL)
                    new.append(" " * indent)
                    col= indent
                    force_newline= False
                else:
                    new.append(elm)
                    col+= len(elm)
                continue
            if elm==': ':
                if force_newline:
                    new.append(NL)
                    new.append(" " * indent)
                    col= indent
                    force_newline= False
                new.append(elm)
                col+= len(elm)
                continue
            new.append(elm)
            col+= len(elm)
        return new
    def __hash__(self):
        """return a hash key, needed when GenericItem are used as dict keys."""
        return hash((self.type, self.var))
    def repr(self):
        """return a nice, repr() like string."""
        l= []
        self._repr_string_lst(l)
        return "".join(l)
    def nice(self, maxcol=70):
        """return a nice, repr() like string."""
        l= []
        self._repr_string_lst(l)
        # pylint: disable= protected-access
        return "".join(self.__class__._repr_nice_lst(l, maxcol))
    def print(self):
        """return a nice, repr() like string.

        Here are some examples:
        >>> GenericItem(None).print()
        None
        >>> GenericItem(True).print()
        True
        >>> GenericItem(1).print()
        1
        >>> GenericItem(1.1).print()
        1.1
        >>> GenericItem(1+2j).print()
        (1+2j)
        >>> GenericItem(b'AB').print()
        b'AB'
        >>> GenericItem(bytearray(b'AB')).print()
        bytearray(b'AB')
        >>> GenericItem("abc").print()
        'abc'
        >>> GenericItem((1,"a",True)).print()
        (1, 'a', True)
        >>> GenericItem([1,"a",True]).print()
        [1, 'a', True]
        >>> GenericItem(set((True,))).print()
        {True}
        >>> GenericItem(set((True,1.2,"A",False,"X"))).print()
        {False, True, 1.2, 'A', 'X'}
        >>> GenericItem({"A":1}).print()
        {'A': 1}
        >>> GenericItem({"A":1, 2:1, True:11}).print()
        {True: 11, 2: 1, 'A': 1}
        """
        print(self.repr())
    def nprint(self, maxcol= 70):
        """return a nice, repr() like string.

        Here are some examples:
        >>> GenericItem({"A":1, "B": [1,2,3], "C": {"x":1, "y":2.0, "z": {True,False}}}).nprint()
        {
          'A': 1, 'B': [
                         1, 2, 3
                       ],
          'C': {
                 'x': 1, 'y': 2.0, 'z': {
                                          False, True
                                        }
               }
        }
        >>> GenericItem({"A":1, "B": [1,2,3], "C": {"x":1, "y":2.0, "a": {True,False}}}).nprint()
        {
          'A': 1, 'B': [
                         1, 2, 3
                       ],
          'C': {
                 'a': {
                        False, True
                      },
                 'x': 1, 'y': 2.0
               }
        }
        >>> GenericItem({"D":1, "B": [1,2,3], "C": {"x":1, "y":2.0, "a": {True,False}}}).nprint()
        {
          'B': [
                 1, 2, 3
               ],
          'C': {
                 'a': {
                        False, True
                      },
                 'x': 1, 'y': 2.0
               },
          'D': 1
        }
        """
        print(self.nice(maxcol))

# pylint: disable= redefined-builtin
def repr(var):
    """return any var in an ordered way."""
    return GenericItem(var).repr()

def nice(var, maxcol= 70):
    """return any var in an ordered way as a multi-line string."""
    return GenericItem(var).nice(maxcol)

def printrepr(var):
    """print a repr string."""
    return GenericItem(var).print()

def printnice(var, maxcol= 70):
    """print a multi-line repr string."""
    return GenericItem(var).nprint(maxcol)
