"""
Docstrings and decorators for some conversion methods
"""
# MATLAB
from textwrap import dedent

DOC_MATLAB_PARAMS = """append: bool
    If true and a file exists under ``output``, append to that file.
    Otherwise the file will be overwritten
format: {'5', '4'}
    Format of file to write. ``'5'`` for MATLAB 5 to 7.2, ``'4'`` for
    MATLAB 4
longNames: bool
    If true, allow variable names to reach 63 characters,
    which works with MATLAB 7.6+. Otherwise, maximum length is
    31 characters
compress: bool
    If true, compress matrices on write
oned: {'row', 'col'}:
    Write one-dimensional arrays as row vectors if
    ``oned=='row'`` (default), or column vectors
"""

def matlabExporter(f):
    doc = f.__doc__
    if '{matlab_params}' in doc:
        f.__doc__ = dedent(doc).replace('{matlab_params}', DOC_MATLAB_PARAMS)
    return f
