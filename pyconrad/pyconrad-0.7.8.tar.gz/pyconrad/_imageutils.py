# Copyright (C) 2010-2017 - Andreas Maier
# CONRAD is developed as an Open Source project under the GNU General Public License (GPL-3.0)

import inspect
import os
import re
import sys
import time
import warnings
from datetime import datetime
from os.path import join

import jpype
import numpy as np

import pyconrad

try:
    import pycuda.gpuarray as gpuarray
except ImportError:
    pass

_always_use_tile = os.environ.get('PYCONRAD_ALWAYS_USE_TILE', True)
PYCONRAD_DUMP_DIR = os.environ.get('PYCONRAD_DUMP_DIR', None)
if PYCONRAD_DUMP_DIR:
    os.makedirs(PYCONRAD_DUMP_DIR, exist_ok=True)
PYCONRAD_DUMP_EXT = os.environ.get('PYCONRAD_DUMP_EXT', 'tif')


class ImageUtil:

    ########################
    #  Convert Grid/numpy  #
    ########################

    @staticmethod
    def grid_from_numpy(grid):
        return np.ndarray.view(pyconrad.PyGrid.from_numpy(grid))

    @staticmethod
    def numpy_from_grid(ndarray):
        return np.ndarray.view(pyconrad.PyGrid.from_grid(ndarray))

    #################
    #  Save Images  #
    #################

    @staticmethod
    def save_grid_as_tiff(grid, path):
        jpype.JPackage(
            'edu').stanford.rsl.conrad.utils.ImageUtil.saveAs(grid, path)

    @staticmethod
    def save_numpy_as_tiff(array, path):
        grid = ImageUtil.grid_from_numpy(array)
        jpype.JPackage(
            'edu').stanford.rsl.conrad.utils.ImageUtil.saveAs(grid, path)

    #################
    #  Load Images  #
    #################

    @staticmethod
    def grid_from_tiff(path):
        ij = jpype.JPackage('ij').IJ.openImage(path)
        if not ij:
            raise RuntimeError('Error opening file \'%s\'' % path)
        grid = jpype.JPackage(
            'edu').stanford.rsl.conrad.utils.ImageUtil.wrapImagePlus(ij)
        return grid

    @staticmethod
    def array_from_tiff(path):
        ij = jpype.JPackage('ij').IJ.openImage(path)
        if not ij:
            raise RuntimeError('Error opening file \'%s\'' % path)
        grid = jpype.JPackage(
            'edu').stanford.rsl.conrad.utils.ImageUtil.wrapImagePlus(ij)
        return ImageUtil.numpy_from_grid(grid)


def _get_dump_filename(title):
    if PYCONRAD_DUMP_DIR:
        return join(PYCONRAD_DUMP_DIR, f'{title}_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")}.{PYCONRAD_DUMP_EXT}')
    else:
        return None


def to_conrad_grid(img, dump_if_numpy_file=None):

    if isinstance(img, pyconrad.edu().stanford.rsl.conrad.data.numeric.NumericGrid):
        return img
    elif isinstance(img, pyconrad.PyGrid):
        return img.grid
    elif 'torch.Tensor' in str(type(img)):
        array = img.cpu().detach().numpy()
    elif isinstance(img, np.ndarray) or hasattr(img, '__array__'):
        array = np.array(img)
    elif 'pycuda' in sys.modules and isinstance(img, gpuarray.GPUArray):
        array = img.get()
    elif isinstance(img, (list, tuple, set)):
        array = np.stack(img)
    else:
        raise TypeError('Unsupported Type: %s' % type(img))

    if dump_if_numpy_file:
        try:
            import skimage.io
            skimage.io.imsave(dump_if_numpy_file, array)
        except Exception as e:
            warnings.warn(f'Failed to dump image "{dump_if_numpy_file}":\n{e}')

    grid = pyconrad.PyGrid.from_numpy(array).grid
    return grid


def show_everything(wait_key_press=False, wait_window_close=False):
    previous_frame = inspect.currentframe().f_back
    locals = previous_frame.f_locals

    if wait_key_press or wait_window_close:
        (filename, line_number, function_name, lines, index) = inspect.getframeinfo(previous_frame)
        print(f'{filename}:{line_number}: {lines[0]}')

    imshow(locals,
           silent_fail=True,
           wait_key_press=wait_key_press,
           wait_window_close=wait_window_close)


def imshow(img,
           title="",
           wait_key_press=False,
           wait_window_close=False,
           origin=None,
           spacing=None,
           auto_assume_channels=True,
           lut=None,
           run=None,
           run_args="",
           silent_fail=False):
    """Shows an image in ImageJ

    Arguments:
        img {np.ndarray,} -- img can be a numpy array, a CONRAD grid, a pycuda.gpuarray.Gpuarray

    Keyword Arguments:
        title {str} -- Title of ImageJ window (default: {""})
        wait_key_press {bool} -- Stops program until key in console is pressed (default: {False})
        wait_window_close {bool} -- Stops program until display window in closed (default: {False})
        origin {[type]} -- Origin of array for metric coordinates in ImageJ (default: {None})
        spacing {[type]} -- Spacing of array for metric coordinates in ImageJ (default: {None})
        auto_assume_channels {bool} -- Try to guess when the last dimension could be channel data
                                         (much smaller size than other dimensions)
        lut {str} -- Apply a lut. Choose from "Fire", "Grays", "Ice", "Spectrum", "3-3-2 RGB", "Red", "Blue", "Cyan",
                     "Magenta", "Yellow", "Red/Green" (alias for run)
        run {str} -- Run a ImageJ command with `run_args`
        run_args {str} -- Commands for ImageJ command `run_args`
    """

    import ij
    if 'PYCONRAD_HEADLESS' in os.environ:
        return

    if not title:
        try:
            previous_frame = inspect.currentframe().f_back
            (filename, line_number, function_name, lines, index) = inspect.getframeinfo(previous_frame)
            match = re.search(r'\(.+\)', lines[0], re.DOTALL)
            title = match[0][1:-1]
        except Exception:
            pass

    class ImageListener:
        def __init__(self, image_plus=None):

            self.is_open = True
            self.image_plus = image_plus

        def imageOpened(self, imagePlus):
            pass

        def imageClosed(self, imagePlus):
            if imagePlus == self.image_plus or not self.image_plus:
                self.is_open = False

        def imageUpdated(self, imagePlus):
            pass

    if isinstance(img, dict):
        for i, (k, v) in enumerate(img.items()):
            imshow(v, str(k),
                   i == len(img.items()) - 1 and wait_key_press,
                   i == len(img.items()) - 1 and wait_window_close,
                   origin,
                   spacing,
                   auto_assume_channels,
                   lut,
                   run,
                   run_args,
                   silent_fail)

        if _always_use_tile:
            pyconrad.tile()
        return

    if not pyconrad.is_gui_started():
        pyconrad.start_gui()

    if isinstance(img, np.ndarray) and auto_assume_channels:
        if all(s > 10 for s in img.shape[:-1]) and img.shape[-1] < 10:
            img = np.moveaxis(img, -1, 0)

    if silent_fail:
        try:
            grid = to_conrad_grid(img, _get_dump_filename(title))
        except Exception:
            return
    else:
        grid = to_conrad_grid(img, _get_dump_filename(title))

    if origin:
        assert len(
            origin) == grid.ndim, 'spacing\'s length needs to match the number of dimensions of the grid'
        grid.setOrigin(origin)
    else:
        origin = list(grid.getOrigin())
    if spacing:
        assert len(
            spacing) == grid.ndim, 'origins\'s length needs to match the number of dimensions of the grid'
        grid.setSpacing(spacing)
    else:
        spacing = list(grid.getSpacing())
        if all(s == 0 for s in spacing):
            spacing = (1,) * max(grid.ndim, 3)

    listener = ImageListener()
    proxy = jpype.JProxy(ij.ImageListener, inst=listener)
    pyconrad.ij().ImagePlus.addImageListener(proxy)

    window = pyconrad.ij().WindowManager.getImage(title) if title else None

    if window:
        imageplus = pyconrad.stanfordrsl().conrad.utils.ImageUtil.wrapGrid(grid, title)
        window.setImage(imageplus)
    else:
        grid.show(title)
        window = pyconrad.ij().WindowManager.getImage(
            title) if title else ij.WindowManager.getCurrentWindow().getImagePlus()

    calibration = window.getCalibration()
    calibration.pixelWidth = spacing[-1]
    if len(spacing) >= 2:
        calibration.pixelHeight = spacing[-2]
    if len(spacing) >= 3:
        calibration.pixelDepth = spacing[-3]
    calibration.xOrigin = 0
    if len(origin) >= 2:
        calibration.yOrigin = 0
    if len(origin) >= 3:
        calibration.zOrigin = 0

    if run:
        ij.IJ.run(window, run, run_args)
        window.close()

    if lut:
        ij.IJ.run(window, lut, '')

    if listener and wait_window_close:
        while listener.is_open:
            time.sleep(0.1)
        pyconrad.ij().WindowManager.closeAllWindows()

    if wait_key_press:
        input("press key")

    if _always_use_tile:
        pyconrad.tile()
