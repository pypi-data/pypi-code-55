"""
Color management. Colors are handled nicely in seaborn. For a quicker acces,
we mix the seaborn color palette with the way colors handled in matplotlib.
E.g. we can define our own color + the seaborn colors in the palette, but if 
they are not found this will automatically fall back to matplotlib
"""

import seaborn as sb

from . import Logger

class ColorDict(dict):
    """
    Sole purpose is not to throw an error in case 
    a key does not exist, but to return the key instead.
    This basically comes down to if a color is not 
    prepdefined, then we rely on matplotlib to find 
    it with the key instead.
    """

    def __getitem__(self, item):
        """
        Do not throw a key error in case a key does not 
        exist.
        """
        if item in self:
            return self.get(item)
        else:
            return item

def get_color_palette(name="dark"):
    """
    Load a color pallete. This will get the predefined color palette, but
    returns a ColorDict instead, which allows for transparent pass through
    of non-exisiting color names.
    We will only allow for the first 9 colors of the specified seaborn
    color palette. 
    It will also offer a color accessible by the key 'inhibited', which 
    can be used to mark 'forbidden' regions in a plot.

    Keyword Args:
        name (str): A string which is passed though seaborn.color_palette

    Returns:
        HErmes.plotting.plot_colors.ColorDict
    """
    color_palette = ColorDict()
    color_palette.update(dict([k for k in zip([j for j in range(9)],sb.color_palette(name))]))
    color_palette['prohibited'] = sb.color_palette("deep")[3]
    return color_palette
    
############################################
