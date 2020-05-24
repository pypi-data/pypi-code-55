import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec

__all__ = [
    'get_figure',
    'vector_field_2d_system',
]

def vector_field_2d_system():
    pass


def get_figure(n_row, n_col, len_row=3, len_col=6):
    fig = plt.figure(figsize=(n_col * len_col, n_row * len_row), constrained_layout=True)
    gs = GridSpec(n_row, n_col, figure=fig)
    return fig, gs

