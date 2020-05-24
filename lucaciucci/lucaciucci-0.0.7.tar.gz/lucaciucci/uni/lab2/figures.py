# ================================================================
# lc.py:  alcune funzioni per lab2
# Date:     XX/6/2020
# Author:   Luca Ciucci
# Contact:  develop@lucaciucci99.com
# ================================================================

from matplotlib import pyplot as plt
import numpy as np

# ////////////////////////////////////////////////////////////////
def figure(_plotter = plt, size = [], pltSizes = [1], spacings = []) :
    """
    Crea una figura e ritorna gli handle ai grafici.


    Parametri:
    - _plotter : oggetto che si occupa della cerazione del grafico,
    default = matplotlib.pyplot
    - size = dimensione del grafico in pollici, default = [6.4, 4.8]
    - pltSizes = dimensione in altezza dei grafici
    - spacings = spazi tra i grafici
    """

    fig = None
    if (len(size) <= 2) :
        if (len(size) == 0) :
            fig = _plotter.figure()
        if (len(size) == 1) :
            fig = _plotter.figure(figsize=[size, size])
        if (len(size) == 2) :
            fig = _plotter.figure(figsize=size)
    else :
        raise Exception("la dimensione del grafico deve essere nel formato [x, y] in pollici")

    plts = []
    pos = 0
    gridsize = [int(np.sum(pltSizes) + np.sum(spacings)), int(1)]

    for i in range(0, len(pltSizes)) :
        plts.append(_plotter.subplot2grid(gridsize, (int(pos), 0), rowspan = int(pltSizes[i])))
        pos = pos + pltSizes[i]

        if (i < len(spacings)) :
            pos = pos + spacings[i]

    return fig, plts

# ////////////////////////////////////////////////////////////////
def close(_plotter = plt) :
    """
    chiudi i grafici
    """
    _plotter.close()

# ////////////////////////////////////////////////////////////////
def show(fig = None, _timeout = 3600, _plotter = plt) :
    """
    Mostra i grafici creati.

    Se fig = None allora mostra tutti i grafici,
    se fig != None allora mostra quel grafico e lo chiude
    in automatico dopo il timer.

    Params:
    - fig : figura da mostrare (mostra tutti se non fornito)
    - _timeout : timeout per la chiusura della figura, attivo
        solo se fig != None
    - _plotter : manager figure
    """

    if (fig is None) or _timeout <= 0 :
        _plotter.show()
        return

    m_timer = fig.canvas.new_timer(interval = 1000*_timeout)
    m_timer.add_callback(lambda : _plotter.close(fig))
    m_timer.start()

    _plotter.show()

_basic_linear_python_fa_schifo_bisogna_fare_questo_obrobrio_perche_funzioni = lambda x, m, q : m*x* + q

# ////////////////////////////////////////////////////////////////
class Grafico :
    """
    Si occupa di creare un grafico e fare fit.

    """

    class _Data :
        """
        Contenitore per i dati
        """
        x = np.array([])
        dx = np.array([])
        y = np.array([])
        dy = np.array([])

    class _FitParams :
        # funzione di fit
        params = np.array([1., 0.])
        model = _basic_linear_python_fa_schifo_bisogna_fare_questo_obrobrio_perche_funzioni
        fit_iter = 3
        absolute_sigma = False
        outliers = 0

        pcov = [[0.01, 0.], [0., 0.01]]

    class _PlotParams :
        # figura
        figure_size = []
        title = "Grafico "
        grid_on = True
        legenda_on = True
        loc_legenda = 'best'
        nome_asse_x = ''
        nome_asse_y = ''
        unita_asse_x = '[u.a.]'
        unita_asse_y = '[u.a.]'

        # scale
        xLog = False
        yLog = False

        # plot
        plot_residui = False
        residui_normalizzati = True
        plot_errors = True
        plot_model = False
        data_lineStyle = ''
        data_color = 'k'
        outliers_color = 'r'
        data_marker = '+'
        data_alpha = 1
        function_lineStyle = '-'
        function_color = 'r'
        function_alpha = 1
        function_intervalliConfidenza = True
        function_samples = 1000
    
    # membri
    data = _Data()
    fitParams = _FitParams()
    plotParams = _PlotParams()

