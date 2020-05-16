from twitterhal.engine import TwitterHAL


__version__ = "0.7.0"
VERSION = tuple(map(int, __version__.split(".")))

__all__ = ["TwitterHAL", "__version__", "VERSION"]
