"""Utilities for dictionaries."""

__version__="5.1" #VERSION#

from StructuredData.internal import Repr

assert __version__==Repr.__version__

# ---------------------------------------------------------
# add values to structured data

# pylint: disable=invalid-name

_struct_add_DICT= 1
_struct_add_LIST= 2
_struct_add_SCALAR= 3

_struct_add_names= { _struct_add_DICT: "dict",
                     _struct_add_LIST: "list",
                     _struct_add_SCALAR: "scalar"
                   }

def _struct_add_type(v):
    if isinstance(v,dict):
        return _struct_add_DICT
    if isinstance(v,list):
        return _struct_add_LIST
    if isinstance(v,int):
        return _struct_add_SCALAR
    if isinstance(v,float):
        return _struct_add_SCALAR
    if isinstance(v,str):
        return _struct_add_SCALAR
    raise AssertionError("unsupported type in var: %s" % repr(v))

def struct_add(dest, src):
    """add to a dict by extending each sub-dict.

    Note: lists are always appended.

    Here are some examples:
    >>> import pprint
    >>> a={ "A":1, "B":[1,2,3], "C": { "x": 2, "y": 3}}
    >>> struct_add(a, {"D":2})
    >>> pprint.pprint(a)
    {'A': 1, 'B': [1, 2, 3], 'C': {'x': 2, 'y': 3}, 'D': 2}
    >>> struct_add(a, {"B":2})
    Traceback (most recent call last):
        ...
    AssertionError: incompatible types: [1, 2, 3](list) 2(scalar)
    >>> struct_add(a, {"B":[3,4]})
    >>> pprint.pprint(a)
    {'A': 1, 'B': [1, 2, 3, 4], 'C': {'x': 2, 'y': 3}, 'D': 2}
    >>> struct_add(a, {"C":[3,4]})
    Traceback (most recent call last):
        ...
    AssertionError: incompatible types: {'x': 2, 'y': 3}(dict) [3, 4](list)
    >>> struct_add(a, {"C":{"z":4,"y":4}})
    >>> pprint.pprint(a)
    {'A': 1, 'B': [1, 2, 3, 4], 'C': {'x': 2, 'y': 4, 'z': 4}, 'D': 2}
    >>> a=[1,2]
    >>> struct_add(a,[3,4])
    >>> pprint.pprint(a)
    [1, 2, 3, 4]
    >>> a=[{"a":1,"b":2}, {"x":10,"y":11}]
    >>> struct_add(a,[{"c":3}])
    >>> pprint.pprint(a)
    [{'a': 1, 'b': 2}, {'x': 10, 'y': 11}, {'c': 3}]
    """
    dest_tp= _struct_add_type(dest)
    src_tp = _struct_add_type(src)
    if dest_tp!=src_tp:
        raise AssertionError("incompatible types: %s(%s) %s(%s)" %\
                              (Repr.repr(dest),_struct_add_names[dest_tp],
                               Repr.repr(src),_struct_add_names[src_tp]))
    if dest_tp==_struct_add_DICT:
        for (k,v) in src.items():
            existing= dest.get(k)
            if existing is None:
                dest[k]= v
                continue
            if _struct_add_type(existing)==_struct_add_SCALAR:
                if _struct_add_type(v)==_struct_add_SCALAR:
                    dest[k]=v
                else:
                    raise AssertionError("incompatible types: %s(%s) %s(%s)" %\
                              (Repr.repr(existing),_struct_add_names[_struct_add_type(existing)],
                               Repr.repr(v),_struct_add_names[_struct_add_type(v)]))
                continue
            struct_add(existing,v)
            continue
    elif dest_tp==_struct_add_LIST:
        for v in src:
            if v in dest:
                continue
            dest.append(v)
    else:
        raise AssertionError("shouldn't happen: %s(%s) %s(%s)" %\
                              (dest,_struct_add_names[dest_tp],
                               src,_struct_add_names[src_tp]))

# ---------------------------------------------------------
# add values to lists

def list_add(l, index, value, default= None):
    """set a value in a list and extend it if necessary.

    Here are some examples:
    >>> l=[]
    >>> list_add(l, 3, "A", "empty")
    >>> l
    ['empty', 'empty', 'empty', 'A']
    >>> list_add(l, 1, "B", "empty")
    >>> l
    ['empty', 'B', 'empty', 'A']
    """
    if len(l)<=index:
        l.extend([default]*(index-len(l)+1))
    l[index]= value

# ---------------------------------------------------------
# get values from lists

def list_get(l, index):
    """get an item from a list, returns None if the list is not long enough.
    """
    if len(l)<=index:
        return None
    return l[index]

# ---------------------------------------------------------
# get values from structured data

def struct_keylist_get(s, keylist):

    """find an element in a structure.

    Here are some examples:
    >>> import pprint
    >>> d= {'A': {'B': {'C': 'val'},
    ...           'b': {'C': 'val2',
    ...                 'D': [None, None, {'X': 'val4'}, 'val3']
    ...                }
    ...          }
    ...    }
    >>> pprint.pprint(struct_keylist_get(d, ["A"]))
    {'B': {'C': 'val'},
     'b': {'C': 'val2', 'D': [None, None, {'X': 'val4'}, 'val3']}}
    >>> pprint.pprint(struct_keylist_get(d, ["A","B"]))
    {'C': 'val'}
    >>> pprint.pprint(struct_keylist_get(d, ["A","b"]))
    {'C': 'val2', 'D': [None, None, {'X': 'val4'}, 'val3']}
    >>> pprint.pprint(struct_keylist_get(d, ["A","b","C"]))
    'val2'
    >>> pprint.pprint(struct_keylist_get(d, ["A","b","D"]))
    [None, None, {'X': 'val4'}, 'val3']
    >>> pprint.pprint(struct_keylist_get(d, ["A","b","D",2]))
    {'X': 'val4'}
    >>> pprint.pprint(struct_keylist_get(d, ["A","b","D",3]))
    'val3'
    """
    try:
        for k in keylist:
            s= s[k]
        return s
    except KeyError as e:
        raise KeyError("%s not found (subkey: %s)" % (keylist,e))
    except IndexError as e:
        raise IndexError("%s not found (subkey index: %s)" % (keylist,e))
    except TypeError as e:
        raise KeyError("%s not found (subkey index: %s)" % (keylist,e))

# ---------------------------------------------------------
# change values in structured data

def struct_keylist_change(s, keylist, val):
    """change an element in a structure.
    >>> import pprint
    >>> d= {'A': {'B': {'C': 'val'},
    ...           'b': {'C': 'val2',
    ...                 'D': [None, None, {'X': 'val4'}, 'val3']
    ...                }
    ...          }
    ...    }
    >>> struct_keylist_change(d, ["A","b","C"], "new")
    >>> pprint.pprint(d)
    {'A': {'B': {'C': 'val'},
           'b': {'C': 'new', 'D': [None, None, {'X': 'val4'}, 'val3']}}}
    >>> struct_keylist_change(d, ["A","b","D",1], 999)
    >>> pprint.pprint(d)
    {'A': {'B': {'C': 'val'},
           'b': {'C': 'new', 'D': [None, 999, {'X': 'val4'}, 'val3']}}}
    >>> struct_keylist_change(d, ["A","b","X"], "new")
    Traceback (most recent call last):
        ...
    KeyError: "['A', 'b', 'X'] not found (subkey: 'X')"
    >>> struct_keylist_change(d, ["A","X","C"], "new")
    Traceback (most recent call last):
        ...
    KeyError: "['A', 'X'] not found (subkey: 'X')"
    >>> struct_keylist_change(d, ["A","b","D",10], 999)
    Traceback (most recent call last):
        ...
    IndexError: ['A', 'b', 'D', 10] not found (subkey index: 10)
    """
    if not keylist:
        raise AssertionError("empty keylist")
    subkey= keylist[-1]
    if len(keylist)<=1:
        obj= s
    else:
        obj= struct_keylist_get(s, keylist[:-1])
        # (may raise KeyError or IndexError)
    if hasattr(obj,"get"):
        # a dictionary
        if subkey not in obj:
            raise KeyError("%s not found (subkey: '%s')" % \
                            (keylist,subkey))
        obj[subkey]= val
        return
    if hasattr(obj,"__setitem__"):
        try:
            obj[subkey]= val
            return
        except IndexError:
            raise IndexError("%s not found (subkey index: %s)" % \
                              (keylist,subkey))
    raise AssertionError("unexpected variable type in %s" % keylist)

# ---------------------------------------------------------
# add values to structured data

def struct_keylist_add(s, keylist, value, always_dicts= False):
    """recursively add elements to a structure.

    Note:
    an integer in the keylist implies that a list should be
    created except when always_dicts is True.

    Here are some examples:
    >>> import pprint
    >>> d={}
    >>> struct_keylist_add(d, ["A","B","C"], "val")
    >>> pprint.pprint(d)
    {'A': {'B': {'C': 'val'}}}
    >>> struct_keylist_add(d, ["A","b","C"], "val2")
    >>> pprint.pprint(d)
    {'A': {'B': {'C': 'val'}, 'b': {'C': 'val2'}}}
    >>> struct_keylist_add(d, ["A","b","C",3], "val3")
    Traceback (most recent call last):
        ...
    AssertionError: found a node that is neither list nor dictionary
    keyindex: 2 path so far: ['A', 'b', 'C'], value found: 'val2'
    >>> struct_keylist_add(d, ["A","b","D",3], "val3")
    >>> pprint.pprint(d)
    {'A': {'B': {'C': 'val'}, 'b': {'C': 'val2', 'D': [None, None, None, 'val3']}}}
    >>> struct_keylist_add(d, ["A","b","D",2,"X"], "val4")
    >>> pprint.pprint(d)
    {'A': {'B': {'C': 'val'},
           'b': {'C': 'val2', 'D': [None, None, {'X': 'val4'}, 'val3']}}}

    >>> d={}
    >>> struct_keylist_add(d, ["A","B","C"], "val", True)
    >>> pprint.pprint(d)
    {'A': {'B': {'C': 'val'}}}
    >>> struct_keylist_add(d, ["A","b","C"], "val2", True)
    >>> pprint.pprint(d)
    {'A': {'B': {'C': 'val'}, 'b': {'C': 'val2'}}}
    >>> struct_keylist_add(d, ["A","b","C",3], "val3", True)
    Traceback (most recent call last):
        ...
    AssertionError: found a node that is neither list nor dictionary
    keyindex: 2 path so far: ['A', 'b', 'C'], value found: 'val2'
    >>> struct_keylist_add(d, ["A","b","D",3], "val3", True)
    >>> pprint.pprint(d)
    {'A': {'B': {'C': 'val'}, 'b': {'C': 'val2', 'D': {3: 'val3'}}}}
    >>> struct_keylist_add(d, ["A","b","D",2,"X"], "val4", True)
    >>> pprint.pprint(d)
    {'A': {'B': {'C': 'val'},
           'b': {'C': 'val2', 'D': {2: {'X': 'val4'}, 3: 'val3'}}}}
    """
    def add(parent, child, keyindex, value):
        """add a new value."""
        if keyindex>=len(keylist):
            parent[keylist[-1]]= value
            return
        if child is None:
            key= keylist[keyindex]
            if isinstance(key, int):
                if always_dicts:
                    child= {}
                else:
                    child= []
            else:
                child= {}
            parent[keylist[keyindex-1]]= child
        if isinstance(child, list):
            key= keylist[keyindex]
            if not isinstance(key, int):
                raise TypeError("key %s in keylist %s is not an int" %\
                        (repr(key), keylist))
            v= list_get(child, key)
            if v is None: # does not yet exist
                # fill list with None where it is not long enough:
                list_add(child, key, None, None)
            add(child, v, keyindex+1, value)
            return
        if isinstance(child, dict):
            key= keylist[keyindex]
            v= child.get(key)
            if v is None: # does not yet exist
                child[key]= None
            add(child, v, keyindex+1, value)
            return
        errstr= ("found a node that is neither list nor dictionary\n" +\
                 "keyindex: %s path so far: %s, value found: %s") % \
                 (keyindex-1,repr(keylist[0:keyindex]), repr(child))
        raise AssertionError(errstr)
    add(None, s, 0, value)

# ---------------------------------------------------------
# iterators

def _list_items(lst):
    """a list iterator that returns key-value pairs."""
    for i, e in enumerate(lst):
        yield (i, e)

def _list_items_value_sorted(lst):
    """a list iterator that returns key-value pairs."""
    for e, i in sorted((e, i) for i, e in enumerate(lst)):
        yield (i, e)

def _key_sorted(dict_):
    """return key value pairs sorted by keys."""
    lst= sorted(dict_.keys())
    for k in lst:
        yield (k, dict_[k])

def _value_sorted(dict_):
    """return key value pairs sorted by keys."""
    lst= sorted([(v,k) for k,v in dict_.items()])
    for v, k in lst:
        yield (k, v)

def key_val_iterator(obj, sorted_= False, value_sorted= False):
    """return a key-value iterator for a dict or a list.

    parameters:
      obj      - the dictionary or list
      sorted_  - if True, return key value pairs sorted.
                 For dictionaries they are sorted by the key,
                 for lists they are sorted by the value.

    Here are some examples:
    >>> d={"X":1, "B":2, "A":3}
    >>> sorted([(k, v) for k,v in key_val_iterator(d)])
    ...
    [('A', 3), ('B', 2), ('X', 1)]
    >>> for (k,v) in key_val_iterator(d, sorted_=True):
    ...   print(k,v)
    ...
    A 3
    B 2
    X 1
    >>> for (k,v) in key_val_iterator(d, sorted_=True, value_sorted=True):
    ...   print(k,v)
    ...
    X 1
    B 2
    A 3
    >>> l=["X","B","A"]
    >>> for (k,v) in key_val_iterator(l):
    ...   print(k,v)
    ...
    0 X
    1 B
    2 A
    >>> for (k,v) in key_val_iterator(l, sorted_=True):
    ...   print(k,v)
    ...
    0 X
    1 B
    2 A
    >>> for (k,v) in key_val_iterator(l, sorted_=True, value_sorted=True):
    ...   print(k,v)
    ...
    2 A
    1 B
    0 X
    """
    if not hasattr(obj, "__iter__"):
        raise TypeError("object %s is not iterable" % repr(obj))
    # pylint: disable= no-else-return
    if hasattr(obj, "keys"):
        if not sorted_:
            return iter(obj.items())
        else:
            if not value_sorted:
                return _key_sorted(obj)
            else:
                return _value_sorted(obj)
    else:
        if (not sorted_) or (not value_sorted):
            return _list_items(obj)
        else:
            return _list_items_value_sorted(obj)
    # pylint: enable= no-else-return

def _test():
    # pylint: disable=import-outside-toplevel
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
