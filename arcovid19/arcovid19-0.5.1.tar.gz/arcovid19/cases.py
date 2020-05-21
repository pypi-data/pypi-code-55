#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2020, Bruno Sanchez, Mauricio Koraj, Vanessa Daza,
#                     Juan B Cabral, Mariano Dominguez, Marcelo Lares,
#                     Nadia Luczywo, Dante Paz, Rodrigo Quiroga,
#                     Martín de los Ríos, Federico Stasyszyn
#                     Cristian Giuppone.
# License: BSD-3-Clause
#   Full Text: https://raw.githubusercontent.com/ivco19/libs/master/LICENSE


# =============================================================================
# DOCS
# =============================================================================

"""Utilities to Utility function to parse all the actual cases of the
COVID-19 in Argentina.

"""

__all__ = [
    "CODE_TO_POVINCIA",
    "D0", "Q1",
    "CasesPlot",
    "CasesFrame",
    "load_cases"]


# =============================================================================
# IMPORTS
# =============================================================================

import datetime as dt
import itertools as it

import logging

import numpy as np

import pandas as pd

import matplotlib.pyplot as plt

import unicodedata

from deprecated import deprecated

from . import cache, core


# =============================================================================
# CONSTANTS
# =============================================================================

CASES_URL = "https://github.com/ivco19/libs/raw/master/databases/cases.xlsx"


AREAS_POP_URL = 'https://github.com/ivco19/libs/raw/master/databases/extra/arg_provs.dat'  # noqa


LABEL_DATE_FORMAT = "%d.%b"


PROVINCIAS = {
    'CABA': 'CABA',
    'Bs As': 'BA',
    'Córdoba': 'CBA',
    'San Luis': 'SL',
    'Chaco': 'CHA',
    'Río Negro': 'RN',
    'Santa Fe': 'SF',
    'Tierra del F': 'TF',
    'Jujuy': 'JY',
    'Salta': 'SAL',
    'Entre Ríos': 'ER',
    'Corrientes': 'COR',
    'Santiago Est': 'SDE',
    'Neuquen': 'NQ',
    'Mendoza': 'MDZ',
    'Tucumán': 'TUC',
    'Santa Cruz': 'SC',
    'Chubut': 'CHU',
    'Misiones': 'MIS',
    'Formosa': 'FOR',
    'Catamarca': 'CAT',
    'La Rioja': 'LAR',
    'San Juan': 'SJU',
    'La Pampa': 'LPA'}


# this alias fixes the original typos
PROVINCIAS_ALIAS = {
    'Tierra del Fuego': "TF",
    'Neuquén': "NQ",
    "Santiago del Estero": "SDE"
}

#: List of Argentina provinces
CODE_TO_POVINCIA = {
    v: k for k, v in it.chain(PROVINCIAS.items(), PROVINCIAS_ALIAS.items())}


STATUS = {
    'Recuperado': 'R',
    'Recuperados': 'R',
    'Confirmados': 'C',
    'Confirmado': 'C',
    'Activos': 'A',
    'Muertos': 'D'}


#: Pandemia Start 2020-03-11
D0 = dt.datetime(year=2020, month=3, day=11)


#:  Argentine quarantine starts 2020-03-20
Q1 = dt.datetime(year=2020, month=3, day=20)


logger = logging.getLogger("arcovid19.cases")


# =============================================================================
# FUNCTIONS_
# =============================================================================

def safe_log(array):
    """Convert all -inf to 0"""
    with np.errstate(divide='ignore'):
        res = np.log(array.astype(float))
    res[np.isneginf(res)] = 0
    return res


# =============================================================================
# CASES
# =============================================================================

class CasesPlot(core.Plotter):

    default_plot_name_method = "curva_epi_pais"

    def _plot_df(
        self, *, odf, prov_name, prov_code,
        confirmed, active, recovered, deceased, norm=1.
    ):

        columns = {}
        if confirmed:
            cseries = odf.loc[(prov_code, 'C')][self.frame.dates].values
            columns[f"{prov_name} Confirmed"] = cseries / norm
        if active:
            cseries = odf.loc[(prov_code, 'A')][self.frame.dates].values
            columns[f"{prov_name} Active"] = cseries / norm
        if recovered:
            cseries = odf.loc[(prov_code, 'R')][self.frame.dates].values
            columns[f"{prov_name} Recovered"] = cseries / norm
        if deceased:
            cseries = odf.loc[(prov_code, 'D')][self.frame.dates].values
            columns[f"{prov_name} Deceased"] = cseries / norm
        pdf = pd.DataFrame(columns)
        return pdf

    @deprecated(version="0.5", reason="use curve_epi_country instead")
    def grate_full_period_all(self, *args, **kwargs):
        return self.curva_epi_pais(*args, **kwargs)

    @deprecated(version="0.5", reason="use curve_epi_province instead")
    def grate_full_period(self, *args, **kwargs):
        return self.curva_epi_provincia(*args, **kwargs)

    def curva_epi_pais(
        self, ax=None, argentina=True,
        exclude=None, log=False, norm=False,
        paint=None, count_days=None,
        **kwargs
    ):
        """
        method: full_period_normalized()

        This function plots the time series, similar to grate_full_period_all,
        but including a second axis and comments about the start of quarantine

        opciones para paint: pandemia, cuarentena

        opciones para count_days: pandemia, cuarentena

        """

        kwargs.setdefault("confirmed", True)
        kwargs.setdefault("active", False)
        kwargs.setdefault("recovered", False)
        kwargs.setdefault("deceased", False)
        exclude = [] if exclude is None else exclude
        if ax is None:
            ax = plt.gca()
            fig = plt.gcf()
            height = len(PROVINCIAS) - len(exclude) - int(argentina)
            height = 4 if height <= 0 else (height)
            fig.set_size_inches(12, height)

        if argentina:
            self.grate_full_period(provincia=None, ax=ax, **kwargs)

        exclude = [] if exclude is None else exclude
        exclude = [self.frame.get_provincia_name_code(e)[1] for e in exclude]

        ccolors = ['steelblue'] * 10 + ['peru'] * 10 + ['darkmagenta'] * 10
        cmarkers = ['o', '.', 'o', 'x', 'D']
        cstyles = ['-', '-', '--', '--', ':']
        cwidths = [2, 1, 1, 1, 2]
        cwidths = [3] * 2 + [1] * 7

        cfaces = ccolors[:]
        for i, _ in enumerate(cfaces):
            if i % 5 == 0 or i % 5 == 4:
                cfaces[i] = 'white'

        calpha = [1.0] * 5 + [1.0] * 5 + [1.0] * 5
        cmrkevry = [(2, 3), (3, 2), (1, 5)]

        icolors = it.cycle(ccolors)
        imarkers = it.cycle(cmarkers)
        istyles = it.cycle(cstyles)
        iwidths = it.cycle(cwidths)
        ifaces = it.cycle(cfaces)
        ialpha = it.cycle(calpha)
        imrkevry = it.cycle(cmrkevry)

        aesthetics = {}

        for code in sorted(CODE_TO_POVINCIA):
            if code in exclude:
                continue

            aesthetics['color'] = next(icolors)
            aesthetics['linewidth'] = next(iwidths)
            aesthetics['linestyle'] = next(istyles)
            aesthetics['marker'] = next(imarkers)
            aesthetics['markerfacecolor'] = next(ifaces)
            aesthetics['markeredgewidth'] = 1
            aesthetics['markersize'] = 6
            aesthetics['markevery'] = next(imrkevry)
            aesthetics['alpha'] = next(ialpha)

            mfc = aesthetics['markerfacecolor']
            mew = aesthetics['markeredgewidth']

            self.curva_epi_provincia(
                provincia=code, ax=ax,
                log=log, norm=norm,
                color=aesthetics['color'],
                linewidth=aesthetics['linewidth'],
                linestyle=aesthetics['linestyle'],
                marker=aesthetics['marker'],
                markerfacecolor=mfc,
                markeredgewidth=mew,
                markersize=aesthetics['markersize'],
                markevery=aesthetics['markevery'],
                alpha=aesthetics['alpha'],
                **kwargs)

        labels = [d.date() for d in self.frame.dates]
        ispace = int(len(labels) / 10)
        ticks = np.arange(len(labels))[::ispace]
        slabels = [lbl.strftime("%d.%b") for lbl in labels][::ispace]
        lmin = labels[0].strftime("%d.%b")
        lmax = labels[-1].strftime("%d.%b")

        ax.set_xticks(ticks=ticks)
        ax.set_xticklabels(labels=slabels, rotation=0, fontsize=16)
        ax.set_title(
            "COVID-19 crecimiento en Argentina, por provincia, entre "
            f"{lmin} and {lmax}", fontsize=16)
        ax.set_xlabel("Date", fontsize=16)
        ylabel = "Numero de casos acumulado"
        if norm:
            ax.set_ylabel(ylabel + " y normalizado", fontsize=16)
        else:
            ax.set_ylabel(ylabel, fontsize=16)
        ax.tick_params(axis='x', direction='in', length=8)
        if log:
            ax.set(yscale='log')

        # agregar eje x secundario
        if count_days == 'pandemia':

            t = np.array([(dd - D0).days for dd in self.frame.dates])

            ax2 = ax.twiny()
            ax2.set_xlim(min(t), max(t))
            ax2.set_xlabel("dias desde la declaracion de la pandemia (11/3)",
                           fontsize=16, color='blue')

            ax2.tick_params(axis='x', direction='in', length=10, pad=-28,
                            color='blue', labelcolor='blue', labelsize=16)

        if count_days == 'cuarentena':

            t = []
            d0 = dt.datetime.strptime("3/20/20", '%m/%d/%y')  # cuarentena
            for dd in self.frame.dates:
                elapsed_days = (dd - d0).days
                t.append(elapsed_days)
            t = np.array(t)

            ax2 = ax.twiny()
            ax2.set_xlim(min(t), max(t))
            ax2.set_xlabel("dias desde la cuarentena (20/3)",
                           fontsize=16, color='blue')

            ax2.tick_params(axis='x', direction='in', length=10, pad=-28,
                            color='blue', labelcolor='blue', labelsize=16)

        # pintar periodo de tiempo
        if (count_days == 'pandemia') or (count_days == 'cuarentena'):
            if paint == 'pandemia':
                q1 = dt.datetime.strptime("3/11/20", '%m/%d/%y')  # pandemia
                d_ini = (q1 - d0).days
                d_fin = ax2.get_xlim()[1]
                ax2.axvspan(d_ini, d_fin, alpha=0.1, color='yellow')

            if paint == 'cuarentena':
                q1 = dt.datetime.strptime("3/20/20", '%m/%d/%y')  # cuarentena
                d_ini = (q1 - d0).days
                d_fin = ax2.get_xlim()[1]
                ax2.axvspan(d_ini, d_fin, alpha=0.1, color='yellow')
        else:
            t = []
            d0 = dt.datetime.strptime("1/01/20", '%m/%d/%y')  # any day
            for dd in self.frame.dates:
                elapsed_days = (dd - d0).days
                t.append(elapsed_days)
            t = np.array(t)
            ax2 = ax.twiny()
            ax2.set_xlim(min(t), max(t))
            ax2.axis('off')

            if paint == 'pandemia':
                q1 = dt.datetime.strptime("3/11/20", '%m/%d/%y')  # pandemia
                d_ini = (q1 - d0).days
                d_fin = ax2.get_xlim()[1]
                ax2.axvspan(d_ini, d_fin, alpha=0.1, color='yellow')

            if paint == 'cuarentena':
                q1 = dt.datetime.strptime("3/20/20", '%m/%d/%y')  # cuarentena
                d_ini = (q1 - d0).days
                d_fin = ax2.get_xlim()[1]
                ax2.axvspan(d_ini, d_fin, alpha=0.1, color='yellow')

        return ax

    def curva_epi_provincia(
        self,
        provincia=None, confirmed=True,
        active=True, recovered=True, deceased=True,
        ax=None,
        log=False, norm=False,
        color=None, alpha=None,
        linewidth=None, linestyle=None,
        marker=None, markerfacecolor=None,
        markeredgewidth=None,
        markersize=None, markevery=None,
        **kwargs
    ):

        if provincia is None:
            prov_name, prov_c = "Argentina", "ARG"
        else:
            prov_name, prov_c = self.frame.get_provincia_name_code(provincia)

        # normalizacion a la poblacion de cada provincia
        norm_factor = 1.
        if norm:
            areapop = self.ctats.areapop
            population = areapop['pop'][areapop['key'] == prov_c].values[0]
            norm_factor = population / 1.e6

        ax = plt.gca() if ax is None else ax

        # preparar dataframe
        pdf = self._plot_df(
            odf=self.frame.df, prov_name=prov_name, prov_code=prov_c,
            confirmed=confirmed, active=active,
            recovered=recovered, deceased=deceased, norm=norm_factor)

        # atributos graficos
        aesthetics = {}
        aesthetics['color'] = None if color is None else color
        aesthetics['linewidth'] = None if linewidth is None else linewidth
        aesthetics['linestyle'] = None if linestyle is None else linestyle
        aesthetics['marker'] = None if marker is None else marker
        mfc = markerfacecolor
        aesthetics['markerfacecolor'] = None if mfc is None else mfc
        mew = markeredgewidth
        aesthetics['markeredgewidth'] = None if mew is None else mew
        aesthetics['markersize'] = None if markersize is None else markersize
        aesthetics['markevery'] = None if markevery is None else markevery
        aesthetics['alpha'] = None if alpha is None else alpha

        # hacer el grafico
        pdf.plot.line(ax=ax, **kwargs, **aesthetics)

        # elementos formales del grafico
        labels = [d.strftime(LABEL_DATE_FORMAT) for d in self.frame.dates]
        ispace = int(len(labels) / 10)
        ticks = np.arange(len(labels))[::ispace]
        slabels = [lbl for lbl in labels][::ispace]
        lmin = labels[0]
        lmax = labels[-1]

        ax.set_xticks(ticks=ticks)
        ax.set_xticklabels(labels=slabels, rotation=0, fontsize=16)
        ax.set_title(
            "COVID-19 crecimiento en Argentina, por provincia, entre "
            f"{lmin} and {lmax}", fontsize=16)
        ax.set_xlabel("Fecha", fontsize=16)
        ax.set_ylabel("N")
        ax.legend(loc='upper left', frameon=False,
                  borderaxespad=4,
                  ncol=2, handlelength=3)
        if log:
            ax.set(yscale='log')

        return ax

    def time_serie_all(
        self, ax=None, argentina=True,
        exclude=None, **kwargs
    ):
        kwargs.setdefault("confirmed", True)
        kwargs.setdefault("active", False)
        kwargs.setdefault("recovered", False)
        kwargs.setdefault("deceased", False)

        exclude = [] if exclude is None else exclude

        if ax is None:
            ax = plt.gca()
            fig = plt.gcf()

            height = len(PROVINCIAS) - len(exclude) - int(argentina)
            height = 4 if height <= 0 else (height)

            fig.set_size_inches(12, height)

        if argentina:
            self.time_serie(provincia=None, ax=ax, **kwargs)

        exclude = [] if exclude is None else exclude
        exclude = [self.frame.get_provincia_name_code(e)[1] for e in exclude]

        for code in sorted(CODE_TO_POVINCIA):
            if code in exclude:
                continue
            self.time_serie(provincia=code, ax=ax, **kwargs)

        labels = [d.strftime(LABEL_DATE_FORMAT) for d in self.frame.dates]
        ticks = np.arange(len(labels))

        ax.set_xticks(ticks=ticks)
        ax.set_xticklabels(labels=labels, rotation=45)

        ax.set_title(
            "COVID-19 cases by date in Argentina by Province\n"
            f"{labels[0]} - {labels[-1]}")
        ax.set_xlabel("Date")
        ax.set_ylabel("N")

        return ax

    def time_serie(
        self, provincia=None, confirmed=True,
        active=True, recovered=True, deceased=True,
        ax=None, **kwargs
    ):
        if provincia is None:
            prov_name, prov_c = "Argentina", "ARG"
        else:
            prov_name, prov_c = self.frame.get_provincia_name_code(provincia)

        ax = plt.gca() if ax is None else ax

        ts = self.frame.restore_time_serie()
        pdf = self._plot_df(
            odf=ts, prov_name=prov_name, prov_code=prov_c,
            confirmed=confirmed, active=active,
            recovered=recovered, deceased=deceased)
        pdf.plot.line(ax=ax, **kwargs)

        labels = [d.strftime(LABEL_DATE_FORMAT) for d in self.frame.dates]
        ticks = np.arange(len(labels))

        ax.set_xticks(ticks=ticks)
        ax.set_xticklabels(labels=labels, rotation=45)

        ax.set_title(
            f"COVID-19 cases by date in {prov_name}\n"
            f"{labels[0]} - {labels[-1]}")
        ax.set_xlabel("Date")
        ax.set_ylabel("N")

        ax.legend()

        return ax

    def barplot(
        self, provincia=None, confirmed=True,
        active=True, recovered=True, deceased=True,
        ax=None, **kwargs
    ):
        ax = plt.gca() if ax is None else ax

        if provincia is None:
            prov_name, prov_c = "Argentina", "ARG"
        else:
            prov_name, prov_c = self.frame.get_provincia_name_code(provincia)

        ts = self.frame.restore_time_serie()
        pdf = self._plot_df(
            odf=ts, prov_name=prov_name, prov_code=prov_c,
            confirmed=confirmed, active=active,
            recovered=recovered, deceased=deceased)

        pdf.plot.bar(ax=ax, **kwargs)

        ax.set_xlabel("Date")
        ax.set_ylabel("N")

        labels = [d.date() for d in self.frame.dates]
        ax.set_xticklabels(labels, rotation=45)
        ax.legend()

        return ax

    def boxplot(
        self, provincia=None, confirmed=True,
        active=True, recovered=True, deceased=True,
        ax=None, **kwargs
    ):
        ax = plt.gca() if ax is None else ax

        if provincia is None:
            prov_name, prov_c = "Argentina", "ARG"
        else:
            prov_name, prov_c = self.frame.get_provincia_name_code(provincia)

        ts = self.frame.restore_time_serie()
        pdf = self._plot_df(
            odf=ts, prov_name=prov_name, prov_code=prov_c,
            confirmed=confirmed, active=active,
            recovered=recovered, deceased=deceased)
        pdf.plot.box(ax=ax, **kwargs)

        ax.set_ylabel("N")

        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

        return ax


class CasesFrame(core.Frame):
    """Wrapper around the `load_cases()` table.

    This class adds functionalities around the dataframe.

    """

    plot_cls = CasesPlot

    @property
    def dates(self):
        """Returns the dates for which we have data.

        Useful to use as time column (row) list for wide (long) format.

        """
        return [
            adate for adate in self.df.columns
            if isinstance(adate, dt.datetime)]

    @property
    def tot_cases(self):
        """Returns latest value of total confirmed cases"""
        return self.df.loc[('ARG', 'C'), self.dates[-1]]

    def get_provincia_name_code(self, provincia):
        """Resolve and validate the name and code of a given provincia
        name or code.

        """
        def norm(text):
            text = text.lower()
            text = unicodedata.normalize('NFD', text)\
                .encode('ascii', 'ignore')\
                .decode("utf-8")
            return str(text)
        prov_norm = norm(provincia)
        for name, code in PROVINCIAS.items():
            if norm(name) == prov_norm or norm(code) == prov_norm:
                return CODE_TO_POVINCIA[code], code

        for alias, code in PROVINCIAS_ALIAS.items():
            if prov_norm == norm(alias):
                return CODE_TO_POVINCIA[code], code

        raise ValueError(f"Unknown provincia'{provincia}'")

    def restore_time_serie(self):
        """Retrieve a new pandas.DataFrame but with observations
        by Date.
        """
        def _cumdiff(row):
            shifted = np.roll(row, 1)
            shifted[0] = 0
            diff = row - shifted
            return diff

        idxs = ~self.df.index.isin([('ARG', 'growth_rate_C')])
        cols = self.dates

        uncum = self.df.copy()
        uncum.loc[idxs, cols] = uncum.loc[idxs][cols].apply(_cumdiff, axis=1)
        return uncum

    def last_growth_rate(self, provincia=None):
        """Returns the last available growth rate for the whole country
        if provincia is None, or for only the named region.

        """
        return self.grate_full_period(provincia=provincia)[self.dates[-1]]

    def grate_full_period(self, provincia=None):
        """Estimates growth rate for the period where we have data

        """
        # R0 de Arg sí es None
        if provincia is None:
            idx_region = ('ARG', 'growth_rate_C')
            return(self.df.loc[idx_region, self.dates[1:]])

        pcia_code = self.get_provincia_name_code(provincia)[1]

        idx_region = (pcia_code, 'C')

        I_n = self.df.loc[idx_region, self.dates[1:]].values.astype(float)
        I_n_1 = self.df.loc[idx_region, self.dates[:-1]].values.astype(float)

        growth_rate = np.array((I_n / I_n_1) - 1)
        growth_rate[np.where(np.isinf(growth_rate))] = np.nan

        return pd.Series(index=self.dates[1:], data=growth_rate)


def load_cases(cases_url=CASES_URL, areas_pop_url=AREAS_POP_URL, force=False):
    """Utility function to parse all the actual cases of the COVID-19 in
    Argentina.


    Parameters
    ----------

    cases_url: str
        The url for the excel table to parse. Default is ivco19 team table.

    areas_pop_url: str
        The url for the csv population table to parse.
        Default is ivco19 team table.

    force : bool (default=False)
        If you want to ignore the local cache and retrieve a new value.

    Returns
    -------

    CasesFrame: Pandas-DataFrame like object with all the arcovid19 datatabase.

        It features a pandas multi index, with the following hierarchy:

        - level 0: cod_provincia - Argentina states
        - level 1: cod_status - Four states of disease patients (R, C, A, D)

    """
    df_infar = cache.from_cache(
        tag="cases.load_cases", force=force,
        function=pd.read_excel, io=cases_url, sheet_name=0, nrows=96)

    areapop = cache.from_cache(
        tag="cases.load_caces[areapop]", force=force,
        function=pd.read_csv, filepath_or_buffer=areas_pop_url)

    # load table and replace Nan by zeros
    df_infar = df_infar.fillna(0)

    # Parsear provincias en codigos standard
    df_infar.rename(columns={'Provicia \\ día': 'Pcia_status'}, inplace=True)
    for irow, arow in df_infar.iterrows():
        pst = arow['Pcia_status'].split()
        stat = STATUS.get(pst[-1])

        pcia = pst[:-2]
        if len(pcia) > 1:
            provincia = ''
            for ap in pcia:
                provincia += ap + ' '
            provincia = provincia.strip()

        else:
            provincia = pcia[0].strip()

        provincia_code = PROVINCIAS.get(provincia)

        df_infar.loc[irow, 'cod_provincia'] = provincia_code
        df_infar.loc[irow, 'cod_status'] = stat
        df_infar.loc[irow, 'provincia_status'] = f"{provincia_code}_{stat}"

    # reindex table with multi-index
    index = pd.MultiIndex.from_frame(df_infar[['cod_provincia', 'cod_status']])
    df_infar.index = index

    # drop duplicate columns
    df_infar.drop(columns=['cod_status', 'cod_provincia'], inplace=True)
    cols = list(df_infar.columns)
    df_infar = df_infar[[cols[-1]] + cols[:-1]]

    # calculate the total number per categorie per state, and the global
    for astatus in np.unique(df_infar.index.get_level_values(1)):
        filter_confirmados = df_infar.index.get_level_values(
            'cod_status').isin([astatus])
        sums = df_infar[filter_confirmados].sum(axis=0)
        dates = [date for date in sums.index if isinstance(date, dt.datetime)]
        df_infar.loc[('ARG', astatus), dates] = sums[dates].astype(int)

        df_infar.loc[('ARG', astatus), 'provincia_status'] = f"ARG_{astatus}"

    n_c = df_infar.loc[('ARG', 'C'), dates].values
    growth_rate_C = (n_c[1:] / n_c[:-1]) - 1
    df_infar.loc[('ARG', 'growth_rate_C'), dates[1:]] = growth_rate_C

    return CasesFrame(df=df_infar, extra={"areapop": areapop})
