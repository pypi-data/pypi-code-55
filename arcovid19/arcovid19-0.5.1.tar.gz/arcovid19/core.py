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

"""Core functionalities for arcovid19

"""

__all__ = ["Frame", "Plotter"]


# =============================================================================
# IMPORTS
# =============================================================================

import abc
import logging

import attr


# =============================================================================
# CONSTANTS
# =============================================================================

logger = logging.getLogger("arcovid19.core")


# =============================================================================
# CASES
# =============================================================================

@attr.s(repr=False)
class Plotter(metaclass=abc.ABCMeta):

    frame = attr.ib()

    @abc.abstractproperty
    def default_plot_name_method(self):
        pass

    def __repr__(self):
        return f"CasesPlot({hex(id(self.frame))})"

    def __call__(self, plot_name=None, ax=None, **kwargs):
        """x.__call__() == x()"""
        plot_name = plot_name or self.default_plot_name_method

        if plot_name.startswith("_"):
            raise ValueError(f"Invalid plot_name '{plot_name}'")

        plot = getattr(self, plot_name)
        ax = plot(ax=ax, **kwargs)
        return ax


@attr.s(repr=False)
class Frame(metaclass=abc.ABCMeta):

    df = attr.ib()
    extra = attr.ib(factory=dict)
    plot = attr.ib(init=False)

    @abc.abstractproperty
    def plot_cls(self):
        pass

    @plot.default
    def _plot_default(self):
        plot_cls = self.plot_cls
        return plot_cls(frame=self)

    def __dir__(self):
        """x.__dir__() <==> dir(x)"""
        return super().__dir__() + dir(self.df)

    def __repr__(self):
        """x.__repr__() <==> repr(x)"""
        return repr(self.df)

    def __getattr__(self, a):
        """x.__getattr__(y) <==> x.y

        Redirect all te missing calls first to extra and then
        to the internal dataframe.

        """
        if a in self.extra:
            return self.extra[a]
        return getattr(self.df, a)

    def __getitem__(self, k):
        """x.__getitem__(y) <==> x[y]"""
        return self.df.__getitem__(k)
