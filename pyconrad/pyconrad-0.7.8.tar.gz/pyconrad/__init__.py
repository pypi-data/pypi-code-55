# Copyright (C) 2010-2017 - Andreas Maier
# CONRAD is developed as an Open Source project under the GNU General Public License (GPL-3.0)

# all non-underscored names are exported unless __all__ is defined

import pkg_resources

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = 'unknown'


from jpype import JDouble, JArray, JInt, JString, JShort, JProxy, JByte, JBoolean, JChar, JLong, JFloat, JClass, JIterator, java, JPackage, attachThreadToJVM, JException, detachThreadFromJVM
import jpype
import jpype.imports
from ._pygrid import PyGrid
from pyconrad._pyconrad import setup_pyconrad, start_gui, start_reconstruction_pipeline_gui, is_initialized, is_gui_started, terminate_pyconrad
from pyconrad._classgetter import ClassGetter
from pyconrad.constants import java_float_dtype
from pyconrad._imageutils import imshow, show_everything, to_conrad_grid
import pyconrad.config
import jpype.imports
import pyconrad.phantoms

jpype.imports.registerDomain('edu')

try:
    import pyconrad.opencl
except:
    pass

jpype.imports.registerDomain('edu')
jpype.imports.registerDomain('ij')


def edu():
    if not is_initialized():
        raise pyconrad._pyconrad.PyConradNotInitializedError()

    return JPackage('edu')


def ij():

    if not is_initialized():
        raise pyconrad._pyconrad.PyConradNotInitializedError()

    return JPackage('ij')


def stanfordrsl():
    if not is_initialized():
        raise pyconrad._pyconrad.PyConradNotInitializedError()

    return JPackage('edu.stanford.rsl')


def close_all_windows():
    import pyconrad
    pyconrad.ij().WindowManager.closeAllWindows()


def tile(always=None):
    import pyconrad
    pyconrad.ij().IJ.run('Tile')
    if always is not None:
        import pyconrad._imageutils
        pyconrad._imageutils._always_use_tile = always


def cascade(always=None):
    import pyconrad
    pyconrad.ij().IJ.run('Cascade')
    if always is not None:
        import pyconrad._imageutils
        pyconrad._imageutils._always_use_tile = not always
