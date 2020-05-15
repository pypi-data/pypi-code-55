#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

import ROOT
from six import string_types

import wagascianpy.plotting.colors


class Marker(object):

    def __init__(self, left_position=None, left_text=None,
                 line_color=wagascianpy.plotting.colors.Colors.Black.value):
        self._line_color = None
        self._left_text = None
        self._left_position = None
        self.line_color = line_color
        self.left_text = left_text
        self.left_position = left_position

    @property
    def left_text(self):
        return self._left_text

    @left_text.setter
    def left_text(self, left_text):
        self._left_text = left_text

    @property
    def left_position(self):
        return self._left_position

    @left_position.setter
    def left_position(self, left_position):
        self._left_position = left_position

    @property
    def line_color(self):
        return self._line_color

    @line_color.setter
    def line_color(self, line_color):
        if isinstance(line_color, int):
            self._line_color = line_color
        elif isinstance(line_color, wagascianpy.plotting.colors.Colors):
            self._line_color = line_color.value
        elif isinstance(line_color, string_types):
            self._line_color = wagascianpy.plotting.line_colors.Colors.get_by_detector(line_color).value
        else:
            raise TypeError("line color type is unknown {}".format(type(line_color).__name__))

    def make_tobjects(self):
        ROOT.gPad.Modified()
        ROOT.gPad.Update()
        y_minimum = ROOT.gPad.GetUymin()
        y_maximum = ROOT.gPad.GetUymax()
        x_minimum = ROOT.gPad.GetUxmin()
        x_maximum = ROOT.gPad.GetUxmax()
        tline = ROOT.TLine(self.left_position, y_minimum, self.left_position, y_maximum)
        tline.SetLineColor(self.line_color)
        tline.SetLineWidth(1)
        tline.SetLineStyle(2)
        ttext = ROOT.TText(self.left_position + (x_maximum - x_minimum) * 0.005,
                           0.98 * y_maximum, self.left_text)
        ttext.SetTextAngle(90)
        ttext.SetTextAlign(33)
        ttext.SetTextSize(0.03)
        ttext.SetTextColor(self.line_color)
        return [ttext, tline]


class DoubleMarker(Marker):

    def __init__(self, left_position=None, left_text=None,
                 line_color=wagascianpy.plotting.colors.Colors.Black.value,
                 right_position=None, right_text=None):
        super(DoubleMarker, self).__init__(left_position=left_position,
                                           left_text=left_text, line_color=line_color)
        self._right_text = None
        self._right_position = None
        self.right_text = right_text
        self.right_position = right_position
        self._transparency = None
        self._fill_color = None

    @property
    def right_text(self):
        return self._right_text

    @right_text.setter
    def right_text(self, right_text):
        self._right_text = right_text

    @property
    def right_position(self):
        return self._right_position

    @right_position.setter
    def right_position(self, right_position):
        self._right_position = right_position

    @property
    def fill_color(self):
        return self._fill_color

    @fill_color.setter
    def fill_color(self, fill_color):
        if isinstance(fill_color, int):
            self._fill_color = fill_color
        elif isinstance(fill_color, wagascianpy.plotting.colors.Colors):
            self._fill_color = fill_color.value
        elif isinstance(fill_color, string_types):
            self._fill_color = wagascianpy.plotting.fill_colors.Colors.get_by_detector(fill_color).value
        else:
            raise TypeError("fill color type is unknown {}".format(type(fill_color).__name__))

    @property
    def transparency(self):
        return self._transparency

    @transparency.setter
    def transparency(self, transparency):
        if not 0 < transparency < 1:
            raise ValueError("Transparence must be a percentage from zero to one")
        self._transparency = transparency

    def make_tobjects(self):
        left_markers = super(DoubleMarker, self).make_tobjects()
        y_minimum = ROOT.gPad.GetUymin()
        y_maximum = ROOT.gPad.GetUymax()
        x_minimum = ROOT.gPad.GetUxmin()
        x_maximum = ROOT.gPad.GetUxmax()
        tline = ROOT.TLine(self.right_position, y_minimum, self.right_position, y_maximum)
        tline.SetLineColor(self.line_color)
        tline.SetLineWidth(1)
        tline.SetLineStyle(2)
        ttext = ROOT.TText(self.right_position + (x_maximum - x_minimum) * 0.005,
                           0.98 * y_maximum, self.right_text)
        ttext.SetTextAngle(90)
        ttext.SetTextAlign(33)
        ttext.SetTextSize(0.03)
        ttext.SetTextColor(self.line_color)
        right_markers = []
        if self.fill_color:
            tbox = ROOT.TBox(self.left_position, y_minimum, self.right_position, y_maximum)
            tbox.SetLineWidth(0)
            tbox.SetFillColorAlpha(self.fill_color + 1, self.transparency)
            right_markers.append(tbox)
        right_markers.append(tline)
        right_markers.append(ttext)
        return right_markers + left_markers
