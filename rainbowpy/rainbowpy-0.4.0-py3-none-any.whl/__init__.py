from rainbowpy.colormap import ColorMap
from rainbowpy.generate_maps_from_config import add_custom_cmaps

add_custom_cmaps()


from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
