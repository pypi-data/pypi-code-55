#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

from enum import Enum

import ROOT
from six import string_types
import wagascianpy.plotting.detector


class Colors(Enum):
    Red = ROOT.kRed
    Green = ROOT.kGreen
    Blue = ROOT.kBlue
    Orange = ROOT.kOrange
    Cyan = ROOT.kCyan
    Black = ROOT.kBlack
    Azure = ROOT.kAzure

    @classmethod
    def get_by_dif(cls, dif_id):
        if dif_id in [0, 1, "0", "1"]:
            return cls.get_by_detector("WallMRD north")
        elif dif_id in [2, 3, "2", "3"]:
            return cls.get_by_detector("WallMRD south")
        elif dif_id in [4, 5, "4", "5"]:
            return cls.get_by_detector("WAGASCI upstream")
        elif dif_id in [6, 7, "6", "7"]:
            return cls.get_by_detector("WAGASCI downstream")
        return cls.Black

    @classmethod
    def get_by_detector(cls, detector):
        name = ""
        if isinstance(detector, wagascianpy.plotting.detector.Detector):
            name = detector.name
        elif isinstance(detector, string_types):
            name = detector
        else:
            TypeError("Wrong type : {}".format(type(detector).__name__))
        if name == "WallMRD north":
            return cls.Green
        elif name == "WallMRD south":
            return cls.Cyan
        elif name == "WAGASCI upstream":
            return cls.Orange
        elif name == "WAGASCI downstream":
            return cls.Blue
        return cls.Black
