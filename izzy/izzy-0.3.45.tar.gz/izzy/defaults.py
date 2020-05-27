"""
defaults.py

Examples
--------

"""

import matplotlib.pyplot as plt


# Plot defaults
plot_defaults = {
    'add': False,
    'close': True,
    'color': None,
    'figsize': (20, 10),
    'style': 'solid',
    'title': None,
    'xlabel': None,
    'xmax': None,
    'xmin': None,
    'ylabel': None,
    'ymax': None,
    'ymin': None
}


# Allow users to set theme
def set_theme(theme='light', font_size=18):
    # Convert theme to lowercase
    theme = theme.lower()

    # Translate theme
    _theme = 'seaborn'
    if theme in ('dark', 'darcula'):
        _theme = 'dark_background'

    # Style defaults
    plt.style.use('default')
    plt.style.use(_theme)
    plt.rcParams.update({
        'axes.labelsize': font_size,
        'axes.titlesize': font_size,
        'figure.titlesize': font_size,
        'font.size': font_size,
        'legend.fontsize': font_size,
        'legend.title_fontsize': font_size,
        'xtick.labelsize': font_size,
        'ytick.labelsize': font_size
    })

    # If darcula, change some extra parameters
    if theme == 'darcula':
        plt.rcParams.update({
            'figure.facecolor': '#2b2b2b',
            'axes.facecolor': '#2b2b2b'
        })


# By default, set the theme to light
# TODO how to get latex axes and fonts?
set_theme('light')
