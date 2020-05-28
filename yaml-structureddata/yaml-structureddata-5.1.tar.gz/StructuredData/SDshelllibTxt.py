"""SDshellibTxt

implements the text layer of StructuredData.
"""

import StructuredData.SDshelllibBase as base
import StructuredData.SDshelllibFun as fun

__version__="5.1" #VERSION#

assert __version__==base.__version__
assert __version__==fun.__version__

# pylint: disable=invalid-name

write_defaults= fun.write_defaults

error= fun.error

# pylint: disable=redefined-builtin

help = fun.help

ROOTKEY= fun.ROOTKEY
ANYKEY = fun.ANYKEY

_format_formatspec_obj= base.MultiStringOption(
    {
        "raw"        :0,
        "yaml"       :0,
        "py"         :0,
        "csv"        :0,
        "aligned"    :0,
    },
    ["yaml"]
    )

def format(val, formatspec=""):
    """formats a value according to the given format.
    """
    (format_,)= _format_formatspec_obj.parse(formatspec)
    if format_=="aligned":
        return base.aligned(val)
    return base.multi(format_, val, base.csvdelim)

# pylint: enable=redefined-builtin

string2pathkey = fun.string2pathkey
pathkey2string  = fun.pathkey2string

_splitpath_formatspec_obj= base.MultiStringOption(
    {
        "yaml"       :0,
        "py"         :0,
        "raw"        :0,
    },
    ["yaml"]
    )

def splitpath(path, formatspec=""):
    """splits a path according to the rules.
    """
    (format_,)= _splitpath_formatspec_obj.parse(formatspec)
    return base.multi(format_, fun.splitpath(path), base.csvdelim)

_joinpath_formatspec_obj= base.MultiStringOption(
    {
        "yaml"       :0,
        "py"         :0,
        "raw"        :0,
    },
    ["raw"]
    )

def joinpath(keys, formatspec=""):
    """joins a path according to the rules.
    """
    (format_,)= _joinpath_formatspec_obj.parse(formatspec)
    return base.multi(format_, fun.joinpath(keys), base.csvdelim)

_combinepaths_formatspec_obj= base.MultiStringOption(
    {
        "yaml"       :0,
        "py"         :0,
        "raw"        :0,
    },
    ["raw"]
    )

def combinepaths(paths, formatspec=""):
    """combines paths according to the rules.
    """
    # pylint: disable=redefined-outer-name
    (format_,)= _combinepaths_formatspec_obj.parse(formatspec)
    return base.multi(format_, fun.combinepaths(paths), base.csvdelim)

_addpaths_formatspec_obj= base.MultiStringOption(
    {
        "yaml"       :0,
        "py"         :0,
        "raw"        :0,
    },
    ["raw"]
    )

def addpaths(path1, path2, formatspec=""):
    """combines paths according to the rules.
    """
    (format_,)= _addpaths_formatspec_obj.parse(formatspec)
    return base.multi(format_, fun.addpaths(path1, path2), base.csvdelim)

_poppath_formatspec_obj= base.MultiStringOption(
    {
        "yaml"       :0,
        "py"         :0,
        "raw"        :0,
    },
    ["raw"]
    )

def poppath(path, formatspec="", no=1):
    """removes parts of a path from the end.
    """
    (format_,)= _poppath_formatspec_obj.parse(formatspec)
    return base.multi(format_, fun.poppath(path, no), base.csvdelim)

_substpath_formatspec_obj= base.MultiStringOption(
    {
        "yaml"       :0,
        "py"         :0,
        "raw"        :0,
    },
    ["raw"]
    )

def substpath(path, pattern, formatspec=""):
    """removes parts of a path from the end.
    """
    (format_,)= _substpath_formatspec_obj.parse(formatspec)
    return base.multi(format_, fun.substpath(path, pattern), base.csvdelim)

read= fun.read
write= fun.write

copy= fun.copy

clear_store= fun.clear_store
clear_types= fun.clear_types
filter_out = fun.filter_out

_paths_formatspec_obj= base.MultiStringOption(
    {
        "yaml"       :0,
        "py"         :0,
        "csv"        :0,
        "raw"        :0,
        "hidelinks"  :1,
        "marklinks"  :1,
    },
    ["yaml", "hidelinks"]
    )

def paths(pattern="*", formatspec="",
          paths= None,
          sdc= None):
    """returns a list of all matching paths in a StructuredDataContainer."""
    # pylint: disable=redefined-outer-name
    (format_, _)= _paths_formatspec_obj.parse(formatspec)
    m= fun.paths(pattern,
                 paths= paths,
                 sdc=sdc)
    if format_=='csv':
        packed= [ [x] for x in m ]
        return base.as_csv(packed, base.csvdelim)
    return base.multi(format_, m)

_find_formatspec_obj= base.MultiStringOption(
    {
        "yaml"       :0,
        "py"         :0,
        "csv"        :0,
        "aligned"    :0,
        "raw"        :0,
        "hidelinks"  :1,
        "marklinks"  :1,
    },
    ["aligned", "hidelinks"]
    )

FIND_SIMPLE= fun.FIND_SIMPLE
FIND_IPATTERN= fun.FIND_IPATTERN
FIND_REGEXP= fun.FIND_REGEXP

def internal_find(type_, pattern,
                  path_list= None,
                  formatspec="", sdc= None):
    """internal find function.

    This is used to cover several flavours of find functions.
    """
    (format_, linkspec)= _find_formatspec_obj.parse(formatspec)
    m= fun.internal_find(type_, pattern,
                         path_list= path_list,
                         show_links= (linkspec=="marklinks"),
                         sdc= sdc)
    if format_=="aligned":
        l=0
        for (k,_) in m:
            if len(k)>l:
                l=len(k)
        d= dict(m)
        res= []
        for k in sorted(d.keys()):
            res.append("%s: %s" % (k.ljust(l),d[k]))
        return "\n".join(res)
    # pylint: disable= no-else-return
    if format_=="raw":
        return m
    elif format_=="yaml":
        return base.yaml(dict(m))
    elif format_=='py':
        return base.py(dict(m))
    elif format_=='csv':
        return base.as_csv(m, base.csvdelim)
    else:
        error(ValueError, "ERROR: unexpected format_:%s" % format_)
        return fun.std_return

def find(pattern, formatspec="",
         paths= None,
         sdc= None):
    """return paths and values for a given pattern.
    """
    # pylint: disable=redefined-outer-name
    return internal_find(fun.FIND_SIMPLE, pattern=pattern,
                         formatspec= formatspec,
                         path_list= paths,
                         sdc=sdc)

def ifind(pattern, formatspec="",
          paths= None,
          sdc= None):
    """return paths and values for a given "i"-pattern.
    """
    # pylint: disable=redefined-outer-name
    return internal_find(fun.FIND_IPATTERN, pattern=pattern,
                         formatspec= formatspec,
                         path_list= paths,
                         sdc=sdc)

def rxfind(pattern, formatspec="",
           paths= None,
           sdc= None):
    """return paths and values for a given regexp.
    """
    # pylint: disable=redefined-outer-name
    return internal_find(fun.FIND_REGEXP, pattern=pattern,
                         formatspec= formatspec,
                         path_list= paths,
                         sdc=sdc)

FINDVAL_SIMPLE= fun.FINDVAL_SIMPLE
FINDVAL_IPATTERN= fun.FINDVAL_IPATTERN
FINDVAL_REGEXP= fun.FINDVAL_REGEXP

_findval_formatspec_obj= base.MultiStringOption(
    {
        "yaml"       :0,
        "py"         :0,
        "csv"        :0,
        "aligned"    :0,
        "raw"        :0,
        "hidelinks"  :1,
        "marklinks"  :1,
    },
    ["aligned", "hidelinks"]
    )

def internal_findval(type_,
                     val_pattern,
                     pattern= None,
                     path_list= None,
                     formatspec="", sdc= None):
    """internal findval function.

    This is used to cover several flavours of findval functions.
    """
    # pylint: disable=too-many-arguments
    (format_, linkspec)= _findval_formatspec_obj.parse(formatspec)
    m= fun.internal_findval(type_, val_pattern,
                            show_links= (linkspec=="marklinks"),
                            pattern= pattern,
                            path_list= path_list,
                            sdc= sdc)
    # pylint: disable= no-else-return
    if format_=="raw":
        return m
    elif format_=="aligned":
        return base.aligned(m)
    elif format_=="yaml":
        return base.yaml(dict(m))
    elif format_=='py':
        return base.py(dict(m))
    elif format_=='csv':
        return base.as_csv(m, base.csvdelim)
    else:
        error(ValueError, "ERROR: unexpected format_:%s" % format_)
        return fun.std_return

def findval(value, formatspec="",
            pattern= None,
            paths= None,
            sdc= None):
    """return paths and values for a given value.
    """
    # pylint: disable=redefined-outer-name
    return internal_findval(fun.FINDVAL_SIMPLE, val_pattern= value,
                            pattern= pattern,
                            path_list= paths,
                            formatspec= formatspec, sdc=sdc)

def ifindval(val_pattern, formatspec="",
             pattern= None,
             paths= None,
             sdc= None):
    """return paths and values for a value matching an "i"-pattern.
    """
    # pylint: disable=redefined-outer-name
    return internal_findval(fun.FINDVAL_IPATTERN, val_pattern= val_pattern,
                            pattern= pattern,
                            path_list= paths,
                            formatspec= formatspec, sdc=sdc)

def rxfindval(val_pattern, formatspec="",
              pattern= None,
              paths= None,
              sdc= None):
    """return paths and values for a value matching a regexp.
    """
    # pylint: disable=redefined-outer-name
    return internal_findval(fun.FINDVAL_REGEXP, val_pattern= val_pattern,
                            pattern= pattern,
                            path_list= paths,
                            formatspec= formatspec, sdc=sdc)

_get_formatspec_obj= base.MultiStringOption(
    {
        "yaml"      :0,
        "py"        :0,
        "raw"       :0,
        "hidelinks" :1,
        "marklinks" :1,
    },
    ["raw", "hidelinks"]
    )

def get(pattern, formatspec="", paths= None, sdc= None):
    """get a part of the structure for a given pattern."""
    # pylint: disable=redefined-outer-name
    (format_, linkspec)= _get_formatspec_obj.parse(formatspec)
    val= fun.get(pattern,
                 show_links= (linkspec=="marklinks"),
                 paths= paths,
                 sdc= sdc)
    if val is None:
        return None
    return base.multi(format_, val)

change= fun.change
put= fun.put
delete= fun.delete
link= fun.link
refresh_links= fun.refresh_links

_get_links_formatspec_obj= base.MultiStringOption(
    {
        "yaml"   :0,
        "py"     :0,
        "raw"    :0,
    },
    ["yaml"]
    )

def getlinks(path, formatspec="", include=None, exclude=None, sdc= None):
    """return links for a path."""
    (format_,)= _get_links_formatspec_obj.parse(formatspec)
    links= fun.getlinks(path= path,
                        include= include,
                        exclude= exclude,
                        sdc= sdc)
    return base.multi(format_, links)

_find_links_formatspec_obj= base.MultiStringOption(
    {
        "yaml"   :0,
        "py"     :0,
        "raw"    :0,
    },
    ["yaml"]
    )

def findlinks(pattern, formatspec="", include= None, exclude= None,
              sdc= None):
    """find links for a pattern."""
    (format_,)= _find_links_formatspec_obj.parse(formatspec)
    links= fun.findlinks(pattern= pattern,
                         include= include,
                         exclude= exclude,
                         sdc= sdc)
    return base.multi(format_, links)

_typepaths_formatspec_obj= base.MultiStringOption(
    {
        "yaml"       :1,
        "py"         :1,
        "csv"        :1,
        "raw"        :1,
    },
    ["yaml"]
    )

def typepaths(pattern="*", formatspec="", sdc= None):
    """find typepaths for a pattern."""
    (format_,)= _typepaths_formatspec_obj.parse(formatspec)
    m= fun.typepaths(pattern, sdc= sdc)
    if format_=='csv':
        m= [ [x] for x in m ]
        return base.as_csv(m, base.csvdelim)
    return base.multi(format_, m)

_typefind_formatspec_obj= base.MultiStringOption(
    {
        "yaml"       :1,
        "py"         :1,
        "csv"        :1,
        "aligned"    :1,
        "raw"        :1,
    },
    ["aligned"]
    )

def typefind(pattern, formatspec="", sdc= None):
    """find a type for a pattern."""
    (format_,)= _typefind_formatspec_obj.parse(formatspec)
    m= fun.typefind(pattern, sdc= sdc)
    if format_=="aligned":
        return base.aligned(m)
    return base.multi(format_, m)

_typeget_formatspec_obj= base.MultiStringOption(
    {
        "yaml"      :0,
        "py"        :0,
        "raw"       :0,
    },
    ["yaml"]
    )

def typeget(path, formatspec="", sdc= None):
    """get a type for a path."""
    (format_,)= _typeget_formatspec_obj.parse(formatspec)
    val= fun.typeget(path= path, sdc= sdc)
    if val is None:
        return None
    return base.multi(format_, val)

typeput= fun.typeput
typeadditem= fun.typeadditem
typedelete= fun.typedelete
typedeleteitem= fun.typedeleteitem
typecheck= fun.typecheck

_typematch_formatspec_obj= base.MultiStringOption(
    {
        "yaml"   :0,
        "py"     :0,
        "raw"    :0,
    },
    ["yaml"]
    )

def typematch(path, formatspec="", sdc= None):
    """try to find a typecheck for the given path.
    """
    (format_,)= _typematch_formatspec_obj.parse(formatspec)
    val= fun.typematch(path, fun.sdc_get(sdc))
    if val is None:
        error(ValueError,
              "ERROR: StructuredDataContainer contains no type information")
        return val
    return base.multi(format_, val)
