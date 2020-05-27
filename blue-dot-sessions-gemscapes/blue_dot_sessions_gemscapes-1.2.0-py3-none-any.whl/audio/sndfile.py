import warnings
try:
    import scikits.audiolab as audiolab
    Sndfile = audiolab.Sndfile
except:
    warnings.warn("Couldn't import scikits.audiolab -- using pysndfile instead")
    from .pysndfile_wrapper import Sndfile
