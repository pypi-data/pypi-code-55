"""XML-RPC functions.
"""

import StructuredData.Classes as SD
from StructuredData.internal import ManagedStore
import StructuredData.SDshelllibBase as base
import StructuredData.SDshelllibFun as fun
import StructuredData.SDshelllibTxt as txt

__version__="5.1" #VERSION#

assert __version__==SD.__version__
assert __version__==ManagedStore.__version__
assert __version__==base.__version__
assert __version__==fun.__version__
assert __version__==txt.__version__

# pylint: disable= invalid-name

# time in seconds elements are kept in the store when they are not acessed:
_keep_time= 600

data_store= ManagedStore.Store(_keep_time)

def _sdc_register(sdc, user_key= None):
    """create a key for an sdc."""
    if user_key is None:
        keep_forever= False
    else:
        keep_forever= True
    sdc_key= data_store.new(user_key= user_key, keep_forever= keep_forever)
    data_store.set(sdc_key, sdc)
    return sdc_key

def _sdc_get(sdc_key):
    """get an sdc from a key or create it.
    """
    if not sdc_key:
        fun.error(ValueError, "sdc key must be a non-empty string")
        return None
    return data_store.get(sdc_key)

def _struc2sym(struc):
    if isinstance(struc, list):
        if len(struc)==1:
            if isinstance(struc[0], str):
                return fun.global_sym(struc[0])
    return struc
def _sym2struc(sym):
    if isinstance(sym, SD.SpecialKey):
        return [repr(sym)]
    return sym

#install hooks:
fun.sdc_register= _sdc_register
fun.sdc_get     = _sdc_get

fun.struc2sym   = _struc2sym
fun.sym2struc   = _sym2struc

fun.std_return  = "ok" # standard return type instead of <None>

symbol_list= base.module_functions({"fun":fun, "txt":txt})
