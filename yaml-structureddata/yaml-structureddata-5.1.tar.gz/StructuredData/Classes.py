"""StructuredData - a package to manage StructuredData.
"""
# pylint: disable=too-many-lines, invalid-name, too-many-arguments

import os
import re
import pickle
import pprint
import copy

import csv
import io


from StructuredData.internal import enumclass
from StructuredData.internal import dictutils
from StructuredData.internal import myyaml
from StructuredData.internal import lock
from StructuredData.internal import Repr

__version__="5.1" #VERSION#

assert __version__==enumclass.__version__
assert __version__==dictutils.__version__
assert __version__==myyaml.__version__
assert __version__==lock.__version__
assert __version__==Repr.__version__

use_lockfile= True

# ---------------------------------------------------------
# constants

FILE_LOCK_TIMEOUT= 30

# ---------------------------------------------------------
# list utilities

def is_iterable(var):
    """return if var is a *real* iterable, not a string."""
    if isinstance(var, str):
        return False
    return hasattr(var, "__iter__")

# ---------------------------------------------------------
# string utilities
def andmatch(st, words):
    """returns True if st contains all the words in any order.

    The comparison is case insensitive.
    Here are some examples:
    >>> st="this is the string that contains some words"
    >>> andmatch(st,["this"])
    True
    >>> andmatch(st,["that","this"])
    True
    >>> andmatch(st,["that","this","there"])
    False
    >>> andmatch(st,["THIS", "There"])
    False
    >>> andmatch(st,["THIS", "That"])
    True
    >>> andmatch(st,["THIS", "That", "contains"])
    True
    """
    st= st.upper()
    for w in words:
        w= w.upper()
        if st.find(w)== -1:
            return False
    return True

def imatch(st, pattern):
    """returns True if st contains all the words from pattern in any order.
    The comparison is case insensitive.

    Here are some examples:
    >>> st="this is the string that contains some words"
    >>> imatch(st, "this")
    True
    >>> imatch(st, "that this")
    True
    >>> imatch(st, "this that there")
    False
    >>> imatch(st, "THIS There")
    False
    >>> imatch(st, "THIS That")
    True
    >>> imatch(st, "THIS That contains")
    True
    """
    return andmatch(st, pattern.split())
# ---------------------------------------------------------
# file utilities

def _cache_filename(filename):
    """return the name of a pickle file.
    """
    return "%s.pic" % filename

def _pickle_write(stream, data):
    """write something pickled.
    """
    pickle.dump(data, stream, pickle.HIGHEST_PROTOCOL)

def _find_cache_file(filename):
    """try to find the cache file.
    """
    if not os.path.exists(filename):
        raise IOError("file %s doesn't exist" % filename)
    cache= _cache_filename(filename)
    if not os.path.exists(cache):
        return (cache, "missing")
    if os.path.getmtime(cache)< os.path.getmtime(filename):
        return (cache, "older")
    return (cache, "newer")

def _write_cache_file(filename, data):
    """try to write pickle data.
    """
    cache= _cache_filename(filename)
    try:
        f= open(cache, "wb")
    except IOError: # cannot write
        return False
    _pickle_write(f, data)
    f.close()
    return True

def _read_cached(filename, direct_read_func):
    """read, optionally from a cache file.

    """
    (cache, state)= _find_cache_file(filename)
    if state!="newer":
        data= direct_read_func(filename)
        _write_cache_file(filename, data)
    else:
        stream= open(cache, 'rb')
        data= pickle.load(stream)
        stream.close()
    return data

# ---------------------------------------------------------
# escaping

_re_escaped_wc= re.compile(r'\\+(\*|\*\*|#)$')

def escape_in_stringkey(st):
    r"""escape special characters with a backslash.

    replace '.' with '\.' and '[number]' with '\[number\]'
    This is needed in order to convert path which contains
    the characters '.' or '[' or ']' to a keylist.
    (see class StructuredDataStore).

    Here are some examples:

    >>> print(escape_in_stringkey("AB"))
    AB
    >>> print(escape_in_stringkey("A.B"))
    A\.B
    >>> print(escape_in_stringkey("A.B[5]C"))
    A\.B\[5\]C
    >>> print(escape_in_stringkey("*"))
    \*
    >>> print(escape_in_stringkey("**"))
    \**
    >>> print(escape_in_stringkey("#"))
    \#
    >>> print(escape_in_stringkey("A#"))
    A#
    >>> print(escape_in_stringkey("A*"))
    A*
    >>> print(escape_in_stringkey(r"\*"))
    \\*
    >>> print(escape_in_stringkey(r"\\*"))
    \\\*
    >>> print(escape_in_stringkey(r"\**"))
    \\**
    >>> print(escape_in_stringkey(r"\#"))
    \\#
    >>> print(escape_in_stringkey(r"\\#"))
    \\\#
    """
    if st=="*" : # related to class SpecialKey
        return r"\*"
    if st=="**": # related to class SpecialKey
        return r"\**"
    if st=="#" : # related to class SpecialKey
        return r"\#"
    if st.startswith("\\"): # starts already with a backslash
        if _re_escaped_wc.match(st) is not None:
            return "\\" + st
    st= st.replace(".", r"\.")
    st= st.replace("[", r"\[")
    st= st.replace("]", r"\]")
    return st

def unescape_in_stringkey(st):
    r"""unescape special characters.

    replace '\.' with '.' and '\[number\]' with '[number]'
    This is needed in order to convert keylist to a path which
    contains the characters '.' or '[' or ']'.
    (see class StructuredDataStore).

    Here are some examples:

    >>> print(unescape_in_stringkey("AB"))
    AB
    >>> print(unescape_in_stringkey("A\.B\[2\]C"))
    A.B[2]C
    >>> print(unescape_in_stringkey("\*"))
    *
    >>> print(unescape_in_stringkey("\**"))
    **
    >>> print(unescape_in_stringkey("\#"))
    #
    >>> print(unescape_in_stringkey("\*A"))
    \*A
    >>> print(unescape_in_stringkey("\#A"))
    \#A
    >>> print(unescape_in_stringkey(r"\\*"))
    \*
    >>> print(unescape_in_stringkey(r"\\**"))
    \**
    >>> print(unescape_in_stringkey(r"\\#"))
    \#
    """
    if st== r"\*" : # related to class SpecialKey
        return "*"
    if st== r"\**": # related to class SpecialKey
        return "**"
    if st== r"\#" : # related to class SpecialKey
        return "#"
    if st.startswith("\\"): # starts already with a backslash
        if _re_escaped_wc.match(st) is not None:
            return st[1:]
    st= st.replace(r"\.",".")
    st= st.replace(r"\[","[")
    st= st.replace(r"\]","]")
    return st

# ---------------------------------------------------------
# SpecialKey

# "root" "#"      : root symbol needed for typepaths
# "any_key" "*"   : matches any key in a path, the key must exist
# "any_keys" "**" : matches any number of keys in a path, there must
#                   be at least one key present

# activate the following for the pylint checker:
## @@@
#SpecialKeyTypesValue= 1
#class SpecialKeyTypes():
#    """dummy class, only here for pylint."""
#    # pylint: disable= too-few-public-methods
#    root=1
#    any_key= 1
#    any_keys=1
#    def __init__(self):
#        pass
#
#class SDTypes():
#    """dummy class, only here for pylint."""
#    # pylint: disable= too-few-public-methods
#    boolean= 1
#    integer= 1
#    real= 1
#    string= 1
#    optional_struct= 1
#    open_struct= 1
#    struct= 1
#    list= 1
#    typed_map= 1
#    optional_list= 1
#    typed_list= 1
#    map= 1
#    def __init__(self):
#        pass
#
#def SDTypesValue(_):
#    # pylint: disable= missing-docstring
#    return SDTypes()
#
## @@@

enumclass.NewEnum(globals(), "SpecialKeyTypes",
                  [ "root", "any_key", "any_keys" ]
                 )

class SpecialKey():
    """
    This class implements a data type for special path elements. Currently
    there are three kinds implemented, the "any_key" type which matches any key
    (exactly one key), "any_keys" which matches any key (one or more) and the
    "root" which is used to represent the root of a StructuredDataStore. Note
    that in order to make objects of this class usable for being dictionary
    keys, instances for each type of this class are instantiated, ANYKEY,
    ANYKEYS and ROOTKEY. You should only use these and not instantiate
    SpecialKey objects of your own. Use the function string_to_keyobject to
    create a SpecialKey object from a string, this function uses the predefined
    objects, too.
    """
    # a number of backslashes followed by a single star
    def __init__(self, type_):
        r"""initialize the SpecialKey from a given type and data

        This creates a SpecialKey object from a given type\_ and an arbitrary
        data object. The type\_ parameter must be of the type
        SpecialKeyTypesValue.  Currently there are only three possible values
        for this parameter, SpecialKeyTypes.any_key, SpecialKeyTypes.any_keys
        and SpecialKeyTypes.root.

        Here are some examples:

        >>> w= SpecialKey(SpecialKeyTypes.any_key)
        >>> repr(w)
        'SpecialKey(SpecialKeyTypes.any_key)'
        >>> str(w)
        '*'
        """
        if not isinstance(type_, SpecialKeyTypesValue):
            raise TypeError("type_ must be a SpecialKeyTypesValue")
        self._type= type_
    def __hash__(self):
        """return hash key."""
        return id(self._type)
    def is_root(self):
        """returns True if the object is of type "root"."""
        return self._type == SpecialKeyTypes.root
    def simple_wildcard(self):
        """returns True if the object is of type "any_key"."""
        return self._type == SpecialKeyTypes.any_key
    def recursive_wildcard(self):
        """returns True if the object is of type "any_keys"."""
        return self._type == SpecialKeyTypes.any_keys
    @staticmethod
    def is_recursive_wildcard(val):
        """test for recursive wildcard."""
        if not isinstance(val, SpecialKey):
            return False
        return val.recursive_wildcard()
    def __lt__(self, other):
        """returns True of self < other."""
        if not isinstance(other, SpecialKey):
            return False
        # pylint: disable= protected-access
        return self._type < other._type
    def __le__(self, other):
        """returns True of self <= other."""
        if not isinstance(other, SpecialKey):
            return False
        # pylint: disable= protected-access
        return self._type <=other._type
    def __eq__(self, other):
        """returns True of self == other."""
        if not isinstance(other, SpecialKey):
            return False
        # pylint: disable= protected-access
        return self._type ==other._type
    def __ne__(self, other):
        """returns True of self != other."""
        if not isinstance(other, SpecialKey):
            return True
        # pylint: disable= protected-access
        return self._type !=other._type
    def __gt__(self, other):
        """returns True of self > other."""
        if not isinstance(other, SpecialKey):
            return True
        # pylint: disable= protected-access
        return self._type > other._type
    def __ge__(self, other):
        """returns True of self >= other."""
        if not isinstance(other, SpecialKey):
            return True
        # pylint: disable= protected-access
        return self._type >=other._type
    def __repr__(self):
        """ returns a python expression for the object.
        """
        if self is ROOTKEY:
            return "ROOTKEY"
        if self is ANYKEY:
            return "ANYKEY"
        if self is ANYKEYS:
            return "ANYKEYS"
        return "SpecialKey(%s)" % repr(self._type)
    def __str__(self):
        """This returns the object in a human readable form."""
        # pylint: disable= no-else-return
        if self._type== SpecialKeyTypes.root:
            return "#"
        elif self._type== SpecialKeyTypes.any_key:
            return "*"
        elif self._type== SpecialKeyTypes.any_keys:
            return "**"
        else:
            raise AssertionError("unexpected value: %s" % repr(self._type))
    def match(self, val):
        """matches the wildcard against an item.

        This method checks if the SpecialKey matches a given string. It returns
        True if it does, False otherwise. It raises an exception if the
        SpecialKey object is not a wildcard.

        Here are some examples:

        >>> m= SpecialKey(SpecialKeyTypes.any_key)
        >>> m.match("ab")
        True
        >>> m.match("xy")
        True
        >>> m.match([1,2])
        False
        >>> m.match(ANYKEY)
        True
        >>> m.match(ANYKEYS)
        True
        >>> m.match(ROOTKEY)
        True
        """
        if self._type== SpecialKeyTypes.any_key:
            if isinstance(val, int):
                return True
            if isinstance(val, str):
                return True
            if isinstance(val, SpecialKey):
                return True
            return False
        raise AssertionError("unexpected internal type: %s" % repr(self._type))
    @staticmethod
    def keysubst(keylist, pattern_keylist):
        """change a keylist according to a pattern-keylist.

        Each wildcard in the pattern means that the corresponding key of the
        keylist remains unchanged. The non-wildcard parts in the pattern
        replace the corresponding key. If the pattern_keylist is shorter than
        the keylist, the remaining keys of the keylist are removed. If the
        pattern_keylist is longer than the keylist the remaining keys of the
        pattern_keylist are appended. However, these remaining keys MUST NOT be
        wildcards.

        Here are some examples:

        >>> def pathsubst(path, pattern):
        ...   l= SpecialKey.keysubst(StructuredDataStore.split_path(path),
        ...                          StructuredDataStore.split_path(pattern))
        ...   return StructuredDataStore.join_path(l)
        ...
        >>> pathsubst("a.b.c","*.*.x")
        'a.b.x'
        >>> pathsubst("a.b.c","*.y.*")
        'a.y.c'
        >>> pathsubst("a.b.c","*.*.*")
        'a.b.c'
        >>> pathsubst("a.b.c","*.*")
        'a.b'
        >>> pathsubst("a.b.c","*.*.*.x")
        'a.b.c.x'
        >>> pathsubst("a.b.c","*.*.*.*")
        Traceback (most recent call last):
            ...
        ValueError: keylist too short for patternlist
        >>> pathsubst("a.b.c","*[3].*")
        'a[3].c'
        >>> pathsubst("a.b.c","X.**")
        'X.b.c'
        >>> pathsubst("a.b.c","X.**.x.y")
        'X.b.c.x.y'
        >>> pathsubst("a.b.c","X.**.x.*")
        Traceback (most recent call last):
            ...
        ValueError: keylist too short for patternlist
        """
        # pylint: disable=too-many-branches
        src_l= len(keylist)
        pat_l= len(pattern_keylist)
        new= []
        src_idx= -1
        pat_idx= -1
        while True:
            src_idx+= 1
            if src_idx>=src_l:
                key= None
            else:
                key= keylist[src_idx]
            pat_idx+= 1
            if pat_idx>=pat_l:
                pat= None
            else:
                pat= pattern_keylist[pat_idx]
            if key is not None:
                if pat is None:
                    break # pattern is finished, stop everything
                if not isinstance(pat, SpecialKey):
                    new.append(pat)
                else:
                    if pat.simple_wildcard():
                        new.append(key)
                    elif pat.recursive_wildcard():
                        for i in range(src_idx, src_l):
                            new.append(keylist[i])
                        src_idx= src_l
                    else:
                        raise ValueError("unexpected patternkey '%s'" % \
                                          str(pat))
            elif pat is not None:
                if not isinstance(pat, SpecialKey):
                    new.append(pat)
                else:
                    raise ValueError("keylist too short for patternlist")
            else:
                break

        return new
    @staticmethod
    def list_match(pattern_list, keylist):
        """matches a pattern_list against a keylist.

        A pattern_list is a list of integers, strings and SpecialKey objects.
        A keylist is a list of integers and strings.

        Here are some examples:

        >>> def test(pattern,path):
        ...   pl= StructuredDataStore.split_path(pattern)
        ...   l = StructuredDataStore.split_path(path)
        ...   return SpecialKey.list_match(pl, l)
        ...
        >>> test("a.*","a.x")
        True
        >>> test("a.*","v.x")
        False
        >>> test("a.*.c","a[3].c")
        True
        >>> test("a.*.c","a[3].d")
        False
        >>> test("a.*.**","a[3].d")
        True
        >>> test("a.*.**","a[3].e")
        True
        >>> test("a.*.**","a[3][7]")
        True
        >>> test("a.**","a[3][7]")
        True
        >>> test("a.*.**","a.b.c")
        True
        >>> test("a.*.**","a.b")
        False
        >>> test("a.*","a.b.c")
        False
        >>> test("a.**","a.b.c")
        True
        >>> test("a.b.**","a.b.c")
        True
        """
        # pylint: disable=too-many-return-statements, too-many-branches
        l=len(pattern_list)
        kl= len(keylist)
        if kl<l: # keylist shorter patternlist
            return False
        exact_match= True
        patternkey= pattern_list[-1]
        if isinstance(patternkey, SpecialKey):
            if patternkey.recursive_wildcard():
                exact_match= False
        if exact_match:
            if kl>l:
                return False
        for i in range(l):
            patternkey= pattern_list[i]
            if isinstance(patternkey, SpecialKey):
                # pylint: disable= no-else-continue
                if patternkey.simple_wildcard():
                    if not patternkey.match(keylist[i]):
                        return False
                    continue
                elif SpecialKey.recursive_wildcard(patternkey):
                    if i!=l-1:
                        raise ValueError("'**' pattern only allowed at "+\
                                          "the end of the patternlist")
                    return True
                else:
                    if patternkey!=keylist[i]:
                        return False
            if patternkey!=keylist[i]:
                return False
        return True

ROOTKEY        = SpecialKey(SpecialKeyTypes.root)
root_key_str   = str(ROOTKEY)
ANYKEY         = SpecialKey(SpecialKeyTypes.any_key)
ANYKEYS        = SpecialKey(SpecialKeyTypes.any_keys)

def string_to_keyobject(val):
    """convert a wildcard to be used by the MatchPaths object.

    uses ROOTKEY, ANYKEY and ANYKEYS.
    """
    if val=="#":
        return ROOTKEY
    if val=="*":
        return ANYKEY
    if val=="**":
        return ANYKEYS
    if isinstance(val, str):
        return unescape_in_stringkey(val)
    return val


# ---------------------------------------------------------
# type checking

enumclass.NewEnum(globals(), "SDTypes",
                  [ "boolean", "integer", "real", "string",
                    "optional_struct",
                    "open_struct",
                    "struct",
                    "typed_map",
                    "map",
                    "optional_list",
                    "typed_list",
                    "list",
                  ])

def check_type_scalar(var, spec, dry_run=False):
    """implement a simple typecheck.

    Three basic scalar types are implemented here:
    SDTypes.boolean: a bool
    SDTypes.integer: an int
    SDTypes.real   : a float
    SDTypes.string : a str

    Here are some examples:

    >>> check_type_scalar(1,SDTypes.integer)
    >>> check_type_scalar(1.2,SDTypes.integer)
    Traceback (most recent call last):
        ...
    TypeError: integer expected, got: 1.2
    >>> check_type_scalar(1.2,SDTypes.real)
    >>> check_type_scalar(1,SDTypes.real)
    >>> check_type_scalar("A",SDTypes.real)
    Traceback (most recent call last):
        ...
    TypeError: real number expected, got: 'A'
    >>> check_type_scalar("A",SDTypes.string)
    >>> check_type_scalar(1,SDTypes.string)
    Traceback (most recent call last):
        ...
    TypeError: string expected, got: 1
    >>> check_type_scalar(True,SDTypes.boolean)
    >>> check_type_scalar(False,SDTypes.boolean)
    >>> check_type_scalar("True",SDTypes.boolean)
    Traceback (most recent call last):
        ...
    TypeError: boolean expected, got: 'True'
    >>> check_type_scalar(1,SDTypes.boolean)
    Traceback (most recent call last):
        ...
    TypeError: boolean expected, got: 1
    """
    # pylint: disable=too-many-return-statements, too-many-branches
    if not isinstance(spec, SDTypesValue):
        raise TypeError("spec must be of type SDTypesValue")
    if spec==SDTypes.boolean:
        if dry_run:
            return
        if not isinstance(var, bool):
            raise TypeError("boolean expected, got: %s" % repr(var))
        return
    if spec==SDTypes.integer:
        if dry_run:
            return
        if not isinstance(var, int):
            raise TypeError("integer expected, got: %s" % repr(var))
        return
    if spec==SDTypes.real:
        if dry_run:
            return
        if (not isinstance(var, float)) and (not isinstance(var, int)):
            raise TypeError("real number expected, got: %s" % repr(var))
        return
    if spec==SDTypes.string:
        if dry_run:
            return
        if not isinstance(var, str):
            raise TypeError("string expected, got: %s" % repr(var))
        return
    raise AssertionError("unexpected typespec: \"%s\"" % spec)

def check_type(var, spec, dry_run=False):
    """implement more complex typechecks.

    These are the known types:

    SDTypes.boolean
      a bool

    SDTypes.integer
      an int

    SDTypes.real
      a float

    SDTypes.string
      a str

    SDTypes.optional_struct [<list of items>]
      This is a dict where each key must be present in the <list of items>.

    SDTypes.open_struct [<list of items>]
      This is a dict where each item of <list of items> must be present as a
      key. Aside from this, the dict may contain an arbitrary set of additional
      of keys.

    SDTypes.struct [<list of items>]
      This is a dict where each item of <list of items> must be present as a
      key. No other keys are allowed than the ones listed in <list of items>.

    SDTypes.typed_map <scalar type>
      This is a dict where each key must be of the type <scalar type>.  <scalar
      type> may be SDTypes.integer, "float" or SDTypes.string.

    SDTypes.map
      This is simply a dict.

    SDTypes.optional_list [<list of items>]
      This is a list where each item must be present in <list of items>.

    SDTypes.typed_list <scalar type>
      This is a list where each item must be of the type <scalar type>.
      <scalar type> may be SDTypes.integer, "float" or SDTypes.string.

    SDTypes.list
      This is simply a list.

    Here are some examples:

    >>> check_type(True,SDTypes.boolean)
    >>> check_type(False,SDTypes.boolean)
    >>> check_type("A",SDTypes.boolean)
    Traceback (most recent call last):
        ...
    TypeError: boolean expected, got: 'A'
    >>> check_type(1,SDTypes.integer)
    >>> check_type(1.2,SDTypes.integer)
    Traceback (most recent call last):
        ...
    TypeError: integer expected, got: 1.2
    >>> check_type(1.2,SDTypes.real)
    >>> check_type(1,SDTypes.real)
    >>> check_type("A",SDTypes.real)
    Traceback (most recent call last):
        ...
    TypeError: real number expected, got: 'A'
    >>> check_type("A",SDTypes.string)
    >>> check_type(1,SDTypes.string)
    Traceback (most recent call last):
        ...
    TypeError: string expected, got: 1

    Tests with the type SDTypes.optional_struct:

    >>> check_type({"a":1,"c":1},{SDTypes.optional_struct:["a","b","c"]})
    >>> check_type({"a":1,"d":1},{SDTypes.optional_struct:["a","b","c"]})
    Traceback (most recent call last):
            ...
    TypeError: key d not in list of allowed keys
    >>> check_type(["a","b"],{SDTypes.optional_struct:["a","b","c"]})
    Traceback (most recent call last):
            ...
    TypeError: structure expected

    Tests with the type SDTypes.open_struct:

    >>> check_type({"a":1,"b":1,"c":1},{SDTypes.open_struct:["a","b","c"]})
    >>> check_type({"a":1,"b":1,"c":1,"d":1},{SDTypes.open_struct:["a","b","c"]})
    >>> check_type({"a":1,"b":1,"d":1},{SDTypes.open_struct:["a","b","c"]})
    Traceback (most recent call last):
        ...
    TypeError: key c is missing

    Tests with the type SDTypes.struct:

    >>> check_type({"a":1,"b":1,"c":1},{SDTypes.struct:["a","b","c"]})
    >>> check_type({"a":1,"b":1},{SDTypes.struct:["a","b","c"]})
    Traceback (most recent call last):
        ...
    TypeError: mandatory key c is missing
    >>> check_type({"a":1,"b":1,"c":1,"d":1},{SDTypes.struct:["a","b","c"]})
    Traceback (most recent call last):
        ...
    TypeError: key d is not in list of allowed keys

    Tests with the type SDTypes.typed_map:

    >>> check_type({"a":1,"b":1},{SDTypes.typed_map:SDTypes.string})
    >>> check_type({2:1,"b":1},{SDTypes.typed_map:SDTypes.string})
    Traceback (most recent call last):
        ...
    TypeError: string expected, got: 2

    Tests with the type SDTypes.map:

    >>> check_type({"a":1,"c":1},SDTypes.map)
    >>> check_type([1,2],SDTypes.map)
    Traceback (most recent call last):
        ...
    TypeError: map expected
    >>> check_type(1,SDTypes.map)
    Traceback (most recent call last):
        ...
    TypeError: map expected

    Tests with the type SDTypes.optional_list:

    >>> check_type(["a","c"],{SDTypes.optional_list:["a","b","c"]})
    >>> check_type(["a","d"],{SDTypes.optional_list:["a","b","c"]})
    Traceback (most recent call last):
        ...
    TypeError: item d not in list of allowed keys
    >>> check_type({"a":1,"b":2},{SDTypes.optional_list:["a","b","c"]})
    Traceback (most recent call last):
        ...
    TypeError: list expected

    Tests with the type SDTypes.typed_list:

    >>> check_type(["a","b"],{SDTypes.typed_list:SDTypes.string})
    >>> check_type(["a","b",1],{SDTypes.typed_list:SDTypes.string})
    Traceback (most recent call last):
        ...
    TypeError: string expected, got: 1

    Tests with the type SDTypes.list:

    >>> check_type([1,2],SDTypes.list)
    >>> check_type({"a":1,"c":1},SDTypes.list)
    Traceback (most recent call last):
        ...
    TypeError: list expected
    >>> check_type(1,SDTypes.list)
    Traceback (most recent call last):
        ...
    TypeError: list expected
    """
    # pylint: disable=too-many-return-statements, too-many-branches
    # pylint: disable=too-many-statements
    # pylint: disable= no-else-return
    if isinstance(spec, dict):
        if len(spec)!=1:
            raise AssertionError("spec dictionary must have exactly one key")
        (spec_key,spec_val)= list(spec.items())[0]
        if not isinstance(spec_key, SDTypesValue):
            raise TypeError("spec_key must be of type SDTypesValue")
        if spec_key==SDTypes.optional_struct:
            if not hasattr(spec_val, "__contains__"):
                raise AssertionError("spec value must be a list or set")
            if dry_run:
                return
            if not isinstance(var, dict):
                raise TypeError("structure expected")
            # each key must be in list of allowed keys
            for key in var.keys():
                if not key in spec_val:
                    raise TypeError("key %s not in list of allowed keys" % key)
            return
        elif spec_key==SDTypes.open_struct:
            if not hasattr(spec_val, "__contains__"):
                raise AssertionError("spec value must be a list or set")
            if dry_run:
                return
            if not isinstance(var, dict):
                raise TypeError("structure expected")
            # each of the allowed keys must be present
            keys= set(var.keys())
            for a in spec_val:
                if a not in keys:
                    raise TypeError("key %s is missing" % a)
            return
        elif spec_key==SDTypes.struct:
            if not hasattr(spec_val, "__contains__"):
                raise AssertionError("spec value must be a list or set")
            if dry_run:
                return
            if not isinstance(var, dict):
                raise TypeError("structure expected")
            # exactly all of the allowed keys must be present
            keys= set(var.keys())
            if isinstance(spec_val, set):
                allowed= spec_val
            else:
                allowed= set(spec_val)
            all_= keys.union(allowed)
            for k in all_:
                if k not in keys:
                    raise TypeError("mandatory key %s is missing" % k)
                if k not in allowed:
                    raise TypeError("key %s is not in list of allowed keys" % k)
            return
        elif spec_key==SDTypes.typed_map:
            check_type_scalar(None, spec_val, True)
            if dry_run:
                return
            if not isinstance(var, dict):
                raise TypeError("map expected")
            for k in var.keys():
                check_type_scalar(k, spec_val)
            return
        elif spec_key==SDTypes.optional_list:
            if not hasattr(spec_val, "__contains__"):
                raise AssertionError("spec value must be a list or set")
            if dry_run:
                return
            if not isinstance(var, list):
                raise TypeError("list expected")
            # each item must be in list of allowed keys
            allowed= spec_val
            for item in var:
                if not item in allowed:
                    raise TypeError("item %s not in list of allowed keys" % item)
            return
        elif spec_key==SDTypes.typed_list:
            check_type_scalar(None, spec_val, True)
            if dry_run:
                return
            if not isinstance(var, list):
                raise TypeError("list expected")
            for k in var:
                check_type_scalar(k, spec_val)
            return
        else:
            raise AssertionError("unknown type spec: %s" % k)
    elif isinstance(spec, SDTypesValue):
        if spec==SDTypes.map:
            if dry_run:
                return
            if not isinstance(var, dict):
                raise TypeError("map expected")
            return
        elif spec==SDTypes.list:
            if dry_run:
                return
            if not isinstance(var, list):
                raise TypeError("list expected")
            return
        else:
            check_type_scalar(var, spec, dry_run)
            return
    else:
        raise AssertionError("unknown type spec: \"%s\"" % repr(spec))

class SingleTypeSpec():
    """a single type specification.

    Optimized for quicker typechecks.

    Here are some examples:

    >>> s= SingleTypeSpec("integer")
    >>> repr(s)
    "SingleTypeSpec('integer')"
    >>> str(s)
    "SingleTypeSpec('integer')"
    >>> s.check(1)
    >>> s.check(1.2)
    Traceback (most recent call last):
        ...
    TypeError: integer expected, got: 1.2
    >>> s=SingleTypeSpec({"optional_struct":["x","y","z"]})
    >>> repr(s)
    "SingleTypeSpec({'optional_struct': ['x', 'y', 'z']})"
    >>> str(s)
    "SingleTypeSpec({'optional_struct': ['x', 'y', 'z']})"
    >>> s.check({"x":1,"z":2})
    >>> s.check({"x":1,"a":2})
    Traceback (most recent call last):
        ...
    TypeError: key a not in list of allowed keys
    """
    def __init__(self, dict_):
        self._val= SingleTypeSpec._from_SD(dict_)
        # self._val is either a SDTypesValue or a
        # dict mapping a SDTypesValue to an SDTypesValue or a set
    def check(self, var, dry_run= False):
        """check a type."""
        return check_type(var, self._val, dry_run=dry_run)
    def __repr__(self):
        d= self.to_dict()
        return "SingleTypeSpec(%s)" % repr(d)
    def __str__(self):
        d= self.to_dict()
        lines= ["SingleTypeSpec("]
        l= pprint.pformat(d, indent=2, width=70).split("\n")
        if len(l)==1:
            return "SingleTypeSpec(%s)" % l[0]
        l[-1]+="\n)"
        lines.extend(l)
        return "\n  ".join(lines)
    def items(self):
        """returns the internal set of items if there is one.

        Since this method returns the internal set object, it can be used to
        manipulate the set directly.

        Here are some examples:

        >>> s= SingleTypeSpec("integer")
        >>> s.items()
        Traceback (most recent call last):
            ...
        TypeError: the typespec has no items
        >>> s=SingleTypeSpec({"optional_struct":["x","y","z"]})
        >>> print(Repr.repr(s.items()))
        {'x', 'y', 'z'}
        >>> s.items().add("w")
        >>> print(s)
        SingleTypeSpec({'optional_struct': ['w', 'x', 'y', 'z']})
        >>> s.items().remove("x")
        >>> print(s)
        SingleTypeSpec({'optional_struct': ['w', 'y', 'z']})
        """
        if not isinstance(self._val, dict):
            raise TypeError("the typespec has no items")
        k= list(self._val.keys())[0]
        v= self._val[k]
        if not isinstance(v, set):
            raise TypeError("the typespec has no items")
        return v
    @staticmethod
    def _from_SD(val):
        """helper to create a SingleTypeSpec from a dict or str.

        If val is a str (string) this function returns a SDTypesValue created
        from that string.

        If val is a dictionary this function expects that this dictionary has
        exactly one key. It returns a dictionary with one key which is a
        SDTypesValue created from the single dictionary key that is mapped to
        an SDTypesValue or a set.
        """
        if isinstance(val, dict):
            if len(val)!=1:
                raise AssertionError("spec dictionary must have exactly one key")
            sk= list(val.keys())[0]
            k= SDTypesValue(sk)
            v= val[sk]
            if isinstance(v, list):
                v= set(v)
            elif isinstance(v, str):
                v= SDTypesValue(v)
            else:
                raise AssertionError("unexpected val %s in spec %s" % (repr(v), repr(val)))
            return { k: v }
        if isinstance(val, str):
            try:
                return SDTypesValue(val)
            except ValueError:
                raise ValueError("unknown typespec: \"%s\"" % val)
        raise AssertionError("unexpected spec: %s" % repr(val))
    def to_dict(self):
        """convert the SingleTypeSpec object to a dictionary."""
        if isinstance(self._val, dict):
            if len(self._val)!=1:
                raise AssertionError("self._val dictionary must have exactly one key")
            k= list(self._val.keys())[0]
            if not isinstance(k, SDTypesValue):
                raise TypeError("key must be of type SDTypesValue")
            v= self._val[k]
            k= str(k)
            if isinstance(v, set):
                v= sorted(v)
            elif isinstance(v, SDTypesValue):
                v= str(v)
            else:
                raise AssertionError("unexpected val %s in self._val %s" % \
                      (repr(v), repr(self._val)))
            return { k: v }
        if isinstance(self._val, SDTypesValue):
            return str(self._val)
        raise AssertionError("unexpected self._val: %s" % repr(self._val))

# ---------------------------------------------------------

# notes:
# keylist:
# a list of strings/ints

class StructuredDataStore():
    """defines a universal data store.

    This class is used to represent the StructuredDataStore. A
    StructuredDataStore contains the pure data as a python dictionary which may
    contain simple values or references to further dictionaries or lists. It
    also may contain a *link dictionary*. This dictionary maps python object
    ids (every python object has an id) to sets of keylists. When the
    StructuredDataStore is modified by using it's methods it tries to keep the
    link dictionary up to date (if it exists), but it cannot cover all cases.
    Especially you should use the *link* method when you plan to refer to the
    same data at several places of the StructuredDataStore.
    """
    # pylint: disable=too-many-public-methods
    _re_br= re.compile(r'(?<!\\)(\[)')
    _re_split= re.compile(r'(?<!\\)\.')
    _re_no= re.compile(r'\[(\d+)\]')

    # -----------------------------------------------------
    # creation / initialization

    @staticmethod
    def from_flat_dict(data=None):
        """create StructuredDataStore from a flat dictionary.

        This initializes the object from a flat dictionary structure. A flat
        dictionary is a dictionary that maps paths to values. These paths and
        the values are used to generate a complete StructuredDataStore
        structure.

        Here is an example:

        >>> p= StructuredDataStore.from_flat_dict({"A.B.C":1, "A.B.D":2})
        >>> print(p)
        StructuredDataStore({'A': {'B': {'C': 1, 'D': 2}}})
        """
        if data is None:
            data= {}
        new= StructuredDataStore()
        new.setitems(iter(data.items()), create_missing= True)
        return new
    def clone(self, deepcopy= True):
        """clones a StructuredDataStore object.

        This creates a copy of the StructuredDataStore. If the parameter
        deepcopy is True, a *deep* copy is performed where the new
        StructuredDataStore is completely independent from the first
        StructuredDataStore meaning that changes on the first one do never
        affect the new one.

        Here are some examples:

        >>> d= {"A": {"B": 1, "C": 2},
        ...      "x": {"y":None},
        ...      "l": [["val"], 1, None]
        ...    }
        >>> d["x"]["y"]= d["A"]
        >>> d["l"][2]= d["l"][0]
        >>> p= StructuredDataStore(d)
        >>> print(p)
        StructuredDataStore(
          { 'A': {'B': 1, 'C': 2},
            'l': [['val'], 1, ['val']],
            'x': {'y': {'B': 1, 'C': 2}}}
        )
        >>> shallow= p.clone(False)
        >>> deep   = p.clone(True)
        >>> p["A"]["B"]="CHANGED!"
        >>> print(p)
        StructuredDataStore(
          { 'A': {'B': 'CHANGED!', 'C': 2},
            'l': [['val'], 1, ['val']],
            'x': {'y': {'B': 'CHANGED!', 'C': 2}}}
        )
        >>> print(shallow)
        StructuredDataStore(
          { 'A': {'B': 'CHANGED!', 'C': 2},
            'l': [['val'], 1, ['val']],
            'x': {'y': {'B': 'CHANGED!', 'C': 2}}}
        )
        >>> print(deep)
        StructuredDataStore(
          { 'A': {'B': 1, 'C': 2},
            'l': [['val'], 1, ['val']],
            'x': {'y': {'B': 1, 'C': 2}}}
        )
        """
        new= StructuredDataStore()
        # pylint: disable= protected-access
        if not deepcopy:
            new._data= copy.copy(self._data)
        else:
            new._data= copy.deepcopy(self._data)
        return new
    def __init__(self, data=None):
        """initialize the object.

        This initializes the object. A python dictionary can be given as an
        optional parameter. In this case, the internal dictionary becomes a
        reference to the given dictionary.
        """
        if data is None:
            data= {}
        self._data= data
        self._link_dict= None
        self._locked= False

    # -----------------------------------------------------
    # exporting

    def as_dict(self):
        """return the as_dict data.

        This method returns the StructuredDataStore as a python dictionary.
        Note that this does not copy the data, it just returns the internal
        dictionary.

        Here is a simple example:

        >>> d={"key1":1, "key2": {"A":"x","B":"y"}, "key3":[1,2,3,{"float":1.23}]}
        >>> p= StructuredDataStore(d)
        >>> Repr.printrepr(p.as_dict())
        {'key1': 1, 'key2': {'A': 'x', 'B': 'y'}, 'key3': [1, 2, 3, {'float': 1.23}]}
        """
        if self._locked:
            raise ValueError("returning StructuredDataStore as a dict failed, "+\
                  "object is locked")
        return self._data
    def as_flat_dict(self, pattern="", show_links= False,
                     path_list= None,
                    ):
        """return the data in the "flat dict" form.

        This method returns the StructuredDataStore as a flat python
        dictionary. This is a dictionary that maps paths to values.

        Here are some examples:

        >>> d={"key1":1, "key2": {"A":"x","B":"y"}, "key3":[1,2,3,{"float":1.23}]}
        >>> p= StructuredDataStore(d)
        >>> Repr.printnice(p.as_flat_dict(), 0)
        {
          'key1': 1,
          'key2.A': 'x',
          'key2.B': 'y',
          'key3[0]': 1,
          'key3[1]': 2,
          'key3[2]': 3,
          'key3[3].float': 1.23
        }
        >>> Repr.printrepr(p.as_flat_dict(pattern="key3.**"))
        {'key3[0]': 1, 'key3[1]': 2, 'key3[2]': 3, 'key3[3].float': 1.23}
        >>> Repr.printrepr(p.as_flat_dict(pattern="key3[3].**"))
        {'key3[3].float': 1.23}
        >>> Repr.printrepr(p.as_flat_dict(pattern="key3[3].float"))
        {'key3[3].float': 1.23}
        >>> Repr.printrepr(p.as_flat_dict(pattern=["key2.**","key3.*"]))
        {'key2.A': 'x', 'key2.B': 'y', 'key3[0]': 1, 'key3[1]': 2, 'key3[2]': 3}
        """
        # if show_links:
        #     join= lambda l: self.annotated_join_path(l)
        # else:
        #     join= StructuredDataStore.join_path
        d={}
        for (path,_,val) in self.universal_iter(patterns=pattern,
                                                path_list= path_list,
                                                only_leaves= True,
                                                sorted_= False,
                                                show_links= show_links):
            # print("PATH:",path,"VAL:",val)
            d[path]= val
        return d
    def as_csv(self, stream= None, delimiter=',',
               align_values= False, value_first= False):
        """return the data in csv form.

        This method returns the StructuredDataStore as csv. If the parameter
        "stream" is supplied it writes to that stream, otherwise it returns a
        string.

        parameters:

        stream
          the stream to print(to. If this is None, return a string with the)
          data.

        align_values
          the value is in the last column, all values are aligned meaning they
          are all at the same column number. If thus parameter is False, the
          values are in the last column of each line but they may be at
          different column numbers in the different lines.

        value_first
          put the value in the first column, *before* all keys.

        Here is a simple example:

        >>> d={"key1":1, "key2": {"A":"x","B":"y"}, "key3":[1,2,3,{"float":1.23}]}
        >>> p= StructuredDataStore(d)
        >>> print(p.as_csv())
        key1,1
        key2,A,x
        key2,B,y
        key3,0,1
        key3,1,2
        key3,2,3
        key3,3,float,1.23
        <BLANKLINE>
        >>> print(p.as_csv(value_first= True))
        1,key1
        x,key2,A
        y,key2,B
        1,key3,0
        2,key3,1
        3,key3,2
        1.23,key3,3,float
        <BLANKLINE>
        >>> print(p.as_csv(align_values=True))
        key1,,,1
        key2,A,,x
        key2,B,,y
        key3,0,,1
        key3,1,,2
        key3,2,,3
        key3,3,float,1.23
        <BLANKLINE>
        """
        # pylint: disable=too-many-locals
        if stream is not None:
            result= stream
        else:
            result= io.StringIO()
        csvwriter= csv.writer(result,
                              delimiter= delimiter,
                              lineterminator= os.linesep)
        if align_values:
            pair_list= []
            max_keylen= 0


        for (_,keys,val) in self.direct_iter(pattern="",
                                             only_leaves= True,
                                             sorted_= True,
                                             show_links= False):
            if align_values:
                pair_list.append((keys[:], val))
                # ^^^ necessary since direct_iter returns *the same*
                # list object at each iteration
                max_keylen= max(max_keylen, len(keys))
            else:
                if value_first:
                    csvwriter.writerow([val]+keys)
                else:
                    csvwriter.writerow(keys+[val])
        if align_values:
            for keylist, v in pair_list:
                if len(keylist)<max_keylen:
                    keylist.extend([""]*(max_keylen-len(keylist)))
                keylist.append(v)
                csvwriter.writerow(keylist)
        if stream is None:
            contents= result.getvalue()
            result.close()
            return contents
        stream.close()
        return None

    # -----------------------------------------------------
    # other global functions

    def lock(self):
        """make the StructuredDataStore read-only."""
        self._locked= True
    def clear(self):
        """delete all data.

        This removes all data from the object.
        """
        if self._locked:
            raise ValueError("modification of StructuredDataStore failed, "+\
                  "object is locked")
        self._data= {}

    # -----------------------------------------------------
    # adding data from python structures

    def add(self, data):
        """adds new data to the StructuredDataStore object.

        This adds new data from a given dictionary representation of a
        StructuredDataStore. Note that different from the update method of
        dict, dictionaries in the structure that already exist are not replaced
        with the ones given in the new structure but new keys are added. Data
        must be a dict or a list of pairs.
        """
        if self._locked:
            raise ValueError("modification of StructuredDataStore failed, "+\
                  "object is locked")
        dictutils.struct_add(self._data, data)
    def update(self, data):
        """updates the StructuredDataStore from the given dictionary.

        This updates the StructuredData object from a given dictionary. Note
        that existing dictionaries are replaced by the ones in the given data.
        You usually want to use the "add" method instead of this one.
        """
        if self._locked:
            raise ValueError("modification of StructuredDataStore failed, "+\
                  "object is locked")
        self._data.update(data)

    # -----------------------------------------------------
    # querying/adding/modifying by keylists

    def keylist_set(self, keylist, new_value= None, always_dicts= False):
        """set the object that is identified by a keylist.

        This method sets a value in the StructuredDataStore that is referred by
        the given keylist. When the parameter create_missing is True, this
        function can also create data structures on the fly when the given keys
        do not yet exist at some place in the structure. The last data item
        created is given by the parameter new_value, which defaults to the
        value "None". Note that updates the internal link dictionary correctly
        only if the value given is not yet present in the StructuredDataStore.
        If the value *is* already present in the StructuredDataStore you should
        use the method link instead.

        Here are some examples:

        >>> p=StructuredDataStore({})
        >>> p.keylist_set(["ab"])
        >>> p
        StructuredDataStore({'ab': None})
        >>> p.keylist_set(["ab","x","y",1,"a"])
        >>> p
        StructuredDataStore({'ab': {'x': {'y': [None, {'a': None}]}}})
        >>> p.keylist_set(["ab","x","z"],"myvalue")
        'myvalue'
        >>> p
        StructuredDataStore({'ab': {'x': {'y': [None, {'a': None}], 'z': 'myvalue'}}})
        """
        if self._locked:
            raise ValueError("modification of StructuredDataStore failed, "+\
                  "object is locked")
        if self._link_dict is not None:
            self._links_remove(keylist)
        dictutils.struct_keylist_add(self._data, keylist,
                                     new_value, always_dicts)
        return new_value

    def keylist2object(self, keylist):
        """get the object that is identified by a keylist.

        This method returns for a given keylist the part of the
        StructuredDataStore it adresses.

        Here are some examples:

        >>> d={"key1":1, "key2": {"A":"x","B":"y"}, "key3":[1,2,3,{"float":1.23}]}
        >>> p= StructuredDataStore(d)
        >>> p.keylist2object(["key2"])
        {'A': 'x', 'B': 'y'}
        >>> p.keylist2object(["key2","B"])
        'y'
        >>> p.keylist2object(["key3",1])
        2
        >>> p.keylist2object(["key3",3])
        {'float': 1.23}
        >>> p.keylist2object(["key3",3,"float"])
        1.23
        >>> p.keylist2object(["key3",3,"floatx"])
        Traceback (most recent call last):
           ...
        KeyError: "['key3', 3, 'floatx'] not found (subkey: 'floatx')"
        """
        return dictutils.struct_keylist_get(self._data, keylist)

    def listsetitem(self, keylist, val, create_missing= False,
                    always_dicts= False):
        """similar to setitem, but gets a keylist.

        This method sets for a given path the part of the StructuredDataStore
        it addresses. If the parameter create_missing is True, this function
        can also create data structures on the fly when the given keys do not
        yet exist at some place in the structure. If the parameter always_dicts
        is True, the created structures are always dicts and never lists even
        if some of the elements of the path are integers.
        """
        if self._locked:
            raise ValueError("modification of StructuredDataStore failed, "+\
                  "object is locked")
        if create_missing:
            self.keylist_set(keylist, val, always_dicts= always_dicts)
        else:
            dictutils.struct_keylist_change(self._data, keylist, val)
        if self._link_dict is not None:
            self._links_remove(keylist)

    def listdelitem(self, keylist):
        """deletes an item from the store.

        This is similar to delitem but gets a keylist instead of a path.

        Here is an example:

        >>> d={"key1":1, "key2": {"A":"x","B":"y"}, "key3":[1,2,3,{"float":1.23}]}
        >>> p= StructuredDataStore(d)
        >>> print(p)
        StructuredDataStore(
          { 'key1': 1,
            'key2': {'A': 'x', 'B': 'y'},
            'key3': [1, 2, 3, {'float': 1.23}]}
        )
        >>> p.listdelitem(["key3",3,"float"])
        >>> print(p)
        StructuredDataStore(
          {'key1': 1, 'key2': {'A': 'x', 'B': 'y'}, 'key3': [1, 2, 3, {}]}
        )
        >>> p.listdelitem(["key3",3])
        >>> print(p)
        StructuredDataStore(
          {'key1': 1, 'key2': {'A': 'x', 'B': 'y'}, 'key3': [1, 2, 3]}
        )
        """
        if self._locked:
            raise ValueError("modification of StructuredDataStore failed, "+\
                  "object is locked")
        last= keylist[-1]
        new_keylist= keylist[0:-1]
        del self.keylist2object(new_keylist)[last]
        self._links_remove(keylist)


    # -----------------------------------------------------
    # querying/adding/modifying by paths

    def path2object(self, path):
        """get the object a path points to.

        This method returns for a given path the part of the
        StructuredDataStore it adresses.

        Here are some examples:

        >>> d={"key1":1, "key2": {"A":"x","B":"y"}, "key3":[1,2,3,{"float":1.23}]}
        >>> p= StructuredDataStore(d)
        >>> p.path2object("key2")
        {'A': 'x', 'B': 'y'}
        >>> p.path2object("key2.A")
        'x'
        >>> p.path2object("key3[1]")
        2
        >>> p.path2object("key3[3]")
        {'float': 1.23}
        >>> p.path2object("key3[3].float")
        1.23
        >>> p.path2object("key3[3].floatx")
        Traceback (most recent call last):
            ...
        KeyError: "['key3', 3, 'floatx'] not found (subkey: 'floatx')"
        """
        return self.keylist2object(StructuredDataStore.split_path(path))

    def __getitem__(self, path):
        """return the object the path points to.

        This method returns for a given path the part of the
        StructuredDataStore it addresses. This means that you may read elements
        in a StructuredDataStore object by addressing it like a dictionary like
        "object[path]".

        Here are some examples:

        >>> d={"key1":1, "key2": {"A":"x","B":"y"}, "key3":[1,2,3,{"float":1.23}]}
        >>> p= StructuredDataStore(d)
        >>> p["key2"]
        {'A': 'x', 'B': 'y'}
        >>> p["key2.A"]
        'x'
        >>> p["key3[1]"]
        2
        >>> p["key3[3]"]
        {'float': 1.23}
        >>> p["key3[3].float"]
        1.23
        >>> p["key3[3].floatx"]
        Traceback (most recent call last):
            ...
        KeyError: "['key3', 3, 'floatx'] not found (subkey: 'floatx')"
        """
        return self.path2object(path)

    def __setitem__(self, path, val):
        """sets an item in the StructuredDataStore.

        This method sets for a given path the part of the StructuredDataStore
        it addresses. This means that you may assign elements in a
        StructuredDataStore object by addressing it like a dictionary like
        "object[path]=value".
        """
        return self.setitem(path, val, create_missing= False)

    def setitem(self, path, val, create_missing= False, always_dicts= False):
        """set the object the path points to.

        This method sets for a given path the part of the StructuredDataStore
        it addresses. If the parameter create_missing is True, this function
        can also create data structures on the fly when the given keys do not
        yet exist at some place in the structure. If the parameter always_dicts
        is True, the created structures are always dicts and never lists even
        if some of the elements of the path are integers.

        Here are some examples:

        >>> d={"key1":1, "key2": {"A":"x","B":"y"}, "key3":[1,2,3,{"float":1.23}]}
        >>> p= StructuredDataStore(d)
        >>> print(p)
        StructuredDataStore(
          { 'key1': 1,
            'key2': {'A': 'x', 'B': 'y'},
            'key3': [1, 2, 3, {'float': 1.23}]}
        )
        >>> p["key1"]= 10
        >>> print(p)
        StructuredDataStore(
          { 'key1': 10,
            'key2': {'A': 'x', 'B': 'y'},
            'key3': [1, 2, 3, {'float': 1.23}]}
        )
        >>> p["key2.A"]= "xx"
        >>> print(p)
        StructuredDataStore(
          { 'key1': 10,
            'key2': {'A': 'xx', 'B': 'y'},
            'key3': [1, 2, 3, {'float': 1.23}]}
        )
        >>> p["key3[3].float"]= 2.46
        >>> print(p)
        StructuredDataStore(
          { 'key1': 10,
            'key2': {'A': 'xx', 'B': 'y'},
            'key3': [1, 2, 3, {'float': 2.46}]}
        )
        >>> p["key3[3].floatx"]= 3.46
        Traceback (most recent call last):
            ...
        KeyError: "['key3', 3, 'floatx'] not found (subkey: 'floatx')"
        >>> p.setitem("key3[3].floatx",3.46,create_missing=True)
        >>> print(p)
        StructuredDataStore(
          { 'key1': 10,
            'key2': {'A': 'xx', 'B': 'y'},
            'key3': [1, 2, 3, {'float': 2.46, 'floatx': 3.46}]}
        )
        """
        if self._locked:
            raise ValueError("modification of StructuredDataStore failed, "+\
                  "object is locked")
        keylist= StructuredDataStore.split_path(path)
        self.listsetitem(keylist, val,
                         create_missing=create_missing,
                         always_dicts= always_dicts)

    def setitems(self, pairs, create_missing= False, always_dicts= False):
        """add new items to the object from a list of pairs.

        This method sets for a list of path-value pairs part of the
        StructuredDataStore they address. If the parameter create_missing is
        True, this function can also create data structures on the fly when the
        given keys do not yet exist at some place in the structure.
        """
        if self._locked:
            raise ValueError("modification of StructuredDataStore failed, "+\
                  "object is locked")
        for (k,v) in pairs:
            self.setitem(k, v, create_missing, always_dicts= always_dicts)

    def __delitem__(self, path):
        """deletes an item from the store.

        This method deletes an item from the StructuredDataStore. This means
        you can use the statement "del store[path]" to delete an item from the
        store.

        Here is an example:

        >>> d={"key1":1, "key2": {"A":"x","B":"y"}, "key3":[1,2,3,{"float":1.23}]}
        >>> p= StructuredDataStore(d)
        >>> print(p)
        StructuredDataStore(
          { 'key1': 1,
            'key2': {'A': 'x', 'B': 'y'},
            'key3': [1, 2, 3, {'float': 1.23}]}
        )
        >>> del p["key3[3].float"]
        >>> print(p)
        StructuredDataStore(
          {'key1': 1, 'key2': {'A': 'x', 'B': 'y'}, 'key3': [1, 2, 3, {}]}
        )

        >>> del p["key3[3]"]
        >>> print(p)
        StructuredDataStore(
          {'key1': 1, 'key2': {'A': 'x', 'B': 'y'}, 'key3': [1, 2, 3]}
        )
        """
        return self.delitem(path)

    def delitem(self, path):
        """deletes an item from the store.

        This is the explicit deletion method, it's function is the same as
        __delitem__.

        Here is an example:

        >>> d={"key1":1, "key2": {"A":"x","B":"y"}, "key3":[1,2,3,{"float":1.23}]}
        >>> p= StructuredDataStore(d)
        >>> print(p)
        StructuredDataStore(
          { 'key1': 1,
            'key2': {'A': 'x', 'B': 'y'},
            'key3': [1, 2, 3, {'float': 1.23}]}
        )
        >>> p.delitem("key3[3].float")
        >>> print(p)
        StructuredDataStore(
          {'key1': 1, 'key2': {'A': 'x', 'B': 'y'}, 'key3': [1, 2, 3, {}]}
        )
        >>> p.delitem("key3[3]")
        >>> print(p)
        StructuredDataStore(
          {'key1': 1, 'key2': {'A': 'x', 'B': 'y'}, 'key3': [1, 2, 3]}
        )
        """
        if self._locked:
            raise ValueError("modification of StructuredDataStore failed, "+\
                  "object is locked")
        keylist= StructuredDataStore.split_path(path)
        return self.listdelitem(keylist)

    # -----------------------------------------------------
    # link handling

    def links_keylist_sets(self):
        """return a dictionary mapping ids to sets of keylists.

        This function returns a dictionary mapping object IDs to sets of
        keylists.  The dictionary only contains entries for objects that are
        referred by the StructuredDataStore at at least two places. The
        dictionary is computed by iterating over all possible paths in the
        StructuredDataStore, so it may take some time to complete.

        Here are some examples:

        >>> d= {"A": {"B": 1, "C": 2},
        ...      "x": {"y":None},
        ...      "l": [["val"], 1, None]
        ...    }
        >>> d["x"]["y"]= d["A"]
        >>> d["l"][2]= d["l"][0]
        >>> s= StructuredDataStore(d)

        Since the ids in the returned dictionary are not reproducible within
        this doctest code, we cannot print(them directly:)

        >>> def myprint(linkdict):
        ...     d= {}
        ...     l= sorted([sorted(x) for x in linkdict.values()])
        ...     idx=1
        ...     for it in l:
        ...         d[idx]= set(it)
        ...         idx+=1
        ...     Repr.printrepr(d)

        >>> myprint(s.links_keylist_sets())
        {1: {('A',), ('x', 'y')}, 2: {('l', 0), ('l', 2)}}
        """
        def walk(val, id_keylists, keylist):
            """walk all nodes."""
            if id(val) in id_keylists:
                id_keylists[id(val)].add(keylist)
                return
            id_keylists[id(val)]= set( (keylist,) )
            iterator= dictutils.key_val_iterator(val)
            for (k,v) in iterator:
                if not is_iterable(v):
                    continue
                walk(v, id_keylists, keylist+(k,))

        if not is_iterable(self._data):
            raise AssertionError("self._data is no iterable")
        id_keylists= {}
        walk(self._data, id_keylists, ())
        result= {}
        for (k,v) in id_keylists.items():
            if len(v)<=1:
                continue
            result[k]= v
        self._link_dict= result
        return result
    def links_path_sets(self):
        """return a dict mapping ids to sets of paths refer to the same data.

        This function is similar to links_keylist_sets but it returns a
        dictionary mapping object IDs to sets of paths.

        Here are some examples:

        >>> d= {"A": {"B": 1, "C": 2},
        ...      "x": {"y":None},
        ...      "l": [["val"], 1, None]
        ...    }
        >>> d["x"]["y"]= d["A"]
        >>> d["l"][2]= d["l"][0]
        >>> s= StructuredDataStore(d)

        Since the ids in the returned dictionary are not reproducible within
        this doctest code, we cannot print(them directly:)

        >>> def myprint(linkdict):
        ...     d= {}
        ...     l= sorted([sorted(x) for x in linkdict.values()])
        ...     idx=1
        ...     for it in l:
        ...         d[idx]= set(it)
        ...         idx+=1
        ...     Repr.printrepr(d)

        >>> myprint(s.links_path_sets())
        {1: {'A', 'x.y'}, 2: {'l[0]', 'l[2]'}}
        """
        d= self.links_keylist_sets()
        for k,s in d.items():
            new= {StructuredDataStore.join_path(keys) for keys in s}
            d[k]= new
        return d
    def _links_remove(self, keylist):
        """remove a keylist tuple from the _link_dict.
        """
        if self._link_dict is None:
            return
        val= None
        try:
            val= self.keylist2object(keylist)
        except KeyError:
            val= None
        except IndexError:
            val= None
        if val is None:
            return
        val_id= id(val)
        keylist_set= self._link_dict.get(val_id)
        if keylist_set is None:
            return
        if len(keylist_set)<=2:
            del self._link_dict[val_id]
            return
        keylist_set.discard(tuple(keylist))
    def _links_add(self, from_keylist, to_keylist, val):
        """add a keylist tuple to the _link_dict.
        """
        if self._link_dict is None:
            return
        id_val= id(val)
        keylist_set= self._link_dict.get(id_val)
        if keylist_set is None:
            self._link_dict[id_val]= set((tuple(from_keylist), tuple(to_keylist)))
        else:
            keylist_set.add(tuple(from_keylist))

    def refresh_links(self):
        """refresh the information on links.

        This function refreshes the internal link directory of the
        StructuredDataStore. Since it iterates over all possible paths in the
        StructuredDataStore it may take some time to complete. You should call
        this function if you need information about links in the
        StructuredDataStore after the data has been modifed by functions
        directly operating on the internal dictionary or after data has been
        imported.

        Here are some examples:

        >>> d= {"A": {"B": 1, "C": 2},
        ...      "x": {"y":None},
        ...      "l": [["val"], 1, None]
        ...    }
        >>> d["x"]["y"]= d["A"]
        >>> d["l"][2]= d["l"][0]
        >>> s= StructuredDataStore(d)
        >>> s.refresh_links()

        Since the ids in the returned dictionary are not reproducible within
        this doctest code, we cannot print(them directly:)

        >>> def myprint(linkdict):
        ...     d= {}
        ...     l= sorted([sorted(x) for x in linkdict.values()])
        ...     idx=1
        ...     for it in l:
        ...         d[idx]= set(it)
        ...         idx+=1
        ...     Repr.printrepr(d)

        >>> myprint(s._link_dict)
        {1: {('A',), ('x', 'y')}, 2: {('l', 0), ('l', 2)}}
        """
        # links_keylist_sets updates self._link_dict:
        self.links_keylist_sets()
    def _get_links_by_id(self, id_):
        """get the links from a given object-id.
        """
        if self._link_dict is None:
            self.refresh_links()
        return self._link_dict.get(id_) # returns None or a keylist-set

    def get_links(self,path,include=None, exclude=None):
        """returns all paths that point to the same data as "path".

        This function returns a set of paths that refer to the same data as the
        given path including the given path. If no other paths refer to the
        same data, a set that just contains the given path is returned.  Note
        that "path" is also in the list, so this will return a list with one
        element, "path" if there are no links.

        Here are some examples:

        >>> d= {"A": {"B": 1, "C": 2},
        ...      "x": {"y":None},
        ...      "l": [["val"], 1, None]
        ...    }
        >>> d["x"]["y"]= d["A"]
        >>> d["l"][2]= d["l"][0]
        >>> s= StructuredDataStore(d)
        >>> print(Repr.repr(s.get_links("A")))
        {'A', 'x.y'}
        >>> print(Repr.repr(s.get_links("x.y")))
        {'A', 'x.y'}
        >>> print(Repr.repr(s.get_links("x")))
        {'x'}
        >>> print(Repr.repr(s.get_links("l[2]")))
        {'l[0]', 'l[2]'}
        >>> print(Repr.repr(s.get_links("A",include="x.*")))
        {'x.y'}
        >>> print(Repr.repr(s.get_links("A",exclude="x.*")))
        {'A'}
        >>> print(Repr.repr(s.get_links("l[2]",include="l[0]")))
        {'l[0]'}
        """
        val= self[path] # may raise Exception
        key_tuples= self._get_links_by_id(id(val))
        if key_tuples is None:
            return set((path,))
        if include is not None:
            # all set entries have to match
            include_lst= StructuredDataStore.split_path(include)
            key_tuples= [x for x in key_tuples \
                         if SpecialKey.list_match(include_lst,x)]
        if exclude is not None:
            # all set entries must not match
            exclude_lst= StructuredDataStore.split_path(exclude)
            key_tuples= [x for x in key_tuples \
                         if not SpecialKey.list_match(exclude_lst,x)]
        return {StructuredDataStore.join_path(keylist) \
                for keylist in key_tuples}
    def pattern_get_links(self, pattern,
                          include=None, exclude=None,
                          only_multi_links= True):
        """do get_links for all paths that match a pattern.

        This function returns a sorted list of sets of paths where each path in
        each set refers to the same data. At least one path in each set of
        paths matches the given pattern.

        Here are some examples:

        >>> d= {"A": {"B": 1, "C": 2},
        ...      "x": {"y":None},
        ...      "l": [["val"], 1, None]
        ...    }
        >>> d["x"]["y"]= d["A"]
        >>> d["l"][2]= d["l"][0]
        >>> s= StructuredDataStore(d)
        >>> print(Repr.repr(s.pattern_get_links("l.*")))
        [{'l[0]', 'l[2]'}]
        >>> print(Repr.repr(s.pattern_get_links("*")))
        [{'A', 'x.y'}]
        >>> print(Repr.repr(s.pattern_get_links("*.y")))
        [{'A', 'x.y'}]
        >>> print(Repr.repr(s.pattern_get_links("*.z")))
        []
        >>> print(Repr.repr(s.pattern_get_links("*",only_multi_links= True)))
        [{'A', 'x.y'}]
        >>> print(Repr.repr(s.pattern_get_links("*",only_multi_links= False)))
        [{'A', 'x.y'}, {'x'}, {'l'}]
        >>> print(Repr.repr(s.pattern_get_links("*.y",exclude="*")))
        [{'x.y'}]
        >>> print(Repr.repr(s.pattern_get_links("*.y",exclude="*.*")))
        [{'A'}]
        >>> print(Repr.repr(s.pattern_get_links("*",include="*.*")))
        [{'x.y'}]
        >>> print(Repr.repr(s.pattern_get_links("*",include="*")))
        [{'A'}]
        """
        def filter_(keys_tuples, include, exclude):
            """filters keys_tuples.
            Note: may change a set of tuples to a list of tuples
            """
            if include is not None:
                keys_tuples= [x for x in keys_tuples \
                              if SpecialKey.list_match(include,x)]
            if exclude is not None:
                keys_tuples= [x for x in keys_tuples \
                              if not SpecialKey.list_match(exclude,x)]
            return keys_tuples

        if self._link_dict is None:
            self.refresh_links()
        if include is not None:
            include= StructuredDataStore.split_path(include)
        if exclude is not None:
            exclude= StructuredDataStore.split_path(exclude)
        results= []
        found= set()
        paths= self.simple_search(pattern, add_values= False,
                                  only_leaves= False)
        for path in paths:
            val= self[path]
            val_id= id(val)
            if val_id not in found:
                path_set= self._link_dict.get(val_id)
                if path_set is None:
                    if only_multi_links:
                        continue
                    path_set= set(path)
                else:
                    found.add(val_id)
                    path_set= filter_(path_set, include, exclude)
                    if not path_set:
                        continue
                    path_set= {StructuredDataStore.join_path(keys) \
                               for keys in path_set}
                results.append(path_set)
        return sorted(results)

    def is_linked(self,path):
        """returns True if another path points to the same data.

        This function returns True if there is at least one other path that
        refers to the same data as the given path.

        Here are some examples:

        >>> d= {"A": {"B": 1, "C": 2},
        ...      "x": {"y":None},
        ...      "l": [["val"], 1, None]
        ...    }
        >>> d["x"]["y"]= d["A"]
        >>> d["l"][2]= d["l"][0]
        >>> s= StructuredDataStore(d)
        >>> s.is_linked("A")
        True
        >>> s.is_linked("A.B")
        False
        >>> s.is_linked("l[2]")
        True
        """
        l= self.get_links(path)
        return len(l)>1

    def link(self, from_path, to_path):
        """sets store[from_path]= store[to_path].

        This function creates a link. The data for the path "from_path" is
        changed to refer to the same data as the path "to_path". This function
        updates the internal link dictionary accordingly.

        Here are some examples:

        >>> d= {"A": {"B": 1, "C": 2},
        ...      "x": {"y":None},
        ...      "l": [["val"], 1, None]
        ...    }
        >>> s= StructuredDataStore(d)
        >>> print(s)
        StructuredDataStore(
          {'A': {'B': 1, 'C': 2}, 'l': [['val'], 1, None], 'x': {'y': None}}
        )
        >>> s.link("x.y", "A")
        >>> print(s)
        StructuredDataStore(
          { 'A': {'B': 1, 'C': 2},
            'l': [['val'], 1, None],
            'x': {'y': {'B': 1, 'C': 2}}}
        )
        >>> print(Repr.repr(s.get_links("A")))
        {'A', 'x.y'}
        >>> s.link("l[2]","l[0]")
        >>> print(s)
        StructuredDataStore(
          { 'A': {'B': 1, 'C': 2},
            'l': [['val'], 1, ['val']],
            'x': {'y': {'B': 1, 'C': 2}}}
        )
        >>> print(Repr.repr(s.get_links("l[0]")))
        {'l[0]', 'l[2]'}
        """
        if self._locked:
            raise ValueError("modification of StructuredDataStore failed, "+\
                  "object is locked")
        if self._link_dict is None:
            self.refresh_links()
        from_keylist= StructuredDataStore.split_path(from_path)
        to_keylist  = StructuredDataStore.split_path(to_path)
        to_val= self.keylist2object(to_keylist)
        self.listsetitem(from_keylist, to_val,
                         create_missing= True,
                         always_dicts= False)
        self._links_remove(from_keylist)
        self._links_add(from_keylist, to_keylist, to_val)

    # -----------------------------------------------------
    # iteration across the structure
    def selection_iter(self, pattern, path_list,
                       only_leaves,
                       sorted_, show_links,
                       paths_found_set= None):
        """iteration through a path list.

        Here are some examples:

        >>> d={"key1":1, "key2": {"A":"x","B":"y"}, "key3":[1,2,3,{"float":1.23}]}
        >>> p= StructuredDataStore(d)
        >>> def test(s,pattern,path_list,only_leaves,sorted_,
        ...          show_links=False, paths_found_set= None):
        ...   for l in s.selection_iter(pattern,path_list,only_leaves,
        ...                             sorted_,show_links,paths_found_set):
        ...     print(repr(l))

        >>> test(p,"",['key3[0]','key3[3]'],False,False)
        ('key3[0]', ['key3', 0], 1)
        ('key3[3]', ['key3', 3], {'float': 1.23})

        >>> test(p,"",[('key3[0]',1),('key3[2]',3)],False,False)
        ('key3[0]', ['key3', 0], 1)
        ('key3[2]', ['key3', 2], 3)

        >>> pset= set()
        >>> test(p,"",['key3[0]','key3[3]','key3[3].float'],True,True,False,pset)
        ('key3[0]', ['key3', 0], 1)
        ('key3[3].float', ['key3', 3, 'float'], 1.23)
        >>> test(p,"",['key3[0]','key3[3]','key3[3].float'],False,True,False,pset)
        ('key3[3]', ['key3', 3], {'float': 1.23})

        >>> d={"key1":{"A":"x1","B":"y1"},
        ...    "key2":{"A":"x2","B":"y2"},
        ...    "key3":[1,2,3,{"float":1.23}]}
        >>> p= StructuredDataStore(d)
        >>> test(p,"key1",['key1','key1.A','key2.A'],False,True)
        ('key1', ['key1'], {'A': 'x1', 'B': 'y1'})
        >>> test(p,"key1.**",['key1','key1.A','key2.A'],False,True)
        ('key1.A', ['key1', 'A'], 'x1')
        >>> test(p,"*.A",['key1','key1.A','key2.A'],False,True)
        ('key1.A', ['key1', 'A'], 'x1')
        ('key2.A', ['key2', 'A'], 'x2')

        >>> d={"key1":{"A":"x1","B":"y1"}}
        >>> d["key1"]["B"]= d["key1"]
        >>> p= StructuredDataStore(d)
        >>> test(p,"",["key1","key1.A","key1.B"],False,True)
        ('key1', ['key1'], {'A': 'x1', 'B': {...}})
        ('key1.A', ['key1', 'A'], 'x1')
        ('key1.B', ['key1', 'B'], {'A': 'x1', 'B': {...}})
        >>> test(p,"",["key1","key1.A","key1.B"],False,True,True)
        ('key1*', [('key1', '*')], {'A': 'x1', 'B': {...}})
        ('key1*.A', [('key1', '*'), 'A'], 'x1')
        ('key1*.B*', [('key1', '*'), ('B', '*')], {'A': 'x1', 'B': {...}})
        """
        # pylint: disable=too-many-locals
        def link_check(path, keylist, link_dict):
            """sets the link flags for the keys.

            parameters:

            path
              The path

            keylist
              The corresponding keylist

            link_dict
              Here we remember if a path was already checked for links
            """
            if not show_links:
                return (path, keylist)
            sub_path= ""
            newkeylist= []
            for i, k in enumerate(keylist):
                sub_path= StructuredDataStore.append_path(sub_path, k)

                flag= link_dict.get(sub_path)
                if flag is None:
                    v= self.keylist2object(keylist[:i+1])
                    s= self._get_links_by_id(id(v))
                    flag= (s is not None)
                    link_dict[sub_path]= flag
                if flag:
                    newkeylist.append((k,"*"))
                else:
                    newkeylist.append(k)
                continue
            return (StructuredDataStore.join_path(newkeylist), newkeylist)
        # ----------
        pattern_list= StructuredDataStore.split_path(pattern)
        if not pattern_list:
            pattern_list=[ANYKEYS]
        if sorted_:
            path_list= sorted(path_list)
        link_dict= {}
        for path in path_list:
            # if elements of path_list are tuples or lists take
            # the first element:
            if is_iterable(path):
                path= path[0]
            keys= StructuredDataStore.split_path(path)
            value= self.keylist2object(keys)
            if only_leaves:
                if is_iterable(value):
                    continue
            if not SpecialKey.list_match(pattern_list, keys):
                continue
            (npath, nkeys)= link_check(path, keys, link_dict)
            if paths_found_set is None:
                yield (npath, nkeys, value)
            else:
                if path not in paths_found_set:
                    yield (npath,nkeys,value)
                    paths_found_set.add(path)

    def direct_iter(self, pattern,
                    only_leaves,
                    sorted_, show_links,
                    paths_found_set= None):
        """Iteration through the StructuredDataStore.

        This method returns an iterator on all the nodes of the
        StructuredDataStore. For each iteration it returns a tuple consisting
        of the path, the keylist and the value of that node.

        parameters:

        pattern
          A path pattern that is used to filter the results.  If this is None
          or an empty string, the results are not filtered.

        only_leaves
          If this is true, only nodes that are scalars are returned.

        sorted
          If this is true, iteration through map keys is sorted.

        show_links
          If this is true, links are marked in the result.

        paths_found_set
          If this parameter is given, it should be a set.  Paths that already
          are in this set are not returned.  Paths found are added to this
          set.

        returns:

        a tuple (path,keys,value)

        IMPORTANT NOTE:
        The keys returned at each iteration are NOT a new list but the same
        list with a new content at each iteration. If you use this iterator to
        store the keylist somewhere keep in mind that you have to make a
        shallow copy of the keylist like in "my_keylist= keylist[:]".  Note
        that list comprehension WILL NOT work due to this reason.

        Here are some examples:

        >>> d={"key1":1, "key2": {"A":"x","B":"y"}, "key3":[1,2,3,{"float":1.23}]}
        >>> p= StructuredDataStore(d)
        >>> def test(s,pattern,only_leaves,sorted_,
        ...          show_links=False, paths_found_set= None):
        ...   for l in s.direct_iter(pattern,only_leaves,
        ...                             sorted_,show_links,paths_found_set):
        ...     print(repr(l))

        >>> test(p,"",False,True)
        ('key1', ['key1'], 1)
        ('key2', ['key2'], {'A': 'x', 'B': 'y'})
        ('key2.A', ['key2', 'A'], 'x')
        ('key2.B', ['key2', 'B'], 'y')
        ('key3', ['key3'], [1, 2, 3, {'float': 1.23}])
        ('key3[0]', ['key3', 0], 1)
        ('key3[1]', ['key3', 1], 2)
        ('key3[2]', ['key3', 2], 3)
        ('key3[3]', ['key3', 3], {'float': 1.23})
        ('key3[3].float', ['key3', 3, 'float'], 1.23)

        >>> pset= set()
        >>> test(p,"",True,True,False,pset)
        ('key1', ['key1'], 1)
        ('key2.A', ['key2', 'A'], 'x')
        ('key2.B', ['key2', 'B'], 'y')
        ('key3[0]', ['key3', 0], 1)
        ('key3[1]', ['key3', 1], 2)
        ('key3[2]', ['key3', 2], 3)
        ('key3[3].float', ['key3', 3, 'float'], 1.23)

        >>> test(p,"",False,True,False,pset)
        ('key2', ['key2'], {'A': 'x', 'B': 'y'})
        ('key3', ['key3'], [1, 2, 3, {'float': 1.23}])
        ('key3[3]', ['key3', 3], {'float': 1.23})

        >>> d={"key0":1,
        ...    "key1":{"A":"x1","B":"y1"},
        ...    "key2":{"A":"x2","B":"y2"},
        ...    "key3":[1,2,3,{"float":1.23}]}
        >>> p= StructuredDataStore(d)

        >>> test(p,"",False,True)
        ('key0', ['key0'], 1)
        ('key1', ['key1'], {'A': 'x1', 'B': 'y1'})
        ('key1.A', ['key1', 'A'], 'x1')
        ('key1.B', ['key1', 'B'], 'y1')
        ('key2', ['key2'], {'A': 'x2', 'B': 'y2'})
        ('key2.A', ['key2', 'A'], 'x2')
        ('key2.B', ['key2', 'B'], 'y2')
        ('key3', ['key3'], [1, 2, 3, {'float': 1.23}])
        ('key3[0]', ['key3', 0], 1)
        ('key3[1]', ['key3', 1], 2)
        ('key3[2]', ['key3', 2], 3)
        ('key3[3]', ['key3', 3], {'float': 1.23})
        ('key3[3].float', ['key3', 3, 'float'], 1.23)
        >>> test(p,"key2",False,True)
        ('key2', ['key2'], {'A': 'x2', 'B': 'y2'})
        >>> test(p,"key2.**",False,True)
        ('key2.A', ['key2', 'A'], 'x2')
        ('key2.B', ['key2', 'B'], 'y2')
        >>> test(p,"key3",False,True)
        ('key3', ['key3'], [1, 2, 3, {'float': 1.23}])
        >>> test(p,"key3.*",False,True)
        ('key3[0]', ['key3', 0], 1)
        ('key3[1]', ['key3', 1], 2)
        ('key3[2]', ['key3', 2], 3)
        ('key3[3]', ['key3', 3], {'float': 1.23})
        >>> test(p,"key3.**",False,True)
        ('key3[0]', ['key3', 0], 1)
        ('key3[1]', ['key3', 1], 2)
        ('key3[2]', ['key3', 2], 3)
        ('key3[3]', ['key3', 3], {'float': 1.23})
        ('key3[3].float', ['key3', 3, 'float'], 1.23)
        >>> test(p,"*.A",False,True)
        ('key1.A', ['key1', 'A'], 'x1')
        ('key2.A', ['key2', 'A'], 'x2')
        >>> test(p,"*[0]",False,True)
        ('key3[0]', ['key3', 0], 1)
        >>> test(p,"*[3].**",False,True)
        ('key3[3].float', ['key3', 3, 'float'], 1.23)

        >>> d={"key1":{"A":"x1","B":"y1"}}
        >>> d["key1"]["B"]= d["key1"]
        >>> p= StructuredDataStore(d)
        >>> test(p,"",False,True)
        ('key1', ['key1'], {'A': 'x1', 'B': {...}})
        ('key1.A', ['key1', 'A'], 'x1')
        ('key1.B', ['key1', 'B'], {'A': 'x1', 'B': {...}})
        >>> test(p,"",False,True,True)
        ('key1*', [('key1', '*')], {'A': 'x1', 'B': {...}})
        ('key1*.A', [('key1', '*'), 'A'], 'x1')
        ('key1*.B*', [('key1', '*'), ('B', '*')], {'A': 'x1', 'B': {...}})
        """
        # pylint: disable= too-many-locals, too-many-branches
        # pylint: disable= too-many-statements
        def pattern_iterator(val, patternkey, sorted_, show_links):
            """iterator with a given pattern.

            val MUST be a collection !
            """
            def k_chg(k,v):
                """key change ?"""
                if not show_links:
                    return (k,v)
                s= self._get_links_by_id(id(v))
                if s is None:
                    return (k,v)
                return ((k,"*"),v)
            # ---------
            # pylint: disable= no-else-return
            if isinstance(patternkey, SpecialKey):
                if patternkey.simple_wildcard():
                    for (k,v) in dictutils.key_val_iterator(val, sorted_=sorted_):
                        if patternkey.match(k):
                            yield k_chg(k,v)
                    return
                elif patternkey.recursive_wildcard():
                    for (k,v) in dictutils.key_val_iterator(val, sorted_=sorted_):
                        yield k_chg(k,v)
                    return
                else:
                    raise ValueError("unexpected specialkey: %s" % repr(patternkey))
            else:
                try:
                    v= val[patternkey]
                except KeyError:
                    return
                except TypeError:
                    return
                yield k_chg(patternkey, v)
                return

        # -----------------
        depth= 0
        pattern_list= StructuredDataStore.split_path(pattern)
        if not pattern_list:
            pattern_list=[ANYKEYS]
        pattern_len= len(pattern_list)
        pattern_key= pattern_list[depth]
        paths= [""]
        path= ""
        keys= [None]
        value= self._data
        id_set= set((id(self._data),))
        id_list= [id(self._data)]
        iterators= [pattern_iterator(value, pattern_key, sorted_, show_links)]
        while True:
            try:
                #print("keys:",repr(keys))
                #print("iterators:",iterators)
                (keys[-1],value)= next(iterators[-1])
                # print("KEY",repr(keys[-1]))
            except StopIteration:
                iterators.pop()
                keys.pop()
                paths.pop()
                id_set.discard( id_list.pop() )
                depth-=1
                if depth<0:
                    return
                if depth+1>=pattern_len:
                    pattern_key= pattern_list[-1] # can only happen with ANYKEYS
                else:
                    pattern_key= pattern_list[depth+1]
                continue

            is_collection= is_iterable(value)

            path= StructuredDataStore.append_path(paths[-1], keys[-1])

            if (not only_leaves) or (not is_collection):
                if (depth == pattern_len-1) or \
                   SpecialKey.is_recursive_wildcard(pattern_key):
                    if paths_found_set is None:
                        yield (path,keys,value)
                    else:
                        if path not in paths_found_set:
                            yield (path,keys,value)
                            paths_found_set.add(path)

            if is_collection:
                if id(value) in id_set:
                    continue
                if not SpecialKey.is_recursive_wildcard(pattern_key):
                    if depth+1>=pattern_len:
                        continue
                    pattern_key= pattern_list[depth+1]

                id_list.append(id(value))
                id_set.add(id(value))

                keys.append(None)
                paths.append(path)
                iterators.append(pattern_iterator( value, pattern_key,
                                                   sorted_,
                                                   show_links))
                depth+=1

    def universal_iter(self, patterns, path_list,
                       only_leaves,
                       sorted_, show_links):
        """universal iteration through the StructuredDataStore with path_list.

        Here are some examples:

        >>> d={"key1":1, "key2": {"A":"x","B":"y"}, "key3":[1,2,3,{"float":1.23}]}
        >>> p= StructuredDataStore(d)
        >>> def test(s,patterns,path_list,only_leaves,sorted_,
        ...          show_links=False):
        ...   for l in s.universal_iter(patterns,path_list,only_leaves,
        ...                             sorted_,show_links):
        ...     print(repr(l))
        ...
        >>> test(p,"",['key3[0]','key3[3]'],False,True)
        ('key3[0]', ['key3', 0], 1)
        ('key3[3]', ['key3', 3], {'float': 1.23})
        >>> test(p,"",None,False,True)
        ('key1', ['key1'], 1)
        ('key2', ['key2'], {'A': 'x', 'B': 'y'})
        ('key2.A', ['key2', 'A'], 'x')
        ('key2.B', ['key2', 'B'], 'y')
        ('key3', ['key3'], [1, 2, 3, {'float': 1.23}])
        ('key3[0]', ['key3', 0], 1)
        ('key3[1]', ['key3', 1], 2)
        ('key3[2]', ['key3', 2], 3)
        ('key3[3]', ['key3', 3], {'float': 1.23})
        ('key3[3].float', ['key3', 3, 'float'], 1.23)
        >>> test(p,"key3.**",['key3','key3[0]','key3[3]'],False,True)
        ('key3[0]', ['key3', 0], 1)
        ('key3[3]', ['key3', 3], {'float': 1.23})
        >>> test(p,"key3.**",[],False,True)
        ('key3[0]', ['key3', 0], 1)
        ('key3[1]', ['key3', 1], 2)
        ('key3[2]', ['key3', 2], 3)
        ('key3[3]', ['key3', 3], {'float': 1.23})
        ('key3[3].float', ['key3', 3, 'float'], 1.23)
        >>> test(p,["key2.**","key3.**"],[],False,True)
        ('key2.A', ['key2', 'A'], 'x')
        ('key2.B', ['key2', 'B'], 'y')
        ('key3[0]', ['key3', 0], 1)
        ('key3[1]', ['key3', 1], 2)
        ('key3[2]', ['key3', 2], 3)
        ('key3[3]', ['key3', 3], {'float': 1.23})
        ('key3[3].float', ['key3', 3, 'float'], 1.23)
        """
        if not is_iterable(patterns):
            if not patterns:
                patterns= [""]
            else:
                patterns= [patterns]
            paths_found_set= None
        else:
            paths_found_set= set()
        for pattern in patterns:
            if not path_list:
                iter_= self.direct_iter(pattern= pattern,
                                        only_leaves= only_leaves,
                                        sorted_= sorted_,
                                        show_links= show_links,
                                        paths_found_set= paths_found_set)
            else:
                iter_= self.selection_iter(pattern= pattern,
                                           path_list= path_list,
                                           only_leaves= only_leaves,
                                           sorted_= sorted_,
                                           show_links= show_links,
                                           paths_found_set= paths_found_set)
            for(path,keylist,val) in iter_:
                yield(path,keylist,val)

    # -----------------------------------------------------
    # path pattern support

    def simple_search(self, path_patterns,
                      path_list= None,
                      add_values= False,
                      only_leaves=True,
                      show_links= False):
        """search all paths for a given pattern.

        This method is used to search the paths by a given pattern or list of
        patterns. It returns a list of paths or a list of path-value pairs.

        parameters:

        path_patterns
          This may be a pattern (a string) or a list of patterns (a list of
          strings). Only paths that match this or these patterns are
          returned.

        add_values
          If this is True, the returned list contains pairs of the path and
          the value. Otherwise, only paths are returned in the list.

        only_leaves
          If this is true, only nodes that are scalars are returned.

        show_links
          If this is true, links are marked in the result.

        returns:

        A list consisting of paths or path-value pairs.

        Here are some examples:

        >>> d={"key1":1, "key2": {"A":"x","B":"y"}, "key3":[1,2,3,{"float":1.23}]}
        >>> p= StructuredDataStore(d)
        >>> print( p)
        StructuredDataStore(
          { 'key1': 1,
            'key2': {'A': 'x', 'B': 'y'},
            'key3': [1, 2, 3, {'float': 1.23}]}
        )
        >>> print(p.simple_search("*.A", add_values=False))
        ['key2.A']
        >>> print(p.simple_search("key2.**", add_values=False))
        ['key2.A', 'key2.B']
        >>> print(p.simple_search("key3.*.float", add_values=False))
        ['key3[3].float']

        >>> pl=["key2","key2.B","key3[3].float"]
        >>> print(p.simple_search("*.A", path_list=pl, add_values=False))
        []
        >>> print(p.simple_search("*.B", path_list=pl, add_values=False))
        ['key2.B']
        >>> print(p.simple_search("key2.**", add_values=False))
        ['key2.A', 'key2.B']
        >>> print(p.simple_search("key2.**", path_list= pl, add_values=False))
        ['key2.B']

        >>> print(p.simple_search("key3.*.float", add_values=True))
        [('key3[3].float', 1.23)]
        >>> print(p.simple_search("key3.**", add_values=True))
        [('key3[0]', 1), ('key3[1]', 2), ('key3[2]', 3), ('key3[3].float', 1.23)]
        >>> print(p.simple_search("key3.*", add_values=True))
        [('key3[0]', 1), ('key3[1]', 2), ('key3[2]', 3)]

        >>> print(p.simple_search("*.A",["key1","key2.A","key2.B"],
        ...                       add_values=False))
        ['key2.A']
        >>> print(p.simple_search("*.A",["key1","key2.B"], add_values=False))
        []

        >>> d={"key1":1, "key2": {"A":"x","B":"y"}, "key3":[1,2,3,{"float":1.23}]}
        >>> d["key2"]["C"]= d["key3"]
        >>> p= StructuredDataStore(d)
        >>> print(p)
        StructuredDataStore(
          { 'key1': 1,
            'key2': {'A': 'x', 'B': 'y', 'C': [1, 2, 3, {'float': 1.23}]},
            'key3': [1, 2, 3, {'float': 1.23}]}
        )
        >>> print(p.simple_search("*.B", add_values=False, show_links=True))
        ['key2.B']
        >>> print(p.simple_search("*.C.**", add_values=False, show_links=True))
        ['key2.C*[0]', 'key2.C*[1]', 'key2.C*[2]', 'key2.C*[3].float']
        >>> print(p.simple_search("*.C.*", add_values=True, show_links=True))
        [('key2.C*[0]', 1), ('key2.C*[1]', 2), ('key2.C*[2]', 3)]
        """
        matched= []
        for (path,_,val) in self.universal_iter(patterns= path_patterns,
                                                path_list= path_list,
                                                only_leaves= only_leaves,
                                                sorted_= False,
                                                show_links= show_links):
            if add_values:
                matched.append((path, val))
            else:
                matched.append(path)
        return matched

    # -----------------------------------------------------
    # searching paths

    def _pattern_search(self, pattern,
                        is_rx_pattern,
                        path_list= None,
                        add_values= False,
                        only_leaves=True, show_links= False):
        """search all paths for a given pattern.
        """
        if is_rx_pattern:
            rx= re.compile(pattern)
            match= lambda st: rx.match(st) is not None
        else:
            words= pattern.split()
            match= lambda st: andmatch(st, words)
        matched= []

        for (path,_,val) in self.universal_iter(patterns="",
                                                path_list= path_list,
                                                only_leaves= only_leaves,
                                                sorted_= False,
                                                show_links= show_links):
            if not match(path):
                continue
            if add_values:
                matched.append((path, val))
            else:
                matched.append(path)
        return matched

    def i_search(self, i_pattern,
                 path_list= None,
                 add_values= False,
                 only_leaves=True, show_links= False):
        r"""search all paths for a given i-pattern.

        An "i-pattern" is a list of space separated sub-strings. All
        strings that contain all of these sub-strings in any order
        (compared case insensitive) match.

        Here are some examples:

        >>> d={"key1":1, "key2": {"A":"x","B":"y"}, "key3":[1,2,3,{"float":1.23}]}
        >>> p= StructuredDataStore(d)
        >>> print( p)
        StructuredDataStore(
          { 'key1': 1,
            'key2': {'A': 'x', 'B': 'y'},
            'key3': [1, 2, 3, {'float': 1.23}]}
        )

        >>> Repr.printrepr(sorted(p.i_search("1")))
        ['key1', 'key3[1]']
        >>> Repr.printrepr(sorted(p.i_search("1", add_values= False)))
        ['key1', 'key3[1]']
        >>> Repr.printrepr(sorted(p.i_search("float", add_values= False)))
        ['key3[3].float']
        >>> Repr.printrepr(sorted(p.i_search("float", add_values= True)))
        [('key3[3].float', 1.23)]
        >>> Repr.printrepr(sorted(p.i_search("2 key", add_values= True)))
        [('key2.A', 'x'), ('key2.B', 'y'), ('key3[2]', 3)]
        """
        return self._pattern_search(i_pattern, is_rx_pattern=False,
                                    path_list= path_list,
                                    add_values= add_values,
                                    only_leaves= only_leaves,
                                    show_links= show_links)

    def regexp_search(self, regexp_pattern,
                      path_list= None,
                      add_values= False,
                      only_leaves=True, show_links= False):
        r"""search all paths for a given regexp pattern.

        This method is used to search the paths by a given regular expression.
        It returns a list of paths or a list of path-value pairs. See the
        documentation of the python module "re" for regular expressions. If the
        parameter add_values is True, the values addressed by the paths are
        included in the result.

        Here are some examples:

        >>> d={"key1":1, "key2": {"A":"x","B":"y"}, "key3":[1,2,3,{"float":1.23}]}
        >>> p= StructuredDataStore(d)
        >>> print( p)
        StructuredDataStore(
          { 'key1': 1,
            'key2': {'A': 'x', 'B': 'y'},
            'key3': [1, 2, 3, {'float': 1.23}]}
        )
        >>> Repr.printrepr(sorted(p.regexp_search(r'.*1')))
        ['key1', 'key3[1]']
        >>> Repr.printrepr(sorted(p.regexp_search(r'.*1', add_values= False)))
        ['key1', 'key3[1]']
        >>> Repr.printrepr(sorted(p.regexp_search(r'.*float', add_values= False)))
        ['key3[3].float']
        >>> Repr.printrepr(sorted(p.regexp_search(r'.*float', add_values= True)))
        [('key3[3].float', 1.23)]
        >>> Repr.printrepr(sorted(p.regexp_search(r'^k.*\b[A-Z]', add_values= True)))
        [('key2.A', 'x'), ('key2.B', 'y')]

        >>> d={"key1":1, "key2": {"A":"x","B":"y"}, "key3":[1,2,3,{"float":1.23}]}
        >>> d["key2"]["C"]= d["key3"]
        >>> p= StructuredDataStore(d)
        >>> print(p)
        StructuredDataStore(
          { 'key1': 1,
            'key2': {'A': 'x', 'B': 'y', 'C': [1, 2, 3, {'float': 1.23}]},
            'key3': [1, 2, 3, {'float': 1.23}]}
        )
        >>> Repr.printrepr(sorted(p.regexp_search(r'.*1', show_links= True)))
        ['key1', 'key2.C*[1]', 'key3*[1]']
        >>> Repr.printrepr(sorted(p.regexp_search(r'.*float', add_values= True, show_links= True)))
        [('key2.C*[3].float', 1.23), ('key3*[3].float', 1.23)]
        """
        return self._pattern_search(regexp_pattern, is_rx_pattern=True,
                                    path_list= path_list,
                                    add_values= add_values,
                                    only_leaves= only_leaves,
                                    show_links= show_links)

    # -----------------------------------------------------
    # searching values

    def value_search(self, value,
                     path_patterns= None,
                     path_list= None,
                     add_values= False,
                     show_links= False):
        """search for an exact value.

        This method looks for values that are equal to the given value. It
        returns a list of paths or a list of path-value pairs.

        Here are some examples:

        >>> d={"key1":1, "key2": {"A":1,"B":2}, "key3":[1,2,3,{"float":1.23}]}
        >>> p= StructuredDataStore(d)
        >>> print( p)
        StructuredDataStore(
          { 'key1': 1,
            'key2': {'A': 1, 'B': 2},
            'key3': [1, 2, 3, {'float': 1.23}]}
        )
        >>> print(sorted(p.value_search(1)))
        ['key1', 'key2.A', 'key3[0]']
        >>> print(sorted(p.value_search(1, add_values= True)))
        [('key1', 1), ('key2.A', 1), ('key3[0]', 1)]
        >>> print(sorted(p.value_search(1.23)))
        ['key3[3].float']

        >>> print(sorted(p.value_search(1,path_list=["key2.A","key3"])))
        ['key2.A']

        >>> d={"key1":1, "key2": {"A":1,"B":2}, "key3":[1,2,3,{"float":1.23}]}
        >>> d["key2"]["C"]= d["key3"]
        >>> p= StructuredDataStore(d)
        >>> print(p)
        StructuredDataStore(
          { 'key1': 1,
            'key2': {'A': 1, 'B': 2, 'C': [1, 2, 3, {'float': 1.23}]},
            'key3': [1, 2, 3, {'float': 1.23}]}
        )
        >>> print(sorted(p.value_search(1, show_links= True)))
        ['key1', 'key2.A', 'key2.C*[0]', 'key3*[0]']
        >>> print(sorted(p.value_search(1, add_values= True, show_links= True)))
        [('key1', 1), ('key2.A', 1), ('key2.C*[0]', 1), ('key3*[0]', 1)]
        >>> print(sorted(p.value_search(1.23, show_links= True)))
        ['key2.C*[3].float', 'key3*[3].float']
        """
        matched= []
        for (path, _, val) in self.universal_iter(patterns= path_patterns,
                                                  path_list= path_list,
                                                  only_leaves= True,
                                                  sorted_= False,
                                                  show_links= show_links):
            if val!=value:
                continue
            if not add_values:
                matched.append(path)
            else:
                matched.append((path, val))
        return matched

    def _pattern_value_search(self, pattern,
                              is_rx_pattern,
                              path_patterns= None,
                              path_list= None,
                              add_values= False,
                              show_links= False):
        """search for a value with a pattern.
        """
        if is_rx_pattern:
            rx= re.compile(pattern)
            match= lambda st: rx.match(st) is not None
        else:
            words= pattern.split()
            match= lambda st: andmatch(st, words)
        matched= []
        for (path,_,val) in self.universal_iter(patterns= path_patterns,
                                                path_list= path_list,
                                                only_leaves= True,
                                                sorted_= False,
                                                show_links= show_links):
            if not match(str(val)):
                continue
            if add_values:
                matched.append((path, val))
            else:
                matched.append(path)
        return matched

    def value_i_search(self, i_pattern,
                       path_patterns= None,
                       path_list= None,
                       add_values= False,
                       show_links= False):
        r"""search all paths for a given i-pattern.

        An "i-pattern" is a list of space separated sub-strings. All
        strings that contain all of these sub-strings in any order
        (compared case insensitive) match.

        Here are some examples:

        >>> d={"key1":1, "key2": {"A":1,"B":2}, "key3":[1,2,3,{"float":1.23}]}
        >>> p= StructuredDataStore(d)
        >>> print( p)
        StructuredDataStore(
          { 'key1': 1,
            'key2': {'A': 1, 'B': 2},
            'key3': [1, 2, 3, {'float': 1.23}]}
        )
        >>> Repr.printrepr(sorted(p.value_i_search("1")))
        ['key1', 'key2.A', 'key3[0]', 'key3[3].float']
        >>> Repr.printrepr(sorted(p.value_i_search("2")))
        ['key2.B', 'key3[1]', 'key3[3].float']
        >>> Repr.printrepr(sorted(p.value_i_search("1 2")))
        ['key3[3].float']
        >>> Repr.printrepr(sorted(p.value_i_search("1", path_list=["key2.A","key3"])))
        ['key2.A']
        """
        return self._pattern_value_search(i_pattern,
                                          is_rx_pattern= False,
                                          path_patterns= path_patterns,
                                          path_list= path_list,
                                          add_values= add_values,
                                          show_links= show_links)

    def value_regexp_search(self, regexp_pattern,
                            path_patterns= None,
                            path_list= None,
                            add_values= False,
                            show_links= False):
        r"""search for a value with a regular expression.

        This method is used to search the values by a given regular expression.
        It returns a list of paths or a list of path-value pairs. See the
        documentation of the python module "re" for regular expressions. If the
        parameter add_values is True, the values addressed by the paths are
        included in the result.

        Here are some examples:

        >>> d={"key1":1, "key2": {"A":1,"B":2}, "key3":[1,2,3,{"float":1.23}]}
        >>> p= StructuredDataStore(d)
        >>> print( p)
        StructuredDataStore(
          { 'key1': 1,
            'key2': {'A': 1, 'B': 2},
            'key3': [1, 2, 3, {'float': 1.23}]}
        )
        >>> Repr.printrepr(sorted(p.value_regexp_search("1")))
        ['key1', 'key2.A', 'key3[0]', 'key3[3].float']
        >>> Repr.printrepr(sorted(p.value_regexp_search("[23]")))
        ['key2.B', 'key3[1]', 'key3[2]']
        >>> Repr.printrepr(p.value_regexp_search("\.", add_values= True))
        []
        >>> Repr.printrepr(p.value_regexp_search(r"\.", add_values= True))
        []
        >>> Repr.printrepr(sorted(p.value_regexp_search(r".*\.", add_values= True)))
        [('key3[3].float', 1.23)]

        >>> Repr.printrepr(sorted(p.value_regexp_search("1", path_list=["key2.A","key3"])))
        ['key2.A']

        >>> d={"key1":1, "key2": {"A":1,"B":2}, "key3":[1,2,3,{"float":1.23}]}
        >>> d["key2"]["C"]= d["key3"]
        >>> p= StructuredDataStore(d)
        >>> print(p)
        StructuredDataStore(
          { 'key1': 1,
            'key2': {'A': 1, 'B': 2, 'C': [1, 2, 3, {'float': 1.23}]},
            'key3': [1, 2, 3, {'float': 1.23}]}
        )
        >>> Repr.printnice(sorted(p.value_regexp_search("1", show_links= True)), 0)
        [
          'key1',
          'key2.A',
          'key2.C*[0]',
          'key2.C*[3].float',
          'key3*[0]',
          'key3*[3].float'
        ]
        >>> Repr.printrepr(sorted(p.value_regexp_search("[23]", show_links= True)))
        ['key2.B', 'key2.C*[1]', 'key2.C*[2]', 'key3*[1]', 'key3*[2]']
        """
        return self._pattern_value_search(regexp_pattern,
                                          is_rx_pattern= True,
                                          path_patterns= path_patterns,
                                          path_list= path_list,
                                          add_values= add_values,
                                          show_links= show_links)

    # -----------------------------------------------------
    # path utilities

    @staticmethod
    def _keyconvert(key, include_separator=False):
        if include_separator:
            separator= "."
        else:
            separator= ""
        if isinstance(key, tuple):
            extra= key[1]
            key= key[0]
        else:
            extra= ""
        if isinstance(key, SpecialKey):
            key= str(key)
        elif isinstance(key, str):
            key= escape_in_stringkey(key)
        elif isinstance(key, int):
            separator= ""
            key= "[%d]" % key
        else:
            key= str(key)
        return "".join((separator,key,extra))

    @staticmethod
    def join_path(keylist):
        r"""joins a path from a keylist.

        This method joins a list of keys to a path.  It doesn't need access to
        the StructuredDataStore so it is a static method. Usually each key of
        the keylist is a SpecialKey object, a string or an integer or a pair.
        In the latter case the pair consists of a SpecialKey, a string or an
        integer and an extra string. All these are combined to form a
        StructuredData path.

        Here are some examples:

        >>> print(StructuredDataStore.join_path(["A","B"]))
        A.B
        >>> print(StructuredDataStore.join_path(["A.B","C"]))
        A\.B.C
        >>> print(StructuredDataStore.join_path(["A",2,"C"]))
        A[2].C
        >>> print(StructuredDataStore.join_path(["A","*","C"]))
        A.\*.C
        >>> print(StructuredDataStore.join_path(["A","x[3]","C"]))
        A.x\[3\].C
        >>> print(StructuredDataStore.join_path(["A",ANYKEY,"B"]))
        A.*.B
        """
        path= ".".join([StructuredDataStore._keyconvert(x) for x in keylist])
        # avoid things like "A.[3]B":
        return path.replace(".[","[")

    @staticmethod
    def append_path(path, key):
        r"""append a key to a path.

        The key is a path key or a pair of a path key and an extra string.

        Here are some examples:

        >>> print(StructuredDataStore.append_path("a.b","c"))
        a.b.c
        >>> print(StructuredDataStore.append_path("a.b",3))
        a.b[3]
        >>> print(StructuredDataStore.append_path("a[1]","c"))
        a[1].c
        >>> print(StructuredDataStore.append_path("a[1]",2))
        a[1][2]
        >>> print(StructuredDataStore.append_path("","c"))
        c
        >>> print(StructuredDataStore.append_path("",3))
        [3]
        >>> print(StructuredDataStore.append_path("a[1]","x.y"))
        a[1].x\.y
        >>> print(StructuredDataStore.append_path("a[1]","*"))
        a[1].\*
        >>> print(StructuredDataStore.append_path("a[1]","**"))
        a[1].\**
        """
        return path + StructuredDataStore._keyconvert(key, bool(path))

    def annotated_join_path(self,keylist):
        """similar to join_path, but give hints on links.

        All keys in the path that relate to a linked object, one that is
        referred by other paths as well, get a "*" appended at the end.

        Note that list indices get the star appended to the closing bracket.
        Here are some examples:

        >>> d= {"A": {"B": 1, "C": None},
        ...      "x": {"y":None},
        ...      "l": [["val"], 1, None]
        ...    }
        >>> d["x"]["y"]= d["A"]
        >>> d["l"][2]= d["l"][0]
        >>> d["A"]["C"]= d["l"][0]
        >>> p= StructuredDataStore(d)
        >>> print(p)
        StructuredDataStore(
          { 'A': {'B': 1, 'C': ['val']},
            'l': [['val'], 1, ['val']],
            'x': {'y': {'B': 1, 'C': ['val']}}}
        )
        >>> p.annotated_join_path(["A","B"])
        'A*.B'
        >>> p.annotated_join_path(["A","B","C"])
        Traceback (most recent call last):
            ...
        KeyError: 'at key C, item is a scalar'
        >>> p.annotated_join_path(["A","C"])
        'A*.C*'
        >>> p.annotated_join_path(["l",0])
        'l[0]*'
        >>> p.annotated_join_path(["l",1])
        'l[1]'
        >>> p.annotated_join_path(["l",2])
        'l[2]*'
        >>> p.annotated_join_path(["x"])
        'x'
        >>> p.annotated_join_path(["x","y"])
        'x.y*'
        """
        if self._link_dict is None:
            self.refresh_links()
        current= self._data
        new_keylist= []
        for k in keylist:
            if not hasattr(current, "__getitem__"):
                raise KeyError("at key %s, item is a scalar" % k)
            current= current[k] # works for dicts and lists
            s= self._get_links_by_id(id(current))
            if s is not None:
                new_keylist.append((k,"*"))
            else:
                new_keylist.append(k)
        return StructuredDataStore.join_path(new_keylist)

    @staticmethod
    def split_path(path):
        r"""splits a path into a keylist.

        This static method splits a given path to a list of keys. Note that in
        the returned list, strings are map keys and integers are list indices.
        If the path is a pattern, the returned keylist may contain SpecialKey
        objects like ANYREY or ANYKEYS.

        >>> print(StructuredDataStore.split_path("A.B"))
        ['A', 'B']
        >>> print(StructuredDataStore.split_path(""))
        []
        >>> print(StructuredDataStore.split_path(r"A\.B.C"))
        ['A.B', 'C']
        >>> print(StructuredDataStore.split_path("A[2].C"))
        ['A', 2, 'C']
        >>> StructuredDataStore.split_path("A[xy].C")
        ['A', '[xy]', 'C']
        >>> StructuredDataStore.split_path("A[4][3].C")
        ['A', 4, 3, 'C']
        >>> StructuredDataStore.split_path("A.*.C")
        ['A', ANYKEY, 'C']
        >>> StructuredDataStore.split_path("A.**.C")
        ['A', ANYKEYS, 'C']
        """
        if not path: # empty string or None
            return []
        path= StructuredDataStore._re_br.sub(r".\1", path)
        lst= StructuredDataStore._re_split.split(path)
        res= []
        for elm in lst:
            m= StructuredDataStore._re_no.match(elm)
            if m is not None:
                elm= int(m.group(1))
            else:
                elm= string_to_keyobject(elm)
            res.append(elm)
        return res

    # -----------------------------------------------------
    # printing/dumping

    # pylint: disable= line-too-long
    def __repr__(self):
        """return representation of object.

        This returns a python expression that can be used to recreate the
        object.

        Here is an example:

        >>> d={"key1":1, "key2": {"A":"x","B":"y"}, "key3":[1,2,3,{"float":1.23}]}
        >>> p= StructuredDataStore(d)
        >>> print(repr(p))
        StructuredDataStore({'key1': 1, 'key2': {'A': 'x', 'B': 'y'}, 'key3': [1, 2, 3, {'float': 1.23}]})
        """
        return "StructuredDataStore(%s)" % Repr.repr(self._data)
    # pylint: enable= line-too-long
    def __str__(self):
        """return a more human readable representation of the object.

        Here is an example:

        >>> d={"key1":1, "key2": {"A":"x","B":"y"}, "key3":[1,2,3,{"float":1.23}]}
        >>> p= StructuredDataStore(d)
        >>> print(str(p))
        StructuredDataStore(
          { 'key1': 1,
            'key2': {'A': 'x', 'B': 'y'},
            'key3': [1, 2, 3, {'float': 1.23}]}
        )
        """
        lines= ["StructuredDataStore("]
        l= pprint.pformat(self._data, indent=2, width=70).split("\n")
        if len(l)==1:
            if len(l[0])<60:
                return "StructuredDataStore(%s)" % l[0]
        l[-1]+="\n)"
        lines.extend(l)
        return "\n  ".join(lines)



def _get_dict(dict_,key):
    """get dict_[key] or create this entry as a new dict."""
    res= dict_.get(key)
    if res is not None:
        return res
    new= {}
    dict_[key]= new
    return new

def _get_list(dict_,key):
    """get dict_[key] or create this entry as a new list."""
    res= dict_.get(key)
    if res is not None:
        return res
    new= []
    dict_[key]= new
    return new

def _sorted_unique_insert(lst, val):
    """insert an element in a list and keep the list sorted.

    It is also ensured that no element appears in the list twice.
    Here are some examples:

    >>> l=[]
    >>> _sorted_unique_insert(l,4)
    >>> l
    [4]
    >>> _sorted_unique_insert(l,4)
    >>> l
    [4]
    >>> _sorted_unique_insert(l,6)
    >>> l
    [4, 6]
    >>> _sorted_unique_insert(l,6)
    >>> l
    [4, 6]
    >>> _sorted_unique_insert(l,4)
    >>> l
    [4, 6]
    >>> _sorted_unique_insert(l,5)
    >>> l
    [4, 5, 6]
    >>> _sorted_unique_insert(l,5)
    >>> l
    [4, 5, 6]
    >>> _sorted_unique_insert(l,4)
    >>> l
    [4, 5, 6]
    >>> _sorted_unique_insert(l,6)
    >>> l
    [4, 5, 6]
    >>> _sorted_unique_insert(l,2)
    >>> l
    [2, 4, 5, 6]
    >>> _sorted_unique_insert(l,3)
    >>> l
    [2, 3, 4, 5, 6]
    >>> _sorted_unique_insert(l,10)
    >>> l
    [2, 3, 4, 5, 6, 10]
    """
    if not lst:
        lst.append(val)
        return
    l= len(lst)
    for i in range(l):
        if val<=lst[i]:
            if val==lst[i]:
                return
            lst.insert(i, val)
            return
    lst.append(val)

class MatchPaths():
    """This class provides a store for paths and a match function.

    This class provides a store for paths that can be used to find matching
    paths for a given path. A path within the MatchPaths object may contain
    wildcards, "*" matches any map key and any list index. Each path in a
    MatchPaths object is associated with an arbitrary value.

    Here is the algorithm for the path matching:

      take all MatchPaths paths with the same length as path

      from the first element of the matchpath and the path to the last element:

        take all matchpaths where the current element
        is the same as the element in path

        if there is no matchpath that matches take all
        matchpaths that have a wildcard as current element

        continue the loop with the now smaller list of matchpaths

    The paths are internally stored in a different format in order to make the
    match function efficient. However, the MatchPaths object can be converted
    back to a normal dictionary.

    A path should be a StructuredDataStore - path, see also the documentation
    there.  This object manages a list of paths where each path is mapped to an
    arbitrary object.
    """
    @staticmethod
    def _convert_structure_dict(dict_):
        """convert a structure dict to a path dict.
        """
        def treewalk(d, keylist, subdict):
            """walk the tree."""
            for (k,v) in subdict.items():
                if k==root_key_str:
                    if not keylist:
                        d[root_key_str]= v
                    else:
                        d[StructuredDataStore.join_path(keylist)]= v
                else:
                    treewalk(d, keylist+[k], v)
        d= {}
        treewalk(d, [], dict_)
        return d
    def clone(self, deepcopy= True):
        """clones a MatchPaths object.

        Here is an example:

        >>> d={"#": "top level",
        ...     "a": "top level 'a'",
        ...     "*.*": "level 2, '*.*'",
        ...     "a.*": "level 2, 'a.*'",
        ...   }
        >>> m=MatchPaths(d)
        >>> print(str(m))
        MatchPaths(
          { '#': 'top level',
            '*.*': "level 2, '*.*'",
            'a': "top level 'a'",
            'a.*': "level 2, 'a.*'"}
        )
        >>> shallow= m.clone(False)
        >>> deep= m.clone(True)
        >>> m["*.*"]= "NEW!!"
        >>> print(str(m))
        MatchPaths(
          { '#': 'top level',
            '*.*': 'NEW!!',
            'a': "top level 'a'",
            'a.*': "level 2, 'a.*'"}
        )
        >>> print(str(shallow))
        MatchPaths(
          { '#': 'top level',
            '*.*': 'NEW!!',
            'a': "top level 'a'",
            'a.*': "level 2, 'a.*'"}
        )
        >>> print(str(deep))
        MatchPaths(
          { '#': 'top level',
            '*.*': "level 2, '*.*'",
            'a': "top level 'a'",
            'a.*': "level 2, 'a.*'"}
        )
        """
        new= self.__class__()
        # pylint: disable= protected-access
        if not deepcopy:
            new._data= copy.copy(self._data)
        else:
            new._data= copy.deepcopy(self._data)
        return new
    def __init__(self, spec=None, check_func= None):
        """initialize the object from spec.

        This initializes the object. A python dictionary can be given as an
        optional parameter in order to initialize the object.
        """
        self._data= {}
        self._locked= False
        if spec is not None:
            MatchPaths.add(self, spec, check_func)
    def lock(self):
        """make the MatchPaths object read-only."""
        self._locked= True
    def m_direct_iter(self,
                      pattern= "",
                      length= None,
                      paths_found_set= None):
        r"""walk through all types.

        returns lists of strings. SpecialKey objects are returned as objects.

        IMPORTANT NOTE:
        The keylist returned at each iteration is NOT a new list but the same
        list with a new content at each iteration. If you use this iterator to
        store the keylist somewhere keep in mind that you have to make a
        shallow copy of the keylist like in "my_keylist= keylist[:]".
        Note that list comprehension [x for x in s.m_direct_iter] WILL NOT
        work due to this reason.

        Here are some examples:

        >>> d={"#": "top level",
        ...     "*": "top level, '*'",
        ...     "a": "top level 'a'",
        ...     "*.*": "level 2, '*.*'",
        ...     "a.*": "level 2, 'a.*'",
        ...     "n.*": "level 2, 'n.*",
        ...     "n[2]": "level 2, 'n[2]",
        ...     "a.b.C": "level 3, a.b.C",
        ...     "a.*.c": "level 3, a.*.c",
        ...     "a.*.*": {"mykey": 2 }
        ... }
        >>> m=MatchPaths(d)
        >>> def p(m,pattern,length,pathset=None):
        ...     res= [(p,kl[:],v) for (p,kl,v) in m.m_direct_iter(
        ...                                         pattern,
        ...                                         length= length,
        ...                                         paths_found_set= pathset)]
        ...     res.sort(key= lambda x: x[0])
        ...     print(Repr.repr(res).replace("),","),\n"))

        >>> p(m,"",None)
        [('#', [ROOTKEY], 'top level'),
         ('*', [ANYKEY], "top level, '*'"),
         ('*.*', [ANYKEY, ANYKEY], "level 2, '*.*'"),
         ('a', ['a'], "top level 'a'"),
         ('a.*', ['a', ANYKEY], "level 2, 'a.*'"),
         ('a.*.*', ['a', ANYKEY, ANYKEY], {'mykey': 2}),
         ('a.*.c', ['a', ANYKEY, 'c'], 'level 3, a.*.c'),
         ('a.b.C', ['a', 'b', 'C'], 'level 3, a.b.C'),
         ('n.*', ['n', ANYKEY], "level 2, 'n.*"),
         ('n[2]', ['n', 2], "level 2, 'n[2]")]
        >>> p(m,"",2)
        [('*.*', [ANYKEY, ANYKEY], "level 2, '*.*'"),
         ('a.*', ['a', ANYKEY], "level 2, 'a.*'"),
         ('n.*', ['n', ANYKEY], "level 2, 'n.*"),
         ('n[2]', ['n', 2], "level 2, 'n[2]")]
        >>> p(m,"",5)
        []
        >>> p(m,"",3)
        [('a.*.*', ['a', ANYKEY, ANYKEY], {'mykey': 2}),
         ('a.*.c', ['a', ANYKEY, 'c'], 'level 3, a.*.c'),
         ('a.b.C', ['a', 'b', 'C'], 'level 3, a.b.C')]
        >>> p(m,"a.*",None)
        [('a.*', ['a', ANYKEY], "level 2, 'a.*'")]
        >>> p(m,"a.**",None)
        [('a.*', ['a', ANYKEY], "level 2, 'a.*'"),
         ('a.*.*', ['a', ANYKEY, ANYKEY], {'mykey': 2}),
         ('a.*.c', ['a', ANYKEY, 'c'], 'level 3, a.*.c'),
         ('a.b.C', ['a', 'b', 'C'], 'level 3, a.b.C')]
        >>> p(m,"a.**",2)
        [('a.*', ['a', ANYKEY], "level 2, 'a.*'")]
        >>> p(m,"a.**",3)
        [('a.*.*', ['a', ANYKEY, ANYKEY], {'mykey': 2}),
         ('a.*.c', ['a', ANYKEY, 'c'], 'level 3, a.*.c'),
         ('a.b.C', ['a', 'b', 'C'], 'level 3, a.b.C')]
        >>> p(m,"**",1)
        [('*', [ANYKEY], "top level, '*'"),
         ('a', ['a'], "top level 'a'")]
        >>> p(m,"**",0)
        []
        >>> p(m,"",0)
        [('#', [ROOTKEY], 'top level')]
        >>> pset= set()
        >>> p(m,"a.b.*",None,pset)
        [('a.b.C', ['a', 'b', 'C'], 'level 3, a.b.C')]
        >>> p(m,"a.**",None,pset)
        [('a.*', ['a', ANYKEY], "level 2, 'a.*'"),
         ('a.*.*', ['a', ANYKEY, ANYKEY], {'mykey': 2}),
         ('a.*.c', ['a', ANYKEY, 'c'], 'level 3, a.*.c')]
        """
        # pylint: disable= too-many-locals, too-many-branches, too-many-statements
        def pattern_iterator(val, patternkey):
            """iterator with a given patternkey."""
            # pylint: disable= no-else-return
            if isinstance(patternkey, SpecialKey):
                if patternkey.simple_wildcard():
                    for (k,v) in val.items():
                        if patternkey.match(k):
                            yield (k,v)
                    return
                elif patternkey.recursive_wildcard():
                    for (k,v) in val.items():
                        yield (k,v)
                    return
                else:
                    raise ValueError("unexpected specialkey: %s" % repr(patternkey))
            else:
                try:
                    v= val[patternkey]
                except KeyError:
                    return
                except TypeError:
                    return
                yield (patternkey, v)
                return
        # ---------
        if (not length) and (length!=0):
            lengths= list(self._data.keys())
        else:
            if length not in self._data:
                return
            lengths= [length]
        if pattern:
            pattern_list= StructuredDataStore.split_path(pattern)
            if not pattern_list:
                pattern_list=[]
                pattern_anykeys= True
            else:
                pattern_anykeys= (pattern_list[-1]==ANYKEYS)
            pattern_len= len(pattern_list)
            nl= []
            for l in lengths:
                # pylint: disable= no-else-continue
                if l<pattern_len:
                    continue
                elif (l==pattern_len) or pattern_anykeys:
                    nl.append(l)
            lengths= nl
        else:
            pattern_list=[ANYKEYS]
            pattern_len= len(pattern_list)

        if not lengths:
            return
        #print("LEN:",repr(lengths))

        for l in lengths:
            d= self._data.get(l)
            if d is None:
                raise AssertionError("d is None!")
            if l==0:
                # if l==0 is in lengths, there cannot be
                # a pattern given, so output the ROOTKEY anyway:
                if paths_found_set is None:
                    yield (str(ROOTKEY), [ROOTKEY], d)
                else:
                    if str(ROOTKEY) not in paths_found_set:
                        paths_found_set.add(str(ROOTKEY))
                continue
            depth= 0
            paths=[""]
            keylist= [None]
            pattern_key= pattern_list[depth]
            iterators= [pattern_iterator(d, pattern_key)]
            #print("len",length," iterators:",repr(iterators))
            while iterators:
                try:
                    (k,v)= next(iterators[-1])
                    if k is None:
                        continue # ignore "None" key
                    keylist[-1]= k
                    path= StructuredDataStore.append_path(paths[-1], keylist[-1])
                    #print("(k,v):",repr(keylist),repr(v))
                except StopIteration:
                    iterators.pop()
                    depth-=1
                    if depth>=pattern_len:
                        pattern_key= pattern_list[-1] # can only happen with ANYKEYS
                    else:
                        pattern_key= pattern_list[depth]
                    keylist.pop()
                    paths.pop()
                    continue
                #print("d, (k,v):",depth,repr(k),repr(v))
                if depth+1==l:
                    if paths_found_set is None:
                        yield (path, keylist, v)
                    else:
                        if path not in paths_found_set:
                            yield (path, keylist, v)
                            paths_found_set.add(path)
                elif depth+1<l:
                    depth+=1
                    if depth>=pattern_len:
                        pattern_key= pattern_list[-1] # can only happen with ANYKEYS
                    else:
                        pattern_key= pattern_list[depth]
                    #print("pattern_key:",repr(pattern_key))
                    iterators.append(pattern_iterator(v, pattern_key))
                    keylist.append(None)
                    paths.append(path)
        return # implies StopIteration

    def simple_search(self, path_patterns, length= None, add_values= False):
        r"""search by a given pattern.

        A pattern is a StructuredDataStore path which may contain wildcards.
        A wildcard for a key in a dictionary or a list item is "*".

        Here are some examples:

        >>> d={"#": "top level",
        ...     "*": "top level, '*'",
        ...     "\*": "star",
        ...     "a": "top level 'a'",
        ...     "*.*": "level 2, '*.*'",
        ...     "a.*": "level 2, 'a.*'",
        ...     "n.*": "level 2, 'n.*",
        ...     "n[2]": "level 2, 'n[2]",
        ...     "a.b.C": "level 3, a.b.C",
        ...     "a.*.c": "level 3, a.*.c",
        ...     "a.*.*": {"mykey": 2 }
        ... }
        >>> m=MatchPaths(d)
        >>>
        >>> def test(pattern, length= None):
        ...   Repr.printrepr(sorted(m.simple_search(pattern,length)))

        >>> test("**")
        ['*', '*.*', '\\*', 'a', 'a.*', 'a.*.*', 'a.*.c', 'a.b.C', 'n.*', 'n[2]']
        >>> test("\*")
        ['\\*']
        >>> test("a.**")
        ['a.*', 'a.*.*', 'a.*.c', 'a.b.C']
        >>> test("a.b.**")
        ['a.b.C']
        >>> test("#")
        Traceback (most recent call last):
            ...
        ValueError: unexpected specialkey: ROOTKEY
        >>> test("\#")
        []
        >>> test("*")
        ['*', '\\*', 'a']
        >>> test("*.*")
        ['*.*', 'a.*', 'n.*', 'n[2]']
        >>> test("",0)
        ['#']
        >>> test("a.**")
        ['a.*', 'a.*.*', 'a.*.c', 'a.b.C']
        >>> test("a.**",2)
        ['a.*']
        >>> test("a.**",3)
        ['a.*.*', 'a.*.c', 'a.b.C']
        """
        matched= []
        if not is_iterable(path_patterns):
            if not path_patterns:
                path_patterns= [""]
            else:
                path_patterns= [path_patterns]
            paths_found_set= None
        else:
            paths_found_set= set()
        for pattern in path_patterns:
            for (path,_,val) in self.m_direct_iter(pattern= pattern,
                                                   length=length,
                                                   paths_found_set= paths_found_set):
                if not add_values:
                    matched.append(path)
                else:
                    matched.append((path,val))
        return matched

    def add(self, spec, check_func= None):
        """add paths, spec must be a dict or a list of pairs.

        This method adds paths and values from a given dictionary or a given
        list of pairs. A check function may be provided by the optional
        parameter check_func.  This function is called on each value found in
        the given dictionary or list (note: only for the value, not for the
        path). The user may choose to raise an exception in the check function,
        if a value doesn't match certain criteria.

        Here are some examples:

        >>> m=MatchPaths({"A":"a"})
        >>> m.add({"B.C":"x","D.E":"y"})
        >>> print(m)
        MatchPaths({'A': 'a', 'B.C': 'x', 'D.E': 'y'})
        >>> m=MatchPaths({"A":"a"})
        >>> m.add((("B.C","x"),("D.E","y")))
        >>> print(m)
        MatchPaths({'A': 'a', 'B.C': 'x', 'D.E': 'y'})
        >>> m=MatchPaths({"A":"a"})
        >>> m.add([("B.C","x"),("D.E","y")])
        >>> print(m)
        MatchPaths({'A': 'a', 'B.C': 'x', 'D.E': 'y'})
        >>> m.add({"*": "top wildcard", "A.*" : "a-wildcard", "B.C.*": "BC wildcard"})
        >>> print(m)
        MatchPaths(
          { '*': 'top wildcard',
            'A': 'a',
            'A.*': 'a-wildcard',
            'B.C': 'x',
            'B.C.*': 'BC wildcard',
            'D.E': 'y'}
        )
        """
        if self._locked:
            raise ValueError(("modification of %s failed, "+\
                   "object is locked") % self.__class__.__name__)
        if hasattr(spec, "items"):
            it= list(spec.items())
        elif is_iterable(spec):
            it= spec.__iter__()
        else:
            raise TypeError("spec must be a dict or a list or tuple of pairs.")
        MatchPaths.iterator_add(self, it, check_func)
    def iterator_add(self, iterator, check_func= None):
        """add typespecs from an iterator to the MatchPaths.

        This method adds paths from a iterator. The iterator must provide pairs
        consisting of a path and a value. A check function may be provided by
        the optional parameter check_func. This function is called on each
        value found in the given dictionary or list (note: only for the value,
        not for the path).  The user may choose to raise an exception in the
        check function, if a value doesn't match certain criteria.

        No testcode here since this is implicitly tested by the testcode of
        method "add".
        """
        if self._locked:
            raise ValueError(("modification of %s failed, "+\
                   "object is locked") % self.__class__.__name__)
        d= None
        for (k,v) in iterator:
            if check_func is not None:
                check_func(v)
            if k==root_key_str: # top node type specification
                self._data[0]= v
                continue
            # split the path into single keys:
            keylist= StructuredDataStore.split_path(k)
            # get the dict with Paths of this length:
            d= _get_dict(self._data, len(keylist))
            last= len(keylist)-1
            for i in range(last+1):
                key= keylist[i]
                if isinstance(key, SpecialKey):
                    if not SpecialKey.simple_wildcard(key):
                        raise ValueError(("key '%s' not allowed in type" +\
                                           "path") % str(key))
                    l= _get_list(d, None) # create a new list, add to the
                                          # <None> key. This list defines
                                          # the sort order.
                    _sorted_unique_insert(l, key) # keep this list of
                                                   # Wildcards sorted
                if i<last:
                    d= _get_dict(d, key)
                else:
                    d[key]= v
    def __getitem__(self, path):
        """return the value of a given path.

        Here are some examples:

        >>> d={"#": "top level",
        ...     "*": "top level, '*'",
        ...     "a": "top level 'a'",
        ...     "*.*": "level 2, '*.*'",
        ...     "a.*": "level 2, 'a.*'",
        ...     "n.*": "level 2, 'n.*",
        ...     "n[2]": "level 2, 'n[2]",
        ...     "a.b.C": "level 3, a.b.C",
        ...     "a.*.c": "level 3, a.*.c",
        ...     "a.*.*": "level 3, a.*.*"
        ... }
        >>> m=MatchPaths(d)
        >>> m["#"]
        'top level'
        >>> m["*"]
        "top level, '*'"
        >>> m["a"]
        "top level 'a'"
        >>> m[""]
        >>> m["*.*"]
        "level 2, '*.*'"
        >>> m["a.*"]
        "level 2, 'a.*'"
        >>> m["n.*"]
        "level 2, 'n.*"
        >>> m["n[2]"]
        "level 2, 'n[2]"
        >>> m["a.b.C"]
        'level 3, a.b.C'
        >>> m["a..C"]
        >>> m["a.*.C"]
        >>> m["a.*.*"]
        'level 3, a.*.*'
        >>> m["a.vs.dsd.dsdf"]
        """
        if path==root_key_str:
            return self._data.get(0)
        if path=="":
            return None
        keylist= StructuredDataStore.split_path(path)
        d= self._data.get(len(keylist))
        for k in keylist:
            if not isinstance(d, dict):
                return None
            d= d.get(k)
            if d is None:
                return None
        return d
    def __delitem__(self, path):
        """remove a single path.

        >>> d={"#": 1,
        ...     "a": 2,
        ...     "a.b": 3,
        ...   }
        >>> m=MatchPaths(d)
        >>> Repr.printrepr(m._data)
        {0: 1, 1: {'a': 2}, 2: {'a': {'b': 3}}}
        >>> del m["#"]
        >>> Repr.printrepr(m._data)
        {1: {'a': 2}, 2: {'a': {'b': 3}}}
        >>> m=MatchPaths(d)
        >>> del m["a"]
        >>> Repr.printrepr(m._data)
        {0: 1, 2: {'a': {'b': 3}}}
        >>> m=MatchPaths(d)
        >>> del m["a.b"]
        >>> Repr.printrepr(m._data)
        {0: 1, 1: {'a': 2}}

        >>> d={"#": 1,
        ...     "a": 2,
        ...     "b": 3,
        ...     "a.b": 4,
        ...     "a.c": 5,
        ...   }
        >>> m=MatchPaths(d)
        >>> del m["a"]
        >>> Repr.printrepr(m._data)
        {0: 1, 1: {'b': 3}, 2: {'a': {'b': 4, 'c': 5}}}
        >>> del m["b"]
        >>> Repr.printrepr(m._data)
        {0: 1, 2: {'a': {'b': 4, 'c': 5}}}
        >>> m=MatchPaths(d)
        >>> del m["a.b"]
        >>> Repr.printrepr(m._data)
        {0: 1, 1: {'a': 2, 'b': 3}, 2: {'a': {'c': 5}}}
        >>> del m["a.c"]
        >>> Repr.printrepr(m._data)
        {0: 1, 1: {'a': 2, 'b': 3}}

        >>> d={"#": 1,
        ...     "a.b.c.d": 2,
        ...     "a.b.c.e": 3
        ...   }
        >>> m=MatchPaths(d)
        >>> del m["a.b.c.e"]
        >>> Repr.printrepr(m._data)
        {0: 1, 4: {'a': {'b': {'c': {'d': 2}}}}}
        >>> del m["a.b.c.d"]
        >>> Repr.printrepr(m._data)
        {0: 1}

        >>> d={"#": 1,
        ...     "a.b.*.d": 2,
        ...     "a.b.*.e": 3
        ...   }
        >>> m=MatchPaths(d)
        >>> Repr.printrepr(m._data)
        {0: 1, 4: {'a': {'b': {None: [ANYKEY], ANYKEY: {'d': 2, 'e': 3}}}}}
        >>> del m["a.b.*.d"]
        >>> Repr.printrepr(m._data)
        {0: 1, 4: {'a': {'b': {None: [ANYKEY], ANYKEY: {'e': 3}}}}}
        >>> del m["a.b.*.e"]
        >>> Repr.printrepr(m._data)
        {0: 1}
        """
        if self._locked:
            raise ValueError(("modification of %s failed, "+\
                   "object is locked") % self.__class__.__name__)
        if path==root_key_str:
            if 0 not in self._data:
                raise KeyError("path %s not found" % path)
            del self._data[0]
            return
        keylist= StructuredDataStore.split_path(path)
        last_key= len(keylist)-1
        def _del(dict_,index):
            """recursive delete.
            returns False when the recursive delete should stop.
            """
            key= keylist[index]
            val= dict_[key]
            if index<last_key:
                if not _del(val, index+1):
                    return False
            if isinstance(key, SpecialKey):
                lst= dict_[None]
                lst.remove(key)
                if not lst:
                    del dict_[None]
            del dict_[key]
            return len(dict_)<=0
        l= len(keylist)
        _del(self._data[l], 0)
        if not self._data[l]:
            del self._data[l]

    def __setitem__(self, key, val):
        """add a single new path.

        This method adds a single path and value to the MatchPaths object. It
        is implicitly used in a statement like this "matchpathobject[path]=
        value".
        """
        self.add( ((key,val),) )
    def match(self, path, return_matchpath= False):
        """match a path in the MatchPaths.

        This method returns the value of the path in the MatchPaths object that
        matches the given path best.

        Here are some examples:

        >>> d={"#": "top level",
        ...     "*": "top level, '*'",
        ...     "a": "top level 'a'",
        ...     "*.*": "level 2, '*.*'",
        ...     "a.*": "level 2, 'a.*'",
        ...     "n.*": "level 2, 'n.*",
        ...     "n[2]": "level 2, 'n[2]",
        ...     "a.b.C": "level 3, a.b.C",
        ...     "a.*.c": "level 3, a.*.c",
        ...     "a.*.*": "level 3, a.*.*"
        ... }

        >>> m=MatchPaths(d)
        >>> m.match("#")
        'top level'
        >>> m.match("abc")
        "top level, '*'"
        >>> m.match("a")
        "top level 'a'"
        >>> m.match("x.y")
        "level 2, '*.*'"
        >>> m.match("a.y")
        "level 2, 'a.*'"
        >>> m.match("a.y.c")
        'level 3, a.*.c'
        >>> m.match("a.b.c")
        'level 3, a.*.c'
        >>> m.match("a.b.C")
        'level 3, a.b.C'
        >>> m.match("a.x.y")
        'level 3, a.*.*'
        >>> m.match("n[2]")
        "level 2, 'n[2]"
        >>> m.match("n[0]")
        "level 2, 'n.*"
        >>> m.match("x.y.z")
        >>> m=MatchPaths(d)
        >>> m.match("#",True)
        ('#', 'top level')
        >>> m.match("abc",True)
        ('*', "top level, '*'")
        >>> m.match("x.y",True)
        ('*.*', "level 2, '*.*'")
        >>> m.match("a.b.c",True)
        ('a.*.c', 'level 3, a.*.c')
        >>> m.match("a.b.C",True)
        ('a.b.C', 'level 3, a.b.C')
        >>> m.match("n[2]",True)
        ('n[2]', "level 2, 'n[2]")
        >>> m.match("n[0]",True)
        ('n.*', "level 2, 'n.*")
        """
        def walk(last, matchkeys, keylist, index, dct):
            """walk the tree."""
            val= dct.get(keylist[index])
            if val is not None:
                if index==last:
                    return val
                # here val is another dictionary:
                val= walk(last, matchkeys, keylist, index+1, val)
                if val is not None:
                    # the recursively called walk has found something:
                    return val
                # the recursively called walk has found nothing from here
            wildcards= dct.get(None)
            if wildcards is None:
                # no wildcards here
                return None
            for w in wildcards:
                if w.match(keylist[index]):
                    matchkeys[index]= w
                    val= dct[w]
                    if index==last:
                        return val
                    # here val is another dictionary:
                    val= walk(last, matchkeys, keylist, index+1, val)
                    if val is not None:
                        # the recursively called walk has found something:
                        return val
                    matchkeys[index]= keylist[index]
                    # the recursively called walk has found nothing from here
            return None
        # def. of function "walk" ends here
        # ---------------------------------
        if path==root_key_str:
            # pylint: disable= no-else-return
            if not return_matchpath:
                return self._data.get(0)
            else:
                return (root_key_str, self._data.get(0))
        keylist= StructuredDataStore.split_path(path)
        # keylist may contain strings and integers
        # now get the dictionary with paths keylists of this length:
        last= len(keylist)-1
        d= self._data.get(len(keylist))
        if d is None:
            return None
        matchkeys= keylist[:]
        # pylint: disable= no-else-return
        if not return_matchpath:
            return walk(last, matchkeys, keylist, 0, d)
        else:
            res= walk(last, matchkeys, keylist, 0, d)
            return (StructuredDataStore.join_path(matchkeys), res)
    def as_path_dict(self):
        """convert the MatchPaths object to a dictionary.

        This method returns a dictionary than contains all the data of the
        MatchPaths object.

        Here is an example:

        >>> d={"#": "top level",
        ...     "*": "top level, '*'",
        ...     "a": "top level 'a'",
        ...     "*.*": "level 2, '*.*'",
        ...     "a.*": "level 2, 'a.*'",
        ...     "a.*.b": "level 3, a.*.b",
        ...     "a.*.*": "level 3, a.*.*"
        ...   }
        >>> m=MatchPaths(d)
        >>> Repr.printnice(m.as_path_dict(), 0)
        {
          '#': 'top level',
          '*': "top level, '*'",
          '*.*': "level 2, '*.*'",
          'a': "top level 'a'",
          'a.*': "level 2, 'a.*'",
          'a.*.*': 'level 3, a.*.*',
          'a.*.b': 'level 3, a.*.b'
        }
        """
        return { p: v for (p,_,v) in self.m_direct_iter() }
    def __repr__(self):
        """returns a python expression of the object.

        Here is an example:

        >>> d={"#":"a","*":"b","a.*.c":"c"}
        >>> m=MatchPaths(d)
        >>> repr(m)
        "MatchPaths({'#': 'a', '*': 'b', 'a.*.c': 'c'})"
        """
        spec= self.as_path_dict()
        return "%s(%s)" % (self.__class__.__name__,Repr.repr(spec))
    def __str__(self):
        """print(the object as a human readable string.)

        Here is an example:

        >>> d={"#": "top level",
        ...     "*": "top level, '*'",
        ...     "*.*": "level 2, '*.*'",
        ...     "a.*": "level 2, 'a.*'",
        ...     "a.*.b": "level 3, a.*.b",
        ...     "a.*.*": "level 3, a.*.*"
        ...   }
        >>> m=MatchPaths(d)
        >>> print(str(m))
        MatchPaths(
          { '#': 'top level',
            '*': "top level, '*'",
            '*.*': "level 2, '*.*'",
            'a.*': "level 2, 'a.*'",
            'a.*.*': 'level 3, a.*.*',
            'a.*.b': 'level 3, a.*.b'}
        )
        """
        spec= self.as_path_dict()
        lines= ["%s(" % self.__class__.__name__]
        l= pprint.pformat(spec, indent=2, width=70).split("\n")
        if len(l)==1:
            return "%s(%s)" % (self.__class__.__name__,l[0])
        l[-1]+="\n)"
        lines.extend(l)
        return "\n  ".join(lines)


class StructuredDataTypes(MatchPaths):
    """a collection of type specifications for a number of paths.

    This class provides a store for paths and associated type specifications.

    It is a derivative of MatchPaths. For each path a typespec is specified. A
    typespec must be understandable by check_type_scalar.
    """
    @staticmethod
    def _check_func(spec):
        spec.check(None, dry_run= True)
    @staticmethod
    def _iterator_convert_spec(spec_iterator):
        """convert SD specifications to SingleTypeSpec."""
        for (k,v) in spec_iterator:
            yield (k, SingleTypeSpec(v))
    @staticmethod
    def _convert_spec(path_type_decl):
        """convert SD specifications to SingleTypeSpec."""
        if path_type_decl is None:
            return None
        return dict( StructuredDataTypes._iterator_convert_spec(\
                            list(path_type_decl.items())) )

    def __init__(self, path_type_decl=None):
        """initialize the object from path_type_decl.

        This initializes the object. A python dictionary can be given as an
        optional parameter in order to initialize the object. The dictionary
        should map paths to type specifications.

        Here is an example:

        >>> t=StructuredDataTypes({"":"integer","*":"map","a.*":"list"})
        >>> t=StructuredDataTypes({"":"integer","*":"map","a.*":"listx"})
        Traceback (most recent call last):
            ...
        ValueError: unknown typespec: "listx"

        """
        MatchPaths.__init__(self,
                            StructuredDataTypes._convert_spec(path_type_decl),
                            StructuredDataTypes._check_func)
    def add(self, spec, check_func= None):
        """add paths and type specifications.

        This method adds paths and type specifications from a given dictionary
        or a given list of pairs.

        Here are some examples:

        >>> t=StructuredDataTypes({"":"integer","*":"map","a.*":"list"})
        >>> t.add({"b":"integer","c.d":"real"})
        >>> t.add({"x":"blah"})
        Traceback (most recent call last):
            ...
        ValueError: unknown typespec: "blah"
        """
        if check_func is None:
            check_func= StructuredDataTypes._check_func
        MatchPaths.add(self, StructuredDataTypes._convert_spec(spec), check_func)
    def iterator_add(self, iterator, check_func= None):
        """add paths and type specifications from an iterator.

        This method adds paths and type specifications from a iterator. The
        iterator must provide pairs of a path and a type specification.

        Here are some examples:

        >>> t=StructuredDataTypes({"":"integer","*":"map","a.*":"list"})
        >>> t.iterator_add({"b":"integer","c.d":"real"}.items())
        >>> t.iterator_add({"x":"blah"}.items())
        Traceback (most recent call last):
            ...
        ValueError: unknown typespec: "blah"
        """
        if check_func is None:
            check_func= StructuredDataTypes._check_func
        MatchPaths.iterator_add(self,\
                  StructuredDataTypes._iterator_convert_spec(iterator),\
                  check_func)
    def __getitem__(self,path):
        """get a single item of the StructuredDataTypes.

        This method returns a type declaration for a given path. By this you
        can used the StructuredDataTypes object like this:
        "structureddatatypes[path]".

        Here are some examples:

        >>> t=StructuredDataTypes({"#":"integer","*":"map","a.*":"list"})
        >>> t["#"]
        SingleTypeSpec('integer')
        >>> t["*"]
        SingleTypeSpec('map')
        >>> t["a.*"]
        SingleTypeSpec('list')
        >>> print(t["a.b"])
        None
        """
        return MatchPaths.__getitem__(self,path)

    def as_path_dict(self):
        """return the object as a dict.

        Here is an example:

        >>> t=StructuredDataTypes({"#":"integer","*":"map","a.*":"list"})
        >>> Repr.printrepr(t.as_path_dict())
        {'#': 'integer', '*': 'map', 'a.*': 'list'}
        """
        d= MatchPaths.as_path_dict(self)
        for (k,v) in d.items():
            d[k]= v.to_dict() # v is a SingleTypeSpec object
        return d
    def check(self, path, value):
        """typecheck a value for a given path.

        This method takes a path and a value. It then searches the object for a
        matching path and checks the value against the type specification
        associated with the found path. If the typecheck fails, it raises an
        exception.

        Here are some examples:

        >>> d={"#": {"optional_struct":["a","b"]},
        ...     "a": {"typed_map":"integer"},
        ...     "b": "map",
        ...     "b.*": {"typed_list":"string"},
        ...     "n[0]": "string",
        ...     "n.*": "integer",
        ...   }
        >>> t= StructuredDataTypes(d)
        >>> t.check("#", {"a":1})
        >>> t.check("#", {"a":1})
        >>> t.check("#", {"a":0,"b":1})
        >>> t.check("#", {"a":0,"b":1,"c":2})
        Traceback (most recent call last):
            ...
        TypeError: key c not in list of allowed keys
        >>> t.check("a", {1:"x",2:"y"})
        >>> t.check("a", {1:"x",2:"y","z":"zz"})
        Traceback (most recent call last):
            ...
        TypeError: integer expected, got: 'z'
        >>> t.check("a", 2)
        Traceback (most recent call last):
            ...
        TypeError: map expected
        >>> t.check("b", {"y":1, 2:"a"})
        >>> t.check("b", [1,2])
        Traceback (most recent call last):
            ...
        TypeError: map expected
        >>> t.check("b.x", ["a","b"])
        >>> t.check("b.x", ["a","b",3])
        Traceback (most recent call last):
            ...
        TypeError: string expected, got: 3
        >>> t.check("b.x", 2)
        Traceback (most recent call last):
            ...
        TypeError: list expected

        >>> t.check("n[0]", "ab")
        >>> t.check("n[0]", 2)
        Traceback (most recent call last):
            ...
        TypeError: string expected, got: 2
        >>> t.check("n[1]", 2)
        >>> t.check("n[1]", "a")
        Traceback (most recent call last):
            ...
        TypeError: integer expected, got: 'a'
        """
        t= self.match(path)
        if t is None:
            return
        t.check(value)


class StructuredDataContainer():
    """This is a simple container that can hold a StructuredDataStore,
    StructuredDataTypes or both. A StructuredDataContainer is a map that always
    has the key "**SDC-Metadata** and the optional keys "**SDC-Store**" and
    "**SDC-Types**".

    SDC-Metadata:
        This is a simple map that contains information on the format used.
        Currently it has only one key, "version" which has as value the current
        version number of the format as a string. As of the writing of this
        document, the current version is "1.0".

    SDC-Store:
        This is the StructuredDataStore map.

    SDC-Types:
        This is the StructuredDataTypes map.
    """

    MetaDataTag="**SDC-Metadata**"
    DataTag    ="**SDC-Store**"
    TypeTag    ="**SDC-Types**"
    Version    ="1.0"
    def _meta_check(self, initializer, change_meta= False):
        """initialize the meta-data part."""
        SDC= StructuredDataContainer
        if not isinstance(initializer, dict):
            raise TypeError("initializer must be a dict")
        _meta= initializer.get(SDC.MetaDataTag)
        if _meta is None:
            raise ValueError("the key %s is missing in the dict" % \
                              SDC.MetaDataTag)
        version= _meta.get("version")
        if version is None:
            raise ValueError("the version number is missing in the metadata")
        if version!=SDC.Version:
            raise ValueError(("wrong version of data format, " + \
                               "found: %s  expected: %s") %\
                               (_meta[SDC.Version],SDC.Version))
        if change_meta:
            self._meta= _meta.copy() # shallow copy !!

    def pickle(self, filename):
        """write StructuredDataContainer pickled."""
        stream= open(filename, 'w')
        _pickle_write(stream, self.as_dict())
        stream.close()
    @staticmethod
    def unpickle(filename):
        """load from pickled data."""
        stream= open(filename, 'r')
        dict_= pickle.load(stream)
        stream.close()
        return StructuredDataContainer(dict_)
    @staticmethod
    def from_yaml_file(filename):
        """create a StructuredDataContainer from a yaml file.

        Does also lock the file during reading.
        """
        if use_lockfile:
            lk= lock.MyLock(filename, timeout= FILE_LOCK_TIMEOUT)
            try:
                lk.lock()
            except (lock.LockedError, lock.AccessError,
                    lock.NoSuchFileError, OSError) as e:
                raise AssertionError(("file locking of file %s failed with error %s, "+\
                       "you may try to manually remove the lockfile") % \
                       (filename, repr(e)))
        try:
            dict_= _read_cached(filename, myyaml.read_file)
        finally:
            if use_lockfile:
                lk.unlock()
        return StructuredDataContainer(dict_)
    @staticmethod
    def from_yaml_string(st):
        """create a StructuredDataContainer from a yaml file.
        """
        dict_= myyaml.read_string(st)
        return StructuredDataContainer(dict_)
    def clone(self, deepcopy= True):
        """clones a StructuredDataContainer object.

        Here is an example:

        >>> d= {"**SDC-Metadata**": {"version": "1.0" },
        ...      "**SDC-Store**"   : {"a": {"x":1, "y":2 }, "b":10 },
        ...      "**SDC-Types**"   : {"#": {"typed_map": "string"} }
        ...    }
        >>> t= StructuredDataContainer(d)
        >>> shallow= t.clone(False)
        >>> deep   = t.clone(True)
        >>> t.store()["a.y"]= "NEW"
        >>> t.store().setitem("a.z", "ADDED", True)
        >>> print(t)
        StructuredDataContainer(
          {'**SDC-Metadata**': {'version': '1.0'}},
          StructuredDataStore({'a': {'x': 1, 'y': 'NEW', 'z': 'ADDED'}, 'b': 10}),
          StructuredDataTypes({'#': {'typed_map': 'string'}})
          )
        >>> print(shallow)
        StructuredDataContainer(
          {'**SDC-Metadata**': {'version': '1.0'}},
          StructuredDataStore({'a': {'x': 1, 'y': 'NEW', 'z': 'ADDED'}, 'b': 10}),
          StructuredDataTypes({'#': {'typed_map': 'string'}})
          )
        >>> print(deep)
        StructuredDataContainer(
          {'**SDC-Metadata**': {'version': '1.0'}},
          StructuredDataStore({'a': {'x': 1, 'y': 2}, 'b': 10}),
          StructuredDataTypes({'#': {'typed_map': 'string'}})
          )
        """
        new= StructuredDataContainer()
        # pylint: disable= protected-access
        if not deepcopy:
            new._meta= copy.copy(self._meta)
        else:
            new._meta= copy.deepcopy(self._meta)
        if self._data is not None:
            new._data= self._data.clone(deepcopy)
        if self._types is not None:
            new._types= self._types.clone(deepcopy)
        return new
    def __init__(self, dict_= None):
        """initialize the PortableStructuredData object.

        This method initializes the object. The parameter initializer may be
        used to initialize the object from a dictionary. The dictionary must
        have at least the key "**SDC-Metadata**" which must refer to a
        dictionary with the key "version" which must refer to a version number
        string. Optionally the dictionary may have the key "**SDC-Store**"
        which must refer to a dictionary with the StructuredDataStore data. It
        also may have the key "**SDC-Types**" which must refer to a dictionary
        with StructuredDataTypes data in it.

        >>> d= {"**SDC-Metadata**": {"version": "1.0" },
        ...      "**SDC-Store**"   : {"a":1, "b":2 },
        ...      "**SDC-Types**"   : {"#": {"typed_map": "string"} }
        ...    }
        >>> t= StructuredDataContainer(d)
        >>> d= {"**SDC-Metadata**": {"version": "1.0" },
        ...      "**SDC-Store**"    : {"a":1, "b":2 },
        ...    }
        >>> t= StructuredDataContainer(d)
        >>> d= {"**SDC-Metadata**": {"version": "1.0" },
        ...      "**SDC-Types**"   : {"#": {"typed_map": "string"} }
        ...    }
        >>> t= StructuredDataContainer(d)
        >>> d= {"**SDC-Metadata**": {"version": "1.0" },
        ...    }
        >>> t= StructuredDataContainer(d)
        >>> d= {"**SDC-Store**"    : {"a":1, "b":2 },
        ...      "**SDC-Types**"   : {"#": {"typed_map": "string"} }
        ...    }
        >>> t= StructuredDataContainer(d)
        Traceback (most recent call last):
        ...
        ValueError: the key **SDC-Metadata** is missing in the dict
        """
        SDC= StructuredDataContainer
        if dict_ is None:
            self._meta= {"version" : SDC.Version }
            self._data= None
            self._types= None
            return
        self._meta_check(dict_, True)
        self._data=  dict_.get(SDC.DataTag)
        if self._data is not None:
            self._data= StructuredDataStore(self._data)
        self._types= dict_.get(SDC.TypeTag)
        if self._types is not None:
            self._types= StructuredDataTypes(self._types)
    def lock(self):
        """make the StructuredDataContainer read-only."""
        self._data.lock()
        self._types.lock()
    def add(self, dict_):
        """add data to the StructuredDataContainer from a dict.

        This method adds new data to the StructuredDataContainer object. The
        data provided to this method must be a dictionary with two optional
        keys, "**SDC-Store**" and "**SDC-Types**".  The data referenced by
        "**SDC-Store**" is added to the internal StructuredDataStore object.
        The data referenced by "**SDC-Types**" is added to the internal
        StructuredDataTypes object.

        Here is an example:

        >>> t= StructuredDataContainer({"**SDC-Metadata**": {"version": "1.0" },
        ...                             "**SDC-Store**":
        ...                               {"a": {"x": 1 } },
        ...                             "**SDC-Types**":
        ...                               {"a.x" : "integer" }
        ...                            }
        ...                           )
        >>>
        >>> print(t)
        StructuredDataContainer(
          {'**SDC-Metadata**': {'version': '1.0'}},
          StructuredDataStore({'a': {'x': 1}}),
          StructuredDataTypes({'a.x': 'integer'})
          )
        >>>
        >>> t.add({"**SDC-Metadata**": {"version": "1.0" },
        ...        "**SDC-Store**":
        ...           {"a": {"y": 2.0 } },
        ...       }
        ...      )
        >>>
        >>> print(t)
        StructuredDataContainer(
          {'**SDC-Metadata**': {'version': '1.0'}},
          StructuredDataStore({'a': {'x': 1, 'y': 2.0}}),
          StructuredDataTypes({'a.x': 'integer'})
          )
        >>>
        >>> t.add({"**SDC-Metadata**": {"version": "1.0" },
        ...        "**SDC-Types**":
        ...           {"a.y" : "real" }
        ...       }
        ...      )
        >>> print(t)
        StructuredDataContainer(
          {'**SDC-Metadata**': {'version': '1.0'}},
          StructuredDataStore({'a': {'x': 1, 'y': 2.0}}),
          StructuredDataTypes({'a.x': 'integer', 'a.y': 'real'})
          )
        """
        SDC= StructuredDataContainer
        self._meta_check(dict_, True)
        _data=  dict_.get(SDC.DataTag)
        if _data is not None:
            if self._data is None:
                self._data= StructuredDataStore(_data)
            else:
                self._data.add(_data)
        _types= dict_.get(SDC.TypeTag)
        if _types is not None:
            if self._types is None:
                self._types= StructuredDataTypes(_types)
            else:
                self._types.add(_types)
    def add_yaml_string(self, st):
        """add data to the StructuredDataContainer from a yaml string.
        """
        dict_= myyaml.read_string(st)
        self.add(dict_)
    def add_yaml_file(self, filename):
        """add data to the StructuredDataContainer from a yaml file.
        """
        dict_= myyaml.read_file(filename)
        self.add(dict_)
    def as_dict(self):
        r"""return the object as a dictionary.

        This method returns a dictionary that contains all the information of
        the StructuredDataContainer object.

        Here is an example:

        >>> d= {"**SDC-Metadata**": {"version": "1.0" },
        ...      "**SDC-Store**"    : {"a":1, "b":2 },
        ...      "**SDC-Types**"   : {"#": {"typed_map": "string"} }
        ...    }
        >>> t= StructuredDataContainer(d)
        >>> print(Repr.repr(t.as_dict()).replace("},","},\n"))
        {'**SDC-Metadata**': {'version': '1.0'},
         '**SDC-Store**': {'a': 1, 'b': 2},
         '**SDC-Types**': {'#': {'typed_map': 'string'}}}
        """
        SDC= StructuredDataContainer
        d= { SDC.MetaDataTag: self._meta }
        if self._data is not None:
            d[SDC.DataTag]= self._data.as_dict()
        if self._types is not None:
            d[SDC.TypeTag]= self._types.as_path_dict()
        return d
    # pylint: disable= line-too-long
    def __repr__(self):
        """return a python expression representing the object.

        Here is an example:

        >>> d= {"**SDC-Metadata**": {"version": "1.0" },
        ...      "**SDC-Store**"    : {"a":1, "b":2 },
        ...      "**SDC-Types**"   : {"#": {"typed_map": "string"} }
        ...    }
        >>> t= StructuredDataContainer(d)
        >>> print(repr(t))
        StructuredDataContainer({'**SDC-Metadata**': {'version': '1.0'}, '**SDC-Store**': {'a': 1, 'b': 2}, '**SDC-Types**': {'#': {'typed_map': 'string'}}})

        """
        return "StructuredDataContainer(%s)" % Repr.repr(self.as_dict())
    # pylint: enable= line-too-long
    def __str__(self):
        """return a more human readable representation of the object.

        Here is an example:

        >>> d= {"**SDC-Metadata**": {"version": "1.0" },
        ...      "**SDC-Store**"    : {"a":1, "b":2 },
        ...      "**SDC-Types**"   : {"#": {"typed_map": "string"} }
        ...    }
        >>> t= StructuredDataContainer(d)
        >>> print(t)
        StructuredDataContainer(
          {'**SDC-Metadata**': {'version': '1.0'}},
          StructuredDataStore({'a': 1, 'b': 2}),
          StructuredDataTypes({'#': {'typed_map': 'string'}})
          )
        """
        SDC= StructuredDataContainer
        lines= ["StructuredDataContainer("]
        d= { SDC.MetaDataTag: self._meta }
        l= pprint.pformat(d, indent=2, width=70).split("\n")
        l[-1]+= ","
        if self._data is not None:
            l.extend( str(self._data).splitlines() )
        if self._types is not None:
            if self._data is not None:
                l[-1]+= ","
            l.extend( str(self._types).splitlines() )
        lines.extend(l)
        lines.append(")")
        return "\n  ".join(lines)
    def as_yaml_string(self):
        """return the StructuredDataContainer as a yaml string.
        """
        return myyaml.write_string(self.as_dict())
    def as_yaml_file(self, filename):
        """return the StructuredDataContainer as a yaml file.

        Does also lock the file during writing.
        """
        if use_lockfile:
            lk= lock.MyLock(filename, timeout= FILE_LOCK_TIMEOUT)
            try:
                lk.lock()
            except (lock.LockedError, lock.AccessError,
                    lock.NoSuchFileError, OSError) as e:
                raise AssertionError(("file locking of file %s failed with error %s, "+\
                       "you may try to manually remove the lockfile") % \
                       (filename, e))
        try:
            dict_= self.as_dict()
            myyaml.write_file(filename, dict_)
            _write_cache_file(filename, dict_)
        finally:
            if use_lockfile:
                lk.unlock()
    def store(self):
        """return the StructuredDataStore contained in the object."""
        return self._data
    def clear_store(self):
        """remove the StructuredDataStore object."""
        self._data= None
    def set_store(self, data):
        """set the StructuredDataStore in the object."""
        # allow setting the store to <None>:
        if data is not None:
            if not isinstance(data, StructuredDataStore):
                raise TypeError("data must be of class StructuredDataStore")
        self._data= data
    def types(self):
        """return the StructuredDataTypes contained in the object."""
        return self._types
    def clear_types(self):
        """remove the StructuredDataTypes."""
        self._types= None
    def set_types(self, types_):
        """set the StructuredDataTypes contained in the object."""
        # allow setting the types to <None>:
        if types_ is not None:
            if not isinstance(types_, StructuredDataTypes):
                raise TypeError("types must be of class StructuredDataTypes")
        self._types= types_
    def meta(self):
        """return the metadata dictionary of the object."""
        return self._meta
    def typecheck(self, other=None):
        """perform a typecheck on the data.

        This method performs a typecheck on the contained StructuredDataStore.
        If there is also a StructuredDataTypes object in the container, this is
        used for the typechecks. Otherwise, the parameter "other" is used to
        retrieve type check information. This parameter may either be a
        StructuredDataTypes object or a StructuredDataContainer with embedded
        StructuredDataTypes.

        parameters:

        other
          This optional parameter is used to provide the type checking
          information. If this parameter is omitted, the function looks for
          type checking information embedded in the StructuredDataContainer. If
          it is not found there either, an AssertionError is raised. The
          parameter may be a StructuredDataTypes object or a
          StructuredDataContainer object with embeeded type checking
          information.

        Here are some examples:

        >>> d= {"**SDC-Metadata**": {"version": "1.0" },
        ...      "**SDC-Store**" : {"a":1, "b":2 },
        ...      "**SDC-Types**": {"#": {"typed_map": "string"} }
        ...    }
        >>> t= StructuredDataContainer(d)
        >>> t.typecheck()
        >>> d= {"**SDC-Metadata**": {"version": "1.0" },
        ...      "**SDC-Store**" : { 2  :1, "b":2 },
        ...      "**SDC-Types**": {"#": {"typed_map": "string"} }
        ...    }
        >>> t= StructuredDataContainer(d)
        >>> t.typecheck()
        Traceback (most recent call last):
            ...
        TypeError: error at path "#": string expected, got: 2
        """
        def do_check(types_, path, value):
            """do the check."""
            try:
                types_.check(path, value)
            except TypeError as e:
                raise TypeError("error at path \"%s\": %s" % (path, str(e)))
            except AssertionError as e:
                raise AssertionError("error at path \"%s\": %s" % (path, str(e)))
        if self._data is None:
            return
        if other is None:
            if self._types is None:
                raise AssertionError("This StructuredDataContainer has to type definitions")
            types_= self._types
        elif isinstance(other, StructuredDataTypes):
            types_= other
        elif isinstance(other, StructuredDataContainer):
            types_= other.types()
            if not isinstance(types_, StructuredDataTypes):
                raise ValueError("other object contains to typechecks")
        else:
            raise TypeError("other object has wrong type %s" % type(other))
        do_check(types_, root_key_str, self._data.as_dict())
        for (path,_,value) in self._data.universal_iter(patterns="",
                                                        path_list= None,
                                                        only_leaves=False,
                                                        sorted_= False,
                                                        show_links= False):
            do_check(types_, path, value)


def _test():
    # pylint: disable= import-outside-toplevel
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
