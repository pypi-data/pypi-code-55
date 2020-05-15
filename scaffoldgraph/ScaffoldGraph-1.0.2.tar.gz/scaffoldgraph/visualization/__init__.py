"""
scaffoldgraph.visualization
"""
try:
    from IPython.core.display import display, HTML
    from IPython import get_ipython
    have_ipython = True
except ImportError:
    have_ipython = False


def initjs():
    assert have_ipython, "IPython must be installed to use initjs()"
