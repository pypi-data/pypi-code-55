"""SDshellibTxt

implements the interactive layer of StructuredData.
"""

import StructuredData.Classes as SD

import StructuredData.SDshelllibBase as base
import StructuredData.SDshelllibFun as fun
import StructuredData.SDshelllibTxt as txt

__version__="5.1" #VERSION#

assert __version__==base.__version__
assert __version__==fun.__version__
assert __version__==txt.__version__

# pylint: disable=invalid-name

interactive= False

ROOTKEY= SD.ROOTKEY
ANYKEY = SD.ANYKEY

exported_vars= {"ROOTKEY" : ROOTKEY,
                "ANYKEY"  : ANYKEY
               }

def error(exception, st):
    """print an error message."""
    if interactive:
        print(st)
    else:
        txt.error(exception, st)

# levels of functions:
# py_... return python structures
# txt_... return a multi_line string
# ... else

# pylint: disable=redefined-builtin

def help(item=None, level= None):
    """implement the shell's help function."""
    print(txt.help(item= item, level= level))

# pylint: enable=redefined-builtin

# an alias for help:
h= help

def format(val, formatspec=""):
    """formats a value according to the given format.
    """
    # pylint: disable=redefined-builtin
    print(txt.format(val= val, formatspec= formatspec))

def string2pathkey(st):
    """convert a path (string) to a list of keys."""
    print(txt.string2pathkey(st))

def pathkey2string(pk):
    """convert a list of keys to a path (string)."""
    print(txt.pathkey2string(pk))

def splitpath(path, formatspec=""):
    """splits a path according to the rules.
    """
    print(txt.splitpath(path= path, formatspec= formatspec))

def joinpath(keys, formatspec=""):
    """splits a path according to the rules.
    """
    print(txt.joinpath(keys, formatspec))

def combinepaths(paths, formatspec=""):
    """combines paths according to the rules.
    """
    # pylint: disable=redefined-outer-name
    print(txt.combinepaths(paths, formatspec))

def addpaths(path1, path2, formatspec=""):
    """combines paths according to the rules.
    """
    print(txt.addpaths(path1, path2, formatspec))

def poppath(path, formatspec="", no=1):
    """removes parts of a path from the end.
    """
    print(txt.poppath(path= path, formatspec= formatspec, no=no))

def substpath(path, pattern, formatspec=""):
    """removes parts of a path from the end.
    """
    print(txt.substpath(path= path, pattern= pattern,
                        formatspec= formatspec))

def read(filename= None, formatspec="", sdc=None):
    """generic read from file.

    If bool(sdc) is False, use the global SDC variable.
    Note: this function *does not* create a new StructuredDataStore,
    use newsdc() if you want to create a new one.

    returns:
        sdc
    """
    (sdc, lst)= txt.read(filename= filename,
                         formatspec= formatspec,
                         sdc= sdc)
    if interactive and (not filename):
        # interactive and (filename==None or filename==""):
        if len(lst)>1:
            print("Files read: ", end=' ')
        else:
            print("File read: ", end=' ')
        print(" ".join(lst))
    return sdc

# an alias for read:
r= read

def write(filename= None, formatspec="", pattern= None, sdc= None):
    """generic write to a file.
    """
    res= txt.write(filename= filename, formatspec=formatspec,
                   pattern= pattern, sdc= sdc)
    if not filename:
        # no file created, res is the data itself:
        print(res)
    elif res and (res != fun.std_return):
        # filename!=None and filename!="":
        print("file \"%s\" written" % res)

# an alias for write:
w= write

def pr(formatspec="", pattern= None, sdc= None):
    """generic print to the console."""
    write(filename= None, formatspec= formatspec, pattern= pattern,
          sdc= sdc)

# an alias for pr:
p= pr

_rewrite_formatspec_obj= base.MultiStringOption( \
        {
            "container" : 0,
            "store"     : 0,
            "types"     : 0,
            "yaml"      : 1,
            "py"        : 1,
            "csv"       : 1,
            "flat"      : 2,
            "nonflat"   : 2,
            "run"       : 3,
            "dry-run"   : 3,
        },
        ["container", "yaml", "nonflat", "run"] \
        )

def rewrite(formatspec="", pattern= None, sdc= None):
    """write the StructuredData back to the file."""
    (structure, format_, extra, flag)= \
            _rewrite_formatspec_obj.parse(formatspec)
    filename= txt.write_defaults[structure]
    if not filename:
        if flag=="dry-run":
            print("no default filename for writing a %s" % structure)
        else:
            error(ValueError,
                  "ERROR: no default filename for writing a %s" % structure)
        return None
    if flag=="dry-run":
        print("would write to file %s" % filename)
        return None
    return write(filename= filename,
                 formatspec= ":".join([structure,format_,extra]),
                 pattern= pattern,
                 sdc= sdc)

# an alias for rewrite:
rw= rewrite

copy= txt.copy

clear_store= txt.clear_store
clear_types= txt.clear_types
filter_out = txt.filter_out

def paths(pattern="*", formatspec="",
          paths= None,
          sdc= None):
    """returns a list of all matching paths in a StructuredDataContainer."""
    # pylint: disable=redefined-outer-name
    print(txt.paths(pattern= pattern, formatspec= formatspec,
                    paths= paths,
                    sdc= sdc))


def internal_find(type_, pattern,
                  path_list= None,
                  formatspec="", sdc= None):
    """internal find function.

    This is used to cover several flavours of find functions.
    """
    print(txt.internal_find(type_= type_, pattern= pattern,
                            path_list= path_list,
                            formatspec= formatspec,
                            sdc= sdc))

def find(pattern, formatspec="",
         paths= None,
         sdc= None):
    """return paths and values for a given pattern.
    """
    # pylint: disable=redefined-outer-name
    internal_find(txt.FIND_SIMPLE, pattern=pattern,
                  formatspec= formatspec,
                  path_list= paths,
                  sdc=sdc)

def ifind(pattern, formatspec="",
          paths= None,
          sdc= None):
    """return paths and values for a given "i"-pattern.
    """
    # pylint: disable=redefined-outer-name
    internal_find(txt.FIND_IPATTERN, pattern=pattern,
                  formatspec= formatspec,
                  path_list= paths,
                  sdc=sdc)

def rxfind(pattern, formatspec="",
           paths= None,
           sdc= None):
    """return paths and values for a given regexp.
    """
    # pylint: disable=redefined-outer-name
    internal_find(txt.FIND_REGEXP, pattern=pattern,
                  formatspec= formatspec,
                  path_list= paths,
                  sdc=sdc)

def internal_findval(type_, val_pattern,
                     pattern= None,
                     path_list= None,
                     formatspec="", sdc= None):
    """internal findval function.

    This is used to cover several flavours of findval functions.
    """
    # pylint: disable=too-many-arguments
    print(txt.internal_findval(type_= type_,
                               val_pattern= val_pattern,
                               pattern= pattern,
                               path_list= path_list,
                               formatspec= formatspec,
                               sdc= sdc))


def findval(value, formatspec="",
            pattern= None,
            paths= None,
            sdc= None):
    """return paths and values for a given value.
    """
    # pylint: disable=redefined-outer-name
    internal_findval(txt.FINDVAL_SIMPLE, val_pattern= value,
                     pattern= pattern,
                     path_list= paths,
                     formatspec= formatspec,
                     sdc=sdc)

def ifindval(val_pattern, formatspec= "",
             pattern= None,
             paths= None,
             sdc= None):
    """return paths and values for a value matching an "i"-pattern.
    """
    # pylint: disable=redefined-outer-name
    internal_findval(txt.FINDVAL_IPATTERN, val_pattern= val_pattern,
                     pattern= pattern,
                     path_list= paths,
                     formatspec= formatspec,
                     sdc=sdc)

def rxfindval(val_pattern, formatspec="",
              pattern= None,
              paths= None,
              sdc= None):
    """return paths and values for a value matching a regexp.
    """
    # pylint: disable=redefined-outer-name
    internal_findval(txt.FINDVAL_REGEXP, val_pattern= val_pattern,
                     pattern= pattern,
                     path_list= paths,
                     formatspec= formatspec,
                     sdc=sdc)

def get(pattern, formatspec="", paths= None, sdc= None):
    """get a part of the structure for a given pattern."""
    # pylint: disable=redefined-outer-name
    val= txt.get(pattern= pattern, formatspec= formatspec,
                 paths= paths, sdc=sdc)
    if val is not None:
        print(val)

change= txt.change
put= txt.put
delete= txt.delete
link= txt.link
refresh_links= txt.refresh_links

def getlinks(path, formatspec="", include=None, exclude=None, sdc= None):
    """return links for a path."""
    print(txt.getlinks(path= path, formatspec= formatspec,
                       include= include, exclude= exclude, sdc= sdc))

def findlinks(pattern, formatspec="", include= None, exclude= None,
              sdc= None):
    """find links for a pattern."""
    print(txt.findlinks(pattern= pattern, formatspec= formatspec,
                        include= include, exclude= exclude,
                        sdc= sdc))

def typepaths(pattern="*", formatspec="", sdc= None):
    """find typepaths for a pattern."""
    print(txt.typepaths(pattern= pattern, formatspec= formatspec,
                        sdc= sdc))

def typefind(pattern, formatspec="", sdc= None):
    """find a type for a pattern."""
    print(txt.typefind(pattern= pattern, formatspec= formatspec, sdc= sdc))

def typeget(path, formatspec="", sdc= None):
    """get a type for a path."""
    print(txt.typeget(path= path, formatspec= formatspec, sdc= sdc))

typeput= txt.typeput
typeadditem= txt.typeadditem
typedelete= txt.typedelete
typedeleteitem= txt.typedeleteitem

def typecheck(sdc= None):
    """perform a typecheck on the StructuredDataContainer.
    """
    if txt.typecheck(sdc):
        print("all typechecks succeeded")
        return True
    return False

def typematch(path, formatspec="", sdc= None):
    """try to find a typecheck for the given path.
    """
    print(txt.typematch(path= path, formatspec= formatspec, sdc= sdc))
