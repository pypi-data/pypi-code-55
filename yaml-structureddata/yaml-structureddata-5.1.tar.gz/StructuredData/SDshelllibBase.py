"""basic function for the shell.
"""

import inspect
import os.path
import pprint
import csv
import io
from StructuredData.internal import myyaml
from StructuredData.internal import Repr
import StructuredData.Classes as SD

__version__="5.1" #VERSION#

assert __version__==myyaml.__version__
assert __version__==Repr.__version__
assert __version__==SD.__version__

# pylint: disable= invalid-name

csvdelim= ';'

locked_files= set()
locked_dirs= set()

def use_file_lock(flag):
    """switch file locking on and off."""
    SD.use_lockfile= flag

def add_locked_file(filename):
    """add locked file."""
    locked_files.add(os.path.abspath(filename))

def add_locked_dir(dir_):
    """add locked dir."""
    locked_dirs.add(os.path.abspath(dir_))

def module_functions(modules):
    """return all functions of a dict of modules.

    modules must be a dict mapping module names to module objects. The
    function returns a dict mapping function names to function objects.
    """
    def fname(mod_name,fun):
        """function name."""
        if not mod_name:
            return fun
        return "%s.%s" % (mod_name, fun)
    funcs= {}
    for (mod_name, mod) in modules.items():
        for m in inspect.getmembers(mod):
            if not inspect.isfunction(m[1]):
                continue
            funcs[fname(mod_name,m[0])]= m[1]
    return funcs

def is_readonly(path):
    """returns True of the path (file) should not be written.
    """
    path= os.path.abspath(path)
    (head, tail)= os.path.split(path)
    head= os.path.abspath(head)
    if head in locked_dirs:
        return "directory '%s' is read-only" % head
    p= os.path.join(head, tail)
    if p in locked_files:
        return "file '%s' is read-only" % p
    return None

def read_py(f):
    """read as python struct."""
    # pylint: disable= eval-used
    dict_= eval(open(f).read())
    return dict_

def py(val):
    """format as python."""
    return pprint.pformat(val)

def prettyprint(filename, struct):
    """pretty print a structure to console or a file."""
    if not filename:
        # filename==None or filename=="":
        return py(struct)
    stream= open(filename, 'w')
    pprint.pprint(struct, stream)
    stream.close()
    return filename

def write_yml(filename, struct):
    """write in yaml to console or a file."""
    if not filename:
        # filename==None or filename=="":
        return myyaml.write_string(struct)
    myyaml.write_file(filename, struct)
    return filename

def as_csv(iterator, delimiter):
    """return as csv data."""
    result= io.StringIO()
    csvwriter= csv.writer(result,
                          delimiter= delimiter,
                          lineterminator= os.linesep)
    for elm in sorted(iterator):
        csvwriter.writerow(elm)
    contents= result.getvalue()
    result.close()
    return contents

def aligned(val):
    """return aligned."""
    maxlen=0
    d= {}
    if hasattr(val, "items"):
        for (k,v) in val.items():
            if len(k)>maxlen:
                maxlen=len(k)
            d[k]= v
    elif hasattr(val, "__iter__"):
        for (k,v) in val:
            if len(k)>maxlen:
                maxlen=len(k)
            d[k]= v
    else:
        raise AssertionError("unsupported val for align: %s" % repr(val))
    res= []
    for k in sorted(d.keys()):
        res.append("%s: %s" % (k.ljust(maxlen),d[k]))
    return "\n".join(res)

def yaml(val):
    """return yaml."""
    return myyaml.write_string(val)

def multi(format_, val, delimiter=";"):
    """multi formatter."""
    # pylint: disable= no-else-return
    if format_=="raw":
        if isinstance(val, str):
            # return a string as it is:
            return val
        # otherwise return a nice "repr" string:
        return Repr.repr(val)
    elif format_=="yaml":
        return yaml(val)
    elif format_=='py':
        return py(val)
    elif format_=='csv':
        return as_csv(val, delimiter)
    else:
        raise ValueError("ERROR: unexpected format_:%s" % format_)

class MultiStringOption():
    """A helper class for string options.

    Here are some examples:

    >>> m= _MultiStringOption({"a":0, "b":0, "c":0, "x":1, "y":1},[None,"y"])
    >>> m.parse("x:b")
    ['b', 'x']
    >>> m.parse("x:b:a")
    Traceback (most recent call last):
        ...
    ValueError: contradicting part 'a' in spec 'x:b:a'
    >>> m.parse("a")
    ['a', 'y']
    >>> m.parse("x")
    [None, 'x']
    >>> m.parse("z")
    Traceback (most recent call last):
        ...
    ValueError: unknown part 'z' in spec 'z'
    """
    def __init__(self, values, defaults):
        """constructor."""
        self._values= values
        self._defaults= defaults
    def __repr__(self):
        """return a repr string for the object."""
        return "_MultiStringOption(%s, %s)" % \
               (repr(self._values), repr(self._defaults))
    def parse(self, spec):
        """parse a spec string.

        parameters:
            spec -   specification string

        returns:
            a tuple (result, new):
        """
        results= [None] * len(self._defaults)
        lst= spec.split(":")
        for st in lst:
            if st=="":
                continue
            st_l= st.lower()
            idx= self._values.get(st_l)
            if idx is None:
                raise ValueError("unknown part '%s' in spec '%s'" % \
                        (st, spec))
            if results[idx] is not None:
                raise ValueError("contradicting part '%s' in spec '%s'" % \
                        (st, spec))
            results[idx]= st_l
        # pylint: disable= consider-using-enumerate
        for idx in range(len(results)):
            if results[idx] is None:
                results[idx]= self._defaults[idx]
        return results
