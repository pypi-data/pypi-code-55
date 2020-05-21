#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2020, Bruno Sanchez, Mauricio Koraj, Vanessa Daza,
#                     Juan B Cabral, Mariano Dominguez, Marcelo Lares,
#                     Nadia Luczywo, Dante Paz, Rodrigo Quiroga,
#                     Martín de los Ríos, Federico Stasyszyn,
#                     Cristian Giuppone.
# License: BSD-3-Clause
#   Full Text: https://raw.githubusercontent.com/ivco19/libs/master/LICENSE


# =============================================================================
# DOCS
# =============================================================================

"""Core functionalities for arcovid19

"""

__all__ = ["wavid19"]


# =============================================================================
# IMPORTS
# =============================================================================

import io
import inspect
import datetime as dt

import jinja2

import matplotlib.pyplot as plt

import mpld3

import flask
from flask.views import View

from flask_babel import lazy_gettext as _

import pandas as pd

from .. import (
    __doc__ as ARCOVID19_RESUME,
    __version__ as ARCOVID19_VERSION)

from ..models import load_infection_curve, InfectionCurve
from . import forms


# =============================================================================
# BASE CLASS
# =============================================================================

class TemplateView(View):

    def get_template_name(self):
        return self.template_name

    def get_context_data(self):
        return {}

    def render_template(self, context):
        return flask.render_template(self.get_template_name(), **context)

    def dispatch_request(self):
        context = self.get_context_data()
        return self.render_template(context)


# =============================================================================
# VIEWS
# =============================================================================

class InfectionCurveView(TemplateView):

    methods = ['GET', 'POST']
    template_name = "InfectionCurve.html"

    def subplots(self):
        return plt.subplots(frameon=False, figsize=(12, 8))

    def _get_img(self, fig):
        buf = io.StringIO()

        fig.tight_layout()
        fig.savefig(buf, format='svg')
        svg = buf.getvalue()
        buf.close()

        return jinja2.Markup(svg)

    def get_img(self, fig):
        html = mpld3.fig_to_html(fig)
        return jinja2.Markup(html)

    def make_plots(self, result):
        fig_linear, ax_linear = self.subplots()
        result.plot(ax=ax_linear)

        fig_log, ax_log = self.subplots()
        result.plot(ax=ax_log, log=True)

        return {
            _("Linear"): self.get_img(fig_linear),
            _("Log"): self.get_img(fig_log)
        }

    def get_context_data(self):
        context_data = {}

        form = forms.InfectionCurveForm()

        if flask.request.method == "POST" and form.validate_on_submit():

            # get all the data as string
            data = form.data.copy()

            # remove crftokern
            data.pop("csrf_token", None)

            # extract the model method name and the method from the class
            method_name = data.pop("model")
            method = getattr(InfectionCurve, method_name)

            # extract all the parameters for the model itself
            parameters = list(inspect.signature(method).parameters)[1:]
            model_params = {p: data.pop(p) for p in parameters}

            # remove all unused models params
            # TODO: remove all unused models params

            # instantiate the curve
            curve = load_infection_curve(**data)

            # get the result
            result = method(curve, **model_params)

            # create the plots
            context_data["plots"] = self.make_plots(result)

            # add the results to the context
            context_data["result"] = result

        context_data["form"] = form
        return context_data


class DownloadView(InfectionCurveView):

    methods = ['POST']
    content_type = (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    def dispatch_request(self):
        context_data = self.get_context_data()

        result = context_data["result"]

        now = dt.datetime.now().isoformat()
        fname = f"arcovid19_{result.model_name}_{now}.xlsx"

        # the containers
        fileobj = io.BytesIO()
        writer = pd.ExcelWriter(fileobj)

        # write the result
        result.to_excel(writer, sheet_name="Data")

        # retrieve th config
        config_data = context_data["form"].data.copy()
        config_data.pop("csrf_token", None)

        config = pd.DataFrame([config_data]).T
        config.index.name = "Attribute"
        config.columns = ["Value"]
        config.to_excel(writer, sheet_name="Config")

        # write to the object
        writer.save()

        response = flask.make_response(fileobj.getvalue())
        response.headers.set('Content-Type', self.content_type)
        response.headers.set(
            'Content-Disposition', 'attachment', filename=fname)

        return response


# =============================================================================
# Blueprint
# =============================================================================

#: Flask blueprint with the views implemented in arcovid19.
wavid19 = flask.Blueprint("arcovid19", "arcovid19.web.bp")


@wavid19.context_processor
def inject_arcovid19():
    return {
        "ARCOVID19_RESUME": ARCOVID19_RESUME,
        "ARCOVID19_VERSION": ARCOVID19_VERSION}


wavid19.add_url_rule(
    '/', view_func=InfectionCurveView.as_view("index"))
wavid19.add_url_rule(
    '/icurve', view_func=InfectionCurveView.as_view("icurve"))
wavid19.add_url_rule(
    '/download_model', view_func=DownloadView.as_view("download_model"))
