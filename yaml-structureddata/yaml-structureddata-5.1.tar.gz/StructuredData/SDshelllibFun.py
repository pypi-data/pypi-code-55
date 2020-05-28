"""SDshellibFun

implements the functional layer of StructuredData.
"""

import os.path
import glob
import StructuredData.Classes as SD
from StructuredData.internal import rst_load
from StructuredData.internal import myyaml
import StructuredData.SDshelllibBase as base

__version__="5.1" #VERSION#

assert __version__==SD.__version__
assert __version__==rst_load.__version__
assert __version__==myyaml.__version__
assert __version__==base.__version__

# pylint: disable=invalid-name

write_defaults= { "container": None,
                  "store"    : None,
                  "types"    : None
                }

std_return= None
# standard return value for commands

ROOTKEY= SD.ROOTKEY
ANYKEY = SD.ANYKEY


def SDtype():
    """return the software stack on which we are running."""
    return "library"

def global_sym(name):
    """return a global symbol of the given name."""
    return globals()[name]

def struc2sym(struc):
    """return a global symbol from a structure.

    In XMLRPC we cannot simply transfer references global objects.
    So can implement here a way to get a global object from an
    arbitrary structure. The default is to return the object
    itself.
    """
    return struc

def sym2struc(sym):
    """return structure from a global symbol.

    vardict is usually global().

    In XMLRPC we cannot simply transfer references global objects.  So can
    implement here a way to convert a global object to an arbitrary structure.
    The default is to return the object itself.
    """
    return sym

def error(exception, st):
    """raise an exception (why is this needed?)."""
    raise exception(st)

_sdshell_rst= None

def _load_help():
    """load the RST help file."""
    global _sdshell_rst # pylint: disable= global-statement
    if _sdshell_rst is not None:
        return
    module_dir= os.path.split(SD.__file__)[0]
    data_dir= os.path.join(module_dir, "data")
    sd_shell_help_file= os.path.join(data_dir, "SDpyshell.rst")
    _sdshell_rst= rst_load.Rst(rst_load.read_file(sd_shell_help_file))

# pylint: disable=redefined-builtin

def help(item=None, level= None):
    """implement the shell's help function."""
    _load_help()
    if not item:
        # filename==None or filename=="":
        lines=["Please select a topic:",""]
        lines.extend(_sdshell_rst.index())
    elif not isinstance(item, str):
        lines=["error: 1st parameter must be a string"]
    else:
        lines= _sdshell_rst.text(item, level)
    return "\n".join(lines)

# pylint: enable=redefined-builtin

SDC= None

def namedsdc(arg=None):
    """create a new StructuredDataContainer-Key.

    here an sdc-key and an sdc-object are identical.
    """
    sdc= SD.StructuredDataContainer()
    sdc.set_store(SD.StructuredDataStore())
    sdc.set_types(SD.StructuredDataTypes())
    return sdc_register(sdc, arg)

def newsdc():
    """create a new StructuredDataContainer-Key."""
    return namedsdc(None)

def locksdc(sdc):
    """make the sdc read-only."""
    sdc_obj= sdc_get(sdc)
    sdc_obj.lock()
    return std_return

def lockfile(filename):
    """define a filename read-only."""
    base.add_locked_file(filename)

def lockdir(dirname):
    """define a directory read-only."""
    base.add_locked_dir(dirname)

def sdc_register(sdc, user_key= None):
    """create an sdc key from a new sdc object.

    This function is not here to be called directly. It intended to be
    overridden by an application defined function that is then called whenever
    a new sdc object is created. In this "dummy" implementation of the
    function, it simply returns the sdc object, so sdc-key and sdc-object are
    identical here.

    The user_key is an user provided key for the sdc object.  Since this
    implementation simply returns the sdc object itself, the user_key is
    ignored here. However, if this function is overridden, the user_key may be
    taken into account by the new function.
    """
    # pylint: disable=unused-argument
    return sdc

def sdc_get(sdc):
    """returns an sdc-object from an sdc-key.

    This function is not here to be called directly. It intended to be
    overridden by an application defined function that is then called whenever
    a new sdc object is read or written to. In this "dummy" implementation of
    the function, it simply returns the sdc object since the sdc-key and
    sdc-object are identical here.
    """
    global SDC # pylint: disable= global-statement
    if not sdc:
        if not SDC:
            new_key= newsdc()
            # here an sdc-key and an sdc-object are identical:
            SDC= new_key
        return SDC
    return sdc

def _process_paths(paths):
    """returns an iterator on a single string, a pathlist or a pairlist.
    """
    # pylint: disable=redefined-outer-name
    if not SD.is_iterable(paths):
        yield paths
        return # StopIteration
    for elm in paths:
        if isinstance(elm,str) or (not hasattr(elm,"__getitem__")):
            yield elm
        else:
            yield elm[0]
    return # StopIteration

def _path_cmd(path, func):
    """execute a command on a path or a list of paths."""
    if not SD.is_iterable(path):
        func(path)
    else:
        for p in _process_paths(path):
            func(p)

def _path_func(path, func):
    """execute a function on a path or a list of paths."""
    if not SD.is_iterable(path):
        return func(path)
    return [func(p) for p in _process_paths(path)]

def string2pathkey(st):
    """apply escaping rules on '.','[',']' in st.
    """
    return SD.escape_in_stringkey(st)

def pathkey2string(pk):
    """unapply escaping rules on '.','[',']' in pk.
    """
    return SD.unescape_in_stringkey(pk)

def splitpath(path):
    """splits a path according to the rules.
    """
    def my_split_path(path):
        """local split path utility."""
        return [sym2struc(k) for k in SD.StructuredDataStore.split_path(path)]
    return _path_func(path, my_split_path)

def joinpath(keys):
    """joins a path according to the rules.
    """
    return SD.StructuredDataStore.join_path([struc2sym(k) for k in keys])

def combinepaths(paths):
    """combine partial paths to a new one.
    """
    # pylint: disable=redefined-outer-name
    keys= []
    for p in paths:
        keys.extend(SD.StructuredDataStore.split_path(p))
    return joinpath(keys)

def addpaths(path1, path2):
    """combine 2 paths. One may be a list of paths."""
    if SD.is_iterable(path1) and SD.is_iterable(path2):
        error(ValueError, "ERROR: only one arg may be an iterable")
        return std_return
    # pylint: disable= no-else-return
    if SD.is_iterable(path1):
        def _combine(p):
            """utility function."""
            return combinepaths((p, path2))
        return _path_func(path1, _combine)
    elif SD.is_iterable(path2):
        def _combine(p):
            """utility function."""
            return combinepaths((path1, p))
        return _path_func(path2, _combine)
    else:
        return combinepaths((path1, path2))

def poppath(path, no=1):
    """removes parts of a path from the end.
    """
    def _poppath(path_):
        """utility function."""
        l= SD.StructuredDataStore.split_path(path_)
        if no>0:
            l= l[:-no]
        else:
            l= l[-no:]
        return SD.StructuredDataStore.join_path(l)
    return _path_func(path, _poppath)

def substpath(path, pattern):
    """changes the path according to a pattern.
    """
    pattern_keylist= SD.StructuredDataStore.split_path(pattern)
    def _substpath(path_):
        """utility function."""
        return SD.StructuredDataStore.join_path( \
                   SD.SpecialKey.keysubst(
                       SD.StructuredDataStore.split_path(path_),
                       pattern_keylist))
    return _path_func(path, _substpath)

_read_formatspec_obj= base.MultiStringOption(\
        {
            "container" : 0,
            "store"     : 0,
            "types"     : 0,
            "yaml"      : 1,
            "py"        : 1,
            "flat"      : 2,
            "nonflat"   : 2,
        },
        ["container", "yaml", "nonflat"] \
        )

def _my_filter(sds, path_patterns):
    """create a new sds with the filtered data."""
    m= sds.simple_search(path_patterns= path_patterns, add_values= True,
                         only_leaves= True, show_links= False)
    sds_new= SD.StructuredDataStore()
    sds_new.setitems(m, create_missing= True)
    return sds_new

def read(filename= None, formatspec="", sdc=None):
    """generic read from file.

    If bool(sdc) is False, use the global SDC variable.
    Note: this function *does not* create a new StructuredDataStore,
    use newsdc() if you want to create a new one.

    returns:
        (sdc, list_of_read_files)
    """
    # pylint: disable=too-many-branches
    (structure, format_, extra)= _read_formatspec_obj.parse(formatspec)
    sdc_obj= sdc_get(sdc)
    if not filename:
        # filename==None or filename=="":
        globs= {"container": "./*.SDCyml",
                "store"    : "./*.SDSyml",
                "types"    : "./*.SDTyml"}
        lst= glob.glob(globs[structure])
    else:
        lst= [filename]
    if lst:
        write_defaults[structure]= lst[0]
    for f in lst:
        if structure=="container":
            if format_=="yaml":
                sdc_new= SD.StructuredDataContainer.from_yaml_file(f)
            elif format_=='py':
                dict_= base.read_py(f)
                sdc_new= SD.StructuredDataContainer(dict_)
            else:
                raise AssertionError
        elif structure in ("store", "types"):
            if format_=="yaml":
                dict_= myyaml.read_file(f)
            elif format_=='py':
                dict_= base.read_py(f)
            else:
                raise AssertionError
            if structure=="store":
                if extra=="nonflat":
                    sds= SD.StructuredDataStore(dict_)
                elif extra=="flat":
                    sds= SD.StructuredDataStore.from_flat_dict(dict_)
                else:
                    raise AssertionError
                sdc_new= SD.StructuredDataContainer()
                sdc_new.set_store(sds)
            elif structure=="types":
                sdt= SD.StructuredDataTypes(dict_)
                sdc_new= SD.StructuredDataContainer()
                sdc_new.set_types(sdt)
            else:
                raise AssertionError
        else:
            raise AssertionError
        sdc_obj.add(sdc_new.as_dict())
    return (sdc,lst)

_write_formatspec_obj= base.MultiStringOption( \
        {
            "container" : 0,
            "store"     : 0,
            "types"     : 0,
            "yaml"      : 1,
            "py"        : 1,
            "csv"       : 1,
            "flat"      : 2,
            "nonflat"   : 2,
        },
        ["container", "yaml", "nonflat"] \
        )

def write(filename= None, formatspec="", pattern= None, sdc= None):
    """generic write to a file.

    returns:
        name of the written file or, when not bool(filename), the data itself
        or (when error() raises no exception) std_return in case of an error.
    """
    # pylint: disable=too-many-statements
    # pylint: disable=too-many-return-statements
    # pylint: disable=too-many-branches
    (structure, format_, extra)= \
            _write_formatspec_obj.parse(formatspec)
    sdc_object= sdc_get(sdc)
    sdc_local= sdc_object
    if structure=="store" and sdc_local.store() is None:
        error(ValueError, "ERROR: StructuredDataContainer contains no store")
        return std_return
    if structure=="types" and sdc_local.types() is None:
        error(ValueError, "ERROR: StructuredDataContainer contains no types")
        return std_return
    if (structure=="container") and filename:
        # (filename!=None and filename!="")
        msg= base.is_readonly(filename)
        if msg is not None:
            error(IOError, "ERROR: %s" % msg)
            return std_return
    if structure in ("container", "store"):
        if pattern:
            # pattern!=None and pattern!="":
            # create a new container with the filtered data:
            sdc_local= SD.StructuredDataContainer()
            sdc_local.set_types(sdc_object.types())
            sdc_local.set_store(_my_filter(sdc_object.store(), pattern))
    # pylint: disable= no-else-return
    if structure=="container":
        if format_=="yaml":
            if not filename:
                return sdc_local.as_yaml_string()
            else:
                sdc_local.as_yaml_file(filename)
                return filename
        elif format_=="py":
            return base.prettyprint(filename, sdc_local.as_dict())
        else:
            raise AssertionError
    elif structure=="store":
        sds= sdc_local.store()
        if format_=="csv":
            # pylint: disable= no-else-return
            if not filename:
                # filename==None or filename=="":
                return sds.as_csv(align_values=True, delimiter=base.csvdelim)
            else:
                stream= open(filename, 'w')
                sds.as_csv(stream=stream, align_values=True,
                           delimiter=base.csvdelim)
                stream.close()
                return filename
        else:
            if extra=="nonflat":
                dict_= sds.as_dict()
            elif extra=='flat':
                dict_= sds.as_flat_dict()
            else:
                raise AssertionError
            if format_=="yaml":
                return base.write_yml(filename, dict_)
            elif format_=="py":
                return base.prettyprint(filename, dict_)
            else:
                raise AssertionError
    elif structure=="types":
        sdt= sdc_local.types()
        # pylint: disable= no-else-return
        if format_=="yaml":
            dict_= sdt.as_path_dict()
            return base.write_yml(filename, dict_)
        elif format_=="py":
            dict_= sdt.as_path_dict()
            return base.prettyprint(filename, dict_)
        else:
            error(ValueError, "ERROR: unsupported format_ %s" % format_)
            return std_return
    else:
        raise AssertionError
    return std_return

def copy(sdc= None):
    """returns a copy of a StructuredDataContainer."""
    sdc_new= sdc_get(sdc).clone(True)
    return sdc_register(sdc_new)

def clear_store(sdc= None):
    """clear the store of a StructuredDataContainer.
    """
    sdc_get(sdc).clear_store()
    return std_return

def clear_types(sdc= None):
    """clear the types of a StructuredDataContainer.
    """
    sdc_get(sdc).clear_types()
    return std_return

def filter_out(pattern, sdc= None):
    """returns a filtered StructuredDataContainer.
    """
    sdc_obj= sdc_get(sdc)
    sdc_obj.set_store(_my_filter(sdc_obj.store(), pattern))
    return sdc

def paths(pattern="*", paths= None, sdc= None):
    """returns a list of all matching paths in a StructuredDataContainer."""
    # pylint: disable=redefined-outer-name
    sds= sdc_get(sdc).store()
    m= sorted(sds.simple_search(path_patterns= pattern,
                                path_list= paths,
                                add_values= False,
                                only_leaves= False,
                                show_links= False))
    return m

FIND_SIMPLE=1
FIND_IPATTERN=2
FIND_REGEXP=3

def internal_find(type_, pattern, show_links= False,
                  path_list= None,
                  sdc= None):
    """internal find function.

    This is used to cover several flavours of find functions.
    """
    if type_==FIND_SIMPLE:
        m= sdc_get(sdc).store().simple_search(path_patterns= pattern,
                                              path_list= path_list,
                                              add_values= True,
                                              only_leaves= True,
                                              show_links= show_links)
    elif type_==FIND_IPATTERN:
        m= sdc_get(sdc).store().i_search(i_pattern= pattern,
                                         path_list= path_list,
                                         add_values= True,
                                         only_leaves= True,
                                         show_links= show_links)
    elif type_==FIND_REGEXP:
        m= sdc_get(sdc).store().regexp_search(regexp_pattern= pattern,
                                              path_list= path_list,
                                              add_values= True,
                                              only_leaves= True,
                                              show_links= show_links)
    else:
        raise "Assertion"
    return m

def find(pattern, show_links= False,
         paths= None,
         sdc= None):
    """return paths and values for a given pattern.
    """
    # pylint: disable=redefined-outer-name
    return internal_find(FIND_SIMPLE, pattern=pattern,
                         show_links= show_links,
                         path_list= paths,
                         sdc=sdc)

def ifind(pattern, show_links= False,
          paths= None,
          sdc= None):
    """return paths and values for a given "i"-pattern.
    """
    # pylint: disable=redefined-outer-name
    return internal_find(FIND_IPATTERN, pattern=pattern,
                         show_links= show_links,
                         path_list= paths,
                         sdc=sdc)

def rxfind(pattern, show_links= False,
           paths= None,
           sdc= None):
    """return paths and values for a given regexp.
    """
    # pylint: disable=redefined-outer-name
    return internal_find(FIND_REGEXP, pattern=pattern,
                         show_links= show_links,
                         path_list= paths,
                         sdc=sdc)

FINDVAL_SIMPLE=1
FINDVAL_IPATTERN=2
FINDVAL_REGEXP=3

def internal_findval(type_, val_pattern, show_links= False,
                     pattern= None,
                     path_list= None,
                     sdc= None):
    """internal findval function.

    This is used to cover several flavours of findval functions.
    """
    # pylint: disable=too-many-arguments
    if type_==FINDVAL_SIMPLE:
        m= sdc_get(sdc).store().value_search(value= val_pattern,
                                             path_patterns= pattern,
                                             path_list= path_list,
                                             add_values= True,
                                             show_links= show_links)
    elif type_==FINDVAL_IPATTERN:
        m= sdc_get(sdc).store().value_i_search(i_pattern= val_pattern,
                                               path_patterns= pattern,
                                               path_list= path_list,
                                               add_values= True,
                                               show_links= show_links)
    elif type_==FINDVAL_REGEXP:
        m= sdc_get(sdc).store().value_regexp_search(regexp_pattern= \
                                                        val_pattern,
                                                    path_patterns= pattern,
                                                    path_list= path_list,
                                                    add_values= True,
                                                    show_links= show_links)
    else:
        raise "Assertion"
    return m

def findval(value, show_links= False,
            pattern= None,
            paths= None,
            sdc= None):
    """return paths and values for a given value.
    """
    # pylint: disable=redefined-outer-name
    return internal_findval(FINDVAL_SIMPLE,
                            val_pattern= value,
                            show_links= show_links,
                            pattern= pattern,
                            path_list= paths,
                            sdc=sdc)

def ifindval(val_pattern, show_links= False,
             pattern= None,
             paths= None,
             sdc= None):
    """return paths and values for a value matching an "i"-pattern.
    """
    # pylint: disable=redefined-outer-name
    return internal_findval(FINDVAL_IPATTERN,
                            val_pattern= val_pattern,
                            show_links= show_links,
                            pattern= pattern,
                            path_list= paths,
                            sdc=sdc)

def rxfindval(val_pattern, show_links= False,
              pattern= None,
              paths= None,
              sdc= None):
    """return paths and values for a value matching a regexp.
    """
    # pylint: disable=redefined-outer-name
    return internal_findval(FINDVAL_REGEXP,
                            val_pattern= val_pattern,
                            show_links= show_links,
                            pattern= pattern,
                            path_list= paths,
                            sdc=sdc)

def get(pattern, show_links= False, paths= None, sdc= None):
    """get a part of the structure for a given pattern."""
    # pylint: disable=redefined-outer-name
    sdc_obj= sdc_get(sdc)
    res= []
    for(_,_,val) in sdc_obj.store().universal_iter(patterns= pattern,
                                                   path_list= paths,
                                                   only_leaves= False,
                                                   sorted_= True,
                                                   show_links= show_links):
        res.append(val)
    if not res:
        return None
    if len(res)==1:
        return res[0]
    return res

def change(path, value, sdc= None):
    """changes a single value."""
    def _change(path_):
        """utility function."""
        try:
            sdc_get(sdc).store()[path_]= value
        except KeyError as _:
            error(KeyError, "path \"%s\" doesn't exist" % path_)
            return std_return
        return std_return
    _path_cmd(path, _change)
    return std_return

def put(path, value, sdc= None):
    """add a single value."""
    def _put(path_):
        """utility function."""
        try:
            sdc_get(sdc).store().setitem(path_, value,
                                         create_missing= True,
                                         always_dicts= False)
        except KeyError as e:
            error(KeyError, str(e))
            return std_return
        return std_return
    _path_cmd(path, _put)
    return std_return

def delete(path, sdc= None):
    """delete a single value."""
    def _delete(path_):
        """utility function."""
        try:
            del sdc_get(sdc).store()[path_]
        except KeyError as _:
            error(KeyError, "path \"%s\" doesn't exist" % path_)
            return std_return
        return std_return
    _path_cmd(path, _delete)
    return std_return

def link(from_path, to_path, sdc= None):
    """create a link to an existing value at another path."""
    sdstore= sdc_get(sdc).store()
    try:
        sdstore[to_path]
    except KeyError as _:
        error(KeyError, "to-path \"%s\" doesn't exist" % to_path)
        return std_return
    except IndexError as _:
        error(KeyError, "to-path \"%s\" doesn't exist" % to_path)
        return std_return
    def _link(_from):
        """utility function."""
        sdstore.link(_from, to_path)
    _path_cmd(from_path, _link)
    return std_return

def refresh_links(sdc= None):
    """refresh the internal link cache."""
    sdc_get(sdc).store().refresh_links()
    return std_return

def getlinks(path, include=None, exclude=None, sdc= None):
    """return links for a path."""
    sds= sdc_get(sdc).store()
    links_set= sds.get_links(path, include=include, exclude= exclude)
    links= sorted(list(links_set))
    return links

def findlinks(pattern, include= None, exclude= None, sdc= None):
    """find links for a pattern."""
    sds= sdc_get(sdc).store()
    linksset_list= sds.pattern_get_links(pattern,
                                         include= include, exclude= exclude,
                                         only_multi_links=True)
    links= [ sorted(list(x)) for x in linksset_list ]
    return links

def typepaths(pattern="*", sdc= None):
    """find typepaths for a pattern."""
    sdt= sdc_get(sdc).types()
    m= sorted(sdt.simple_search(pattern, add_values= False))
    return m

def typefind(pattern, sdc= None):
    """find a type for a pattern."""
    m= sdc_get(sdc).types().simple_search(pattern, add_values= True)
    m= [(p,t.to_dict()) for (p,t) in m]
    return m

def typeget(path, sdc= None):
    """get a type for a path."""
    sdt= sdc_get(sdc).types()
    try:
        val= sdt[path]
    except KeyError as _:
        error(KeyError, "path \"%s\" doesn't exist" % path)
        return std_return
    if val is None:
        error(KeyError, "path \"%s\" doesn't exist" % path)
        return std_return
    val= val.to_dict()
    return val

def typeput(path, value, sdc= None):
    """set a type."""
    try:
        sdc_get(sdc).types().add({path:value})
    except ValueError as e:
        error(ValueError, str(e))
    return std_return

def _find_type_items(sdc, path):
    """find a typespec item set.

    This function returns a set object.
    """
    sdt= sdc_get(sdc).types()
    try:
        val= sdt[path]
    except KeyError as e:
        return (None,"path \"%s\" doesn't exist" % path)
    try:
        items= val.items() # method of a SingleTypeSpec object
    except TypeError as e:
        return (None, str(e))
    return (items, None)

def typeadditem(path, item, sdc=None):
    """add an item to a type definition."""
    if not isinstance(item, str):
        error(TypeError, "item must be a string")
        return std_return
    (items, msg)= _find_type_items(sdc, path)
    if items is None:
        error(KeyError, msg)
        return std_return
    items.add(item)
    return std_return

def typedelete(path, sdc= None):
    """delete a type."""
    try:
        del sdc_get(sdc).types()[path]
    except KeyError as _:
        error(KeyError, "path \"%s\" doesn't exist" % path)
    return std_return

def typedeleteitem(path, item, sdc=None):
    """delete an item in a type definition."""
    if not isinstance(item, str):
        error(TypeError, "item must be a string")
        return std_return
    (items, msg)= _find_type_items(sdc, path)
    if items is None:
        error(ValueError, msg)
        return std_return
    try:
        items.remove(item)
    except KeyError as _:
        error(KeyError, "cannot delete '%s': not found" % item)
    return std_return

def typecheck(sdc= None):
    """perform a typecheck on the StructuredDataContainer.
    """
    try:
        sdc_get(sdc).typecheck()
    except TypeError as e:
        error(TypeError, "TypeError: %s" % e)
        return False
    return True

def typematch(path, sdc= None):
    """try to find a typecheck for the given path.
    """
    sdt= sdc_get(sdc).types()
    if sdt is None:
        return None
    m= sdt.match(path, return_matchpath= True)
    if m is not None:
        if m[1] is None:
            m= None
    if m is None:
        d= {}
    else:
        d= { m[0]: m[1].to_dict() }
    return d
