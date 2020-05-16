import matplotlib.pyplot as plt
import numpy as np
from ipythonblocks import BlockGrid
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap, ListedColormap


def hex_to_rgb(hex):

    hex = hex.replace("#", "")

    return tuple(int(hex[i:i+2], 16)/255. for i in (0, 2, 4))


class ColorMap(object):

    def __init__(self, *colors, discrete=False, name=None):

        self._colors = colors
        self._number = len(colors)

        if not discrete:

            self._cmap = LinearSegmentedColormap.from_list(name, self._colors)

        else:

            NotImplementedError()

        if name is not None:

            cm.register_cmap(name=name, cmap=self._cmap)

    def show_as_blocks(self):

        block_size = 100

        grid = BlockGrid(self._number, 1, block_size=block_size)

        for block, color in zip(grid, self._colors):
            block.rgb = color

        grid.show()

    @property
    def cmap(self):
        return self._cmap

    @classmethod
    def from_hex(cls, *hexs, discrete=False, name=None):

        rgb = [hex_to_rgb(hex) for hex in hexs]

        return cls(*rgb, discrete=discrete, name=name)


    @classmethod
    def from_palettable(cls, pallet, discrete=False):

        name = pallet.name
        rgb =  [hex_to_rgb(hex) for hex in pallet.hex_colors]

        return cls(*rgb, discrete=discrete, name=name)
        
