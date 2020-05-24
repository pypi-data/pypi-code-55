# ================================================================
# lc.py:  alcune funzioni per lab2
# Date:     XX/5/2020
# Author:   Luca Ciucci
# Contact:  develop@lucaciucci99.com
# ================================================================

# ================================================================
#                            IMPORTS
# ================================================================

import pylab
import numpy
np = numpy
from scipy.optimize import curve_fit
from scipy.misc import derivative
from scipy import signal
from matplotlib import pyplot as plt
import threading
import time
import warnings
from uncertainties import ufloat
import inspect

# ////////////////////////////////////////////////////////////////
# ottieni il nome completo del file
def _path_to(fileName) :
    """
    ottieni il nome completo del file (inserisce .txt se necessario)
    """
    return 'a'
    if len(fileName) < 6 :
        return fileName + ".txt"
    if (fileName[-4] == ".") :
        return fileName
    else:
        return fileName + ".txt"

# ////////////////////////////////////////////////////////////////
def load(filename, **kwargs) :
    """
    Carica un file di dati in formato txt
    """
    return pylab.loadtxt(_path_to(filename), unpack = True, **kwargs)


# ////////////////////////////////////////////////////////////////
def figure(_plotter = plt, size = [], pltSizes = [1], spacings = []) :
    """
    Crea una figura e ritorna gli handle ai grafici.


    Parametri:
    - _plotter : oggetto che si occupa della cerazione del grafico
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

_basic_linear_python_fa_schifo_bisogna_fare_questo_obrobrio_perche_funzioni = lambda x, m, q : m*x*1e10 + q

# ////////////////////////////////////////////////////////////////
class Grafico :
    """
    Membri:

    """
    def __init__(self):
        self.fitParams.model = _basic_linear_python_fa_schifo_bisogna_fare_questo_obrobrio_perche_funzioni

    class _Data :
        xData = np.array([])
        dxData = np.array([])
        yData = np.array([])
        dyData = np.array([])

    class _FitParams :
        # funzione di fit
        params = np.array([1., 0.])
        model = _basic_linear_python_fa_schifo_bisogna_fare_questo_obrobrio_perche_funzioni
        fit_iter = 3
        absolute_sigma = False
        outliers = 3

        #perrors = [0.]
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

    def plot(self, _show = True, _timeout = None) :
        """
        disegna tutto secondo i parametri
        """

        fig = None
        upper = None# grafico superiore
        lower = None# grafico inferiore

        # crea la figura
        if (self.plotParams.plot_residui) :
            fig, plts = figure(size=self.plotParams.figure_size, pltSizes = [6, 3], spacings = [1])
            upper = plts[0]
            lower = plts[1]
        else :
            fig, plts = figure(size=self.plotParams.figure_size)
            upper = plts[0]

        if (len(self.data.xData) != len(self.data.yData)) :
            raise Exception("i dati x e y hanno dimensioni diverse")

        # disegna i dati
        _no_errors = True
        if (self.plotParams.plot_errors) :
            _no_errors = False
            if (len(self.data.xData) != len(self.data.dxData) or len(self.data.yData) != len(self.data.dyData)) :
                warnings.warn("gli errori hanno dimensione errata, non verranno disegnati")
                _no_errors = True
            else:
                upper.errorbar(self.data.xData, self.data.yData, self.data.dyData, self.data.dxData,
                    ls = self.plotParams.data_lineStyle, c = self.plotParams.data_color, marker = self.plotParams.data_marker, alpha = self.plotParams.data_alpha, label = "dati")
        else :
            _no_errors = True
        if (_no_errors) :
            upper.plot(self.data.xData, self.data.yData,
                ls = self.plotParams.data_lineStyle, c = self.plotParams.data_color, marker = self.plotParams.data_marker, alpha = self.plotParams.data_alpha, label = "dati")
        upper_Xlim = upper.get_xlim()
        upper_Ylim = upper.get_ylim()

        # modello
        _f = lambda x : self.fitParams.model(x, *self.fitParams.params)

        if (self.plotParams.plot_residui) :
            dw = np.sqrt(self.data.dyData**2 + (_f(self.data.xData + self.data.dxData) - _f(self.data.xData))**2)
            _residui = self.data.yData - _f(self.data.xData)
            if (self.plotParams.residui_normalizzati) :
                _residui = _residui / dw
                dw = dw*0. + 1.
            if (self.plotParams.plot_errors) :
                lower.errorbar(self.data.xData, _residui, dw,
                ls = self.plotParams.data_lineStyle, c = self.plotParams.data_color, marker = self.plotParams.data_marker, alpha = self.plotParams.data_alpha)
            else :
                lower.plot(self.data.xData, _residui,
                ls = self.plotParams.data_lineStyle, c = self.plotParams.data_color, marker = self.plotParams.data_marker, alpha = self.plotParams.data_alpha)
        
        # plotta funzione
        if (self.plotParams.plot_model) :
            xx = None
            if (self.plotParams.xLog) :
                xx = np.logspace(np.log10(upper_Xlim[0]), np.log10(upper_Xlim[1]), self.plotParams.function_samples)
            else :
                xx = np.linspace(upper_Xlim[0], upper_Xlim[1], self.plotParams.function_samples)
            yy = _f(xx)
            upper.plot(xx, yy, ls = self.plotParams.function_lineStyle, c = self.plotParams.function_color, alpha = self.plotParams.function_alpha, label = "modello")
            if (self.plotParams.plot_residui) :
                lower.plot(xx, xx*0, ls = self.plotParams.function_lineStyle, c = self.plotParams.function_color, alpha = self.plotParams.function_alpha)

            if (self.plotParams.function_intervalliConfidenza) :
                if (len(self.fitParams.pcov) != len(self.fitParams.params)) :
                    warnings.warn("la dimensione della pcov e' errata. Forse non e' stato eseguito il fit, le bande di confidenza non verranno plottate")
                else :
                    _errs = self._error_prop(xx, self.fitParams.model, self.fitParams.params, self.fitParams.pcov)
                    upper.fill_between(xx, yy + _errs, yy - _errs, color = self.plotParams.function_color, alpha = 0.25)
                    if (self.plotParams.plot_residui) :
                        if (self.plotParams.residui_normalizzati) :
                            warnings.warn("residui normalizzati attivi, non verranno plottate le bande di confidenza su residui")
                        else :
                            lower.fill_between(xx, _errs, -_errs, color = self.plotParams.function_color, alpha = 0.25)

        # reimposta i limiti corretti
        upper.set_xlim(upper_Xlim)
        upper.set_ylim(upper_Ylim)
        if (self.plotParams.plot_residui) :
            lower.set_xlim(upper_Xlim)

        # imposta le scale
        if (self.plotParams.xLog) :
            upper.set_xscale('log')
            if (self.plotParams.plot_residui) :
                lower.set_xscale('log')
        if (self.plotParams.yLog) :
            upper.set_yscale('log')

        # griglia
        if (self.plotParams.grid_on) :
            upper.grid(color='grey', linestyle='-', linewidth=1, alpha=0.5, which='major')
            upper.grid(color='grey', linestyle='-', linewidth=1, alpha=0.25, which='minor')
            upper.tick_params(direction='in', length=5, width=1., top=True, right=True)
            upper.tick_params(which='minor', direction='in', width=1., top=True, right=True)
            if (self.plotParams.plot_residui) :
                lower.grid(color='grey', linestyle='-', linewidth=1, alpha=0.5, which='major')
                lower.grid(color='grey', linestyle='-', linewidth=1, alpha=0.25, which='minor')

        # titolo
        upper.set_title(self.plotParams.title)

        # assi
        upper.set_xlabel(self.plotParams.nome_asse_x + " " + self.plotParams.unita_asse_x)
        upper.set_ylabel(self.plotParams.nome_asse_y + " " + self.plotParams.unita_asse_y)
        if (self.plotParams.plot_residui) :
                lower.set_xlabel(self.plotParams.nome_asse_x + " " + self.plotParams.unita_asse_x)
                if (self.plotParams.residui_normalizzati) :
                    lower.set_ylabel("residui normalizzati")
                else:
                    lower.set_ylabel("residui " + self.plotParams.unita_asse_y)

        # legenda
        if (self.plotParams.legenda_on) :
            upper.legend(loc = self.plotParams.loc_legenda)

        # TODO bellurie (tics, titolo, legenda)

        # mostra il grafico
        if (_show) :
            if _timeout is None :
                show(fig)
            else :
                show(fig, _timeout = _timeout)
        else :
            return fig, upper, lower

    def fit(self) :
        p_start = self.fitParams.params
        for i in range(0, self.fitParams.fit_iter) :
            if (len(self.data.dxData) != len(self.data.xData) or len(self.data.dyData) != len(self.data.xData)) :
                warnings.warn("Fit eseguito senza errori!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                self.fitParams.params, self.fitParams.pcov = curve_fit(self.fitParams.model, self.data.xData, self.data.yData, self.fitParams.params)
            else:
                _f = lambda x : self.fitParams.model(x, *self.fitParams.params)
                dw = np.sqrt(self.data.dyData**2 + (_f(self.data.xData + self.data.dxData) - _f(self.data.xData))**2)
                xx = []
                yy = []
                dw_tmp = []
                if (i > 0 and self.fitParams.outliers > 0) :
                    count = 0
                    for i in range(0, len(self.data.xData)) :
                        if (np.abs(_f(self.data.xData[i]) - self.data.yData[i]) <= self.fitParams.outliers) :
                            xx.append(self.data.xData[i])
                            yy.append(self.data.yData[i])
                            dw_tmp.append(dw[i])
                        else:
                            count = count + 1
                    print("outliers = %d, threashold = %f" %(count, self.fitParams.outliers))
                else:
                    xx = self.data.xData
                    yy = self.data.yData
                    dw_tmp = dw[i]
                self.fitParams.params, self.fitParams.pcov = curve_fit(self.fitParams.model, self.data.xData, self.data.yData, self.fitParams.params, dw, absolute_sigma = self.fitParams.absolute_sigma)
            print("fit step %i, chi2: %f" %(i, self._chi2()))
        
        # stampa i risultati
        pNames = self.fitParams.model.__code__.co_varnames[1:]
        print('funzione di fit:')
        print(inspect.getsource(self.fitParams.model))
        print("I parametri incogniti da fittare esano: ", pNames)
        print("I parametri di partenza erano: ", p_start)
        print("- parametri ricavati:")
        for i in range(0, len(pNames)) :
            print("    %s = " %pNames[i], ufloat(self.fitParams.params[i], np.sqrt(self.fitParams.pcov[i][i])))
            #print("    %s = %.16e +- %.3e" %(pNames[i], self.fitParams.params[i], np.sqrt(self.fitParams.pcov[i][i])))
        print("- Correlazioni")
        for i in range(0, len(pNames)) :
            for j in range(i + 1, len(pNames)) :
                print("    Corr(%s, %s) = %.2f" %(pNames[i], pNames[j], self.fitParams.pcov[i][j] / np.sqrt(self.fitParams.pcov[i][i] * self.fitParams.pcov[j][j])))
        print("- covMatrix:")
        print(self.fitParams.pcov)
        print("- absolute sigma: ", self.fitParams.absolute_sigma)
        ndof = len(self.data.xData) - len(pNames)
        print("- ndof = %d    (%d - %d)" %(ndof, len(self.data.xData),len(pNames)))
        print("- chi2 = %.1f" %(self._chi2()))
        print("- chi2 ridotto(chi2/ndof) = %.1f" %(self._chi2() / ndof))

            


    # --------------------------------
    #           private
    # --------------------------------

    def _error_prop(self, x, _f, popt, pcov) :
        sum_v = x*0
        for i in range(0, len(popt)) :
            for j in range(0, len(popt)) :
                def __f(t, r) :
                    p1 = np.array(popt)
                    p1[r] = p1[r] + t
                    return _f(x, *p1)
                fi = lambda t : __f(t, i)
                fj = lambda t : __f(t, j)
                dfi = derivative(fi, 0, 1e-6)
                dfj = derivative(fj, 0, 1e-6)
                sum_v = sum_v + dfi * dfj * pcov[i][j]
        return np.sqrt(sum_v)

    def _chi2(self) :
        _f = lambda x : self.fitParams.model(x, *self.fitParams.params)
        dw = np.sqrt(self.data.dyData**2 + (_f(self.data.xData + self.data.dxData) - _f(self.data.xData))**2)
        return (((_f(self.data.xData) - self.data.yData) / dw)**2).sum()