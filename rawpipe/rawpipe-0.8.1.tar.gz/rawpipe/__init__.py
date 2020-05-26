"""A collection of camera raw processing algorithms.

A collection of reference ISP algorithms, sufficient for producing a reasonably
good looking image from raw sensor data. Each algorithm takes in a frame in RGB
or raw format and returns a modified copy of the frame. The frame is expected to
be a NumPy float array with either 2 or 3 dimensions, depending on the function.
Some of the algorithms can be applied in different orders (demosaicing before or
after linearization, for example), but the reference ordering is as shown below.

Example:
  raw = rawpipe.algs.downsample(raw, iterations=2)
  raw = rawpipe.algs.linearize(raw, blacklevel=64, whitelevel=1023)
  rgb = rawpipe.algs.demosaic(raw, "RGGB")
  rgb = rawpipe.algs.lsc(rgb, my_vignetting_map)
  rgb = rawpipe.algs.lsc(rgb, my_color_shading_map)
  rgb = rawpipe.algs.resize(rgb, 400, 300)
  rgb = rawpipe.algs.wb(rgb, [1.5, 2.0])
  rgb = rawpipe.algs.ccm(rgb, my_3x3_color_matrix)
  rgb = rawpipe.algs.tonemap(rgb, "Reinhard")
  rgb = rawpipe.algs.chroma_denoise(rgb)
  rgb = rawpipe.algs.gamma(rgb, "sRGB")
  rgb = rawpipe.algs.quantize(rgb, 255)

Example:
  raw = rawpipe.verbose.linearize(raw)
  raw = rawpipe.silent.demosaic(raw, "RGGB")
"""

from .rawpipe import Algorithms

__version__ = "0.8.1"
__all__ = ["Algorithms"]

verbose = Algorithms(verbose=True)  # pylint: disable=invalid-name
silent = Algorithms(verbose=False)  # pylint: disable=invalid-name
algs = silent  # pylint: disable=invalid-name
