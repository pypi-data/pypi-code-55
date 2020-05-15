#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

import abc
from datetime import datetime

import ROOT
import numpy

import wagascianpy.analysis.spill
import wagascianpy.database.wagascidb
import wagascianpy.plotting.colors
import wagascianpy.plotting.colors as colors
import wagascianpy.plotting.detector
import wagascianpy.plotting.graph
import wagascianpy.plotting.harvest
import wagascianpy.plotting.marker
import wagascianpy.utils.utils

# compatible with Python 2 *and* 3:
ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})


class Plotter(ABC):

    def __init__(self, output_path="./plot.png"):
        ROOT.gROOT.IsBatch()
        self._canvas = ROOT.TCanvas("canvas", "canvas", 1280, 720)
        self._title = ""
        self._graphs = []
        self._markers = []
        self._multi_graph = None
        self._draw_opts = "AL"
        self._output_path = output_path

    def template_plotter(self):
        self.set_title()
        self._graphs = self.setup_graphs()
        for graph in self._graphs:
            self.gather_data(graph)
        self.change_graph_titles(self._graphs)
        self.build_multigraph()
        self.add_run_markers()
        self.plot()

    @property
    def draw_options(self):
        return self._draw_opts

    @draw_options.setter
    def draw_options(self, draw_options):
        self._draw_opts = draw_options

    @abc.abstractmethod
    def set_title(self):
        pass

    @abc.abstractmethod
    def setup_graphs(self):
        pass

    @abc.abstractmethod
    def gather_data(self, graph):
        pass

    def build_multigraph(self):
        ROOT.gStyle.SetTitleFontSize(0.035)
        self._multi_graph = ROOT.TMultiGraph()
        ROOT.TGaxis.SetMaxDigits(3)
        for graph in self._graphs:
            self._multi_graph.Add(graph.make_tgraph())
        self._multi_graph.SetTitle(self._title)
        self._multi_graph.GetXaxis().SetNdivisions(9, 3, 0, ROOT.kTRUE)
        self._multi_graph.GetXaxis().SetTimeDisplay(1)
        self._multi_graph.GetXaxis().SetTimeFormat("#splitline{%d %b %Y}{%H:%M %Z}%F1970-01-01 00:00:00")
        self._multi_graph.GetXaxis().SetLabelOffset(0.03)

    def add_run_markers(self):
        pass

    def change_graph_titles(self, graphs):
        pass

    def make_run_markers(self):
        if hasattr(self, "_wagasci_database") and self._wagasci_database \
                and hasattr(self, "_start") and self._start and hasattr(self, "_stop"):
            start = self._start
            stop = self._stop
            with wagascianpy.database.wagascidb.WagasciDataBase(db_location=self._wagasci_database,
                                                                repo_location="") as db:
                if isinstance(start, int):
                    if not stop:
                        stop = db.get_last_run_number(only_good=False)
                    records = db.get_run_interval(run_number_start=start, run_number_stop=stop, only_good=False)
                else:
                    if not stop:
                        stop = datetime.now()
                    records = db.get_time_interval(datetime_start=start, datetime_stop=stop, only_good=False,
                                                   include_overlapping=False)
            counter = 0
            markers = []
            for record in records:
                marker = wagascianpy.plotting.marker.DoubleMarker(left_position=record["start_time"],
                                                                  right_position=record["stop_time"],
                                                                  left_text="WAGASCI run %s" % record["run_number"],
                                                                  right_text="",
                                                                  line_color=colors.Colors.Blue)
                if counter % 2 == 0:
                    marker.fill_color = colors.Colors.Azure.value
                else:
                    marker.fill_color = colors.Colors.Orange.value
                marker.transparency = 0.1
                markers.append(marker)
                counter += 1
            self._markers += markers
        else:
            raise RuntimeError("Cannot add run markers")

    def plot(self):
        self._multi_graph.Draw(self.draw_options)
        self._canvas.Update()
        tobjects = []
        for marker in self._markers:
            tobjects += marker.make_tobjects()
        for tobj in tobjects:
            tobj.Draw()
        self._canvas.Update()
        tlegend = ROOT.TLegend(0.13, 0.7, 0.4, 0.89)
        tlegend.SetFillColorAlpha(ROOT.kWhite, 1.)
        for graph in self._graphs:
            opt = "f"
            if "l" in self.draw_options.lower():
                opt += "l"
            if "p" in self.draw_options.lower():
                opt += "p"
            tlegend.AddEntry(graph.id, graph.title, opt)
        tlegend.Draw()
        self._canvas.Update()
        self._canvas.Print(self._output_path)


class BsdPlotter(Plotter, ABC):

    def __init__(self, output_path, bsd_database, bsd_repository, start,
                 stop=None, wagasci_database=None, t2krun=10):
        super(BsdPlotter, self).__init__(output_path=output_path)
        self._bsd_database = bsd_database
        self._bsd_repository = bsd_repository
        self._wagasci_database = wagasci_database
        self._t2krun = t2krun
        self._start = start
        self._stop = stop
        self._data_harvester = wagascianpy.plotting.harvest.Patron(
            start=start, stop=stop, wagasci_database=wagasci_database)
        self._bsd_harvester_class = None

    @abc.abstractmethod
    def set_title(self):
        pass

    @abc.abstractmethod
    def setup_graphs(self):
        pass

    def gather_data(self, graph):
        assert self._bsd_harvester_class is not None, \
            "Derived class must set the _bsd_harvester_class attribute"
        if graph.id != "BSD":
            raise ValueError("Wrong graph with title {} and ID {}".format(graph.title, graph.id))
        self._data_harvester.harvester = self._bsd_harvester_class(
            database=self._bsd_database, repository=self._bsd_repository, t2krun=self._t2krun)
        graph.xdata, graph.ydata = self._data_harvester.gather_data()


class BsdPotPlotter(BsdPlotter):

    def __init__(self, *args, **kwargs):
        super(BsdPotPlotter, self).__init__(*args, **kwargs)
        self._bsd_harvester_class = wagascianpy.plotting.harvest.BsdPotHarvester

    def set_title(self):
        self._title = "Delivered POT during run {};;POT".format(self._t2krun)

    def setup_graphs(self):
        graph = wagascianpy.plotting.graph.Graph("Delivered POT", "BSD")
        graph.color = wagascianpy.plotting.colors.Colors.Red.value
        return [graph]


class BsdSpillPlotter(BsdPlotter):

    def __init__(self, *args, **kwargs):
        super(BsdSpillPlotter, self).__init__(*args, **kwargs)
        self._bsd_harvester_class = wagascianpy.plotting.harvest.BsdSpillHarvester

    def set_title(self):
        self._title = "BSD spill history during run {};;spill number".format(self._t2krun)

    def setup_graphs(self):
        graph = wagascianpy.plotting.graph.Graph("BSD spill history", "BSD")
        graph.color = wagascianpy.plotting.colors.Colors.Red.value
        return [graph]


class WagasciPlotter(Plotter, ABC):

    def __init__(self, output_path, bsd_database, bsd_repository,
                 wagasci_database, wagasci_repository, start,
                 stop=None, topology=None, t2krun=10):
        super(WagasciPlotter, self).__init__(output_path=output_path)
        self._bsd_database = bsd_database
        self._bsd_repository = bsd_repository
        self._wagasci_database = wagasci_database
        self._wagasci_repository = wagasci_repository
        self._t2krun = t2krun
        self._start = start
        self._stop = stop
        self._data_harvester = wagascianpy.plotting.harvest.Patron(
            start=start, stop=stop, wagasci_database=wagasci_database)
        self._wagasci_harvester_class = None
        self._bsd_harvester_class = None
        self._topology = topology if topology is not None else wagascianpy.plotting.detector.Topology()

    @abc.abstractmethod
    def set_title(self):
        pass

    @abc.abstractmethod
    def setup_graphs(self):
        graphs = []
        for enabled_detector in self._topology.get_enabled():
            graph = wagascianpy.plotting.graph.Graph(enabled_detector.name)
            graph.color = enabled_detector.name
            graphs.append(graph)
        return graphs

    def gather_data(self, graph):
        if graph.id == "BSD":
            assert self._bsd_harvester_class is not None, \
                "Derived class must set the _bsd_harvester_class attribute"
            if not self._data_harvester.is_harvester_ready() or \
                    not isinstance(self._data_harvester.harvester, self._bsd_harvester_class):
                self._data_harvester.harvester = self._bsd_harvester_class(
                    database=self._bsd_database,
                    repository=self._bsd_repository,
                    t2krun=self._t2krun)
            graph.xdata, graph.ydata = self._data_harvester.gather_data()
        else:
            for enabled_detector in self._topology.get_enabled():
                if graph.id == enabled_detector.name:
                    assert self._wagasci_harvester_class is not None, \
                        "Derived class must set the _wagasci_harvester_class attribute"
                    if not self._data_harvester.is_harvester_ready() or \
                            not isinstance(self._data_harvester.harvester, self._wagasci_harvester_class):
                        self._data_harvester.harvester = self._wagasci_harvester_class(
                            database=self._wagasci_database,
                            repository=self._wagasci_repository,
                            t2krun=self._t2krun,
                            topology=self._topology)
                    graph.xdata, graph.ydata = self._data_harvester.gather_data(enabled_detector.name)


class WagasciPotPlotter(WagasciPlotter):

    def __init__(self, *args, **kwargs):
        super(WagasciPotPlotter, self).__init__(*args, **kwargs)
        self._wagasci_harvester_class = wagascianpy.plotting.harvest.WagasciPotHarvester
        self._bsd_harvester_class = wagascianpy.plotting.harvest.BsdPotHarvester

    def set_title(self):
        self._title = "#splitline{Accumulated POT for each subdetector during run %s}" \
                      "{after spill matching but before data quality};;POT" % str(self._t2krun)

    def add_run_markers(self):
        self.make_run_markers()

    def setup_graphs(self):
        graphs = super(WagasciPotPlotter, self).setup_graphs()
        bsd_graph = wagascianpy.plotting.graph.Graph("Delivered POT", "BSD")
        bsd_graph.color = wagascianpy.plotting.colors.Colors.Red.value
        graphs.append(bsd_graph)
        return graphs

    def change_graph_titles(self, graphs):
        bsd_graph = next((bsd_graph for bsd_graph in graphs if bsd_graph.id == "BSD"), None)
        if bsd_graph is None:
            return
        bsd_pot = numpy.amax(bsd_graph.ydata)
        bsd_graph.title += " = {:.2e} POT".format(bsd_pot)
        for igraph in [graph for graph in graphs if graph.id != "BSD"]:
            max_pot = numpy.amax(igraph.ydata)
            percent = 100 * float(max_pot) / float(bsd_pot)
            igraph.title += " {:.1f}%".format(percent)


class WagasciSpillPlotter(WagasciPlotter):

    def __init__(self, *args, **kwargs):
        super(WagasciSpillPlotter, self).__init__(*args, **kwargs)
        self._wagasci_harvester_class = wagascianpy.plotting.harvest.WagasciSpillHarvester

    def set_title(self):
        self._title = "#splitline{WAGASCI spill history during run %s}" \
                      "{before bit flip fixing};;spill number" % str(self._t2krun)

    def add_run_markers(self):
        self.make_run_markers()

    def setup_graphs(self):
        self.draw_options = "AP"
        graphs = super(WagasciSpillPlotter, self).setup_graphs()
        for graph in graphs:
            graph.yrange = wagascianpy.plotting.graph.Range(
                lower_bound=wagascianpy.analysis.spill.WAGASCI_MINIMUM_SPILL,
                upper_bound=wagascianpy.analysis.spill.WAGASCI_MAXIMUM_SPILL)

        return graphs


class WagasciFixedSpillPlotter(WagasciPlotter):

    def __init__(self, *args, **kwargs):
        super(WagasciFixedSpillPlotter, self).__init__(*args, **kwargs)
        self._wagasci_harvester_class = wagascianpy.plotting.harvest.WagasciFixedSpillHarvester

    def set_title(self):
        self._title = "#splitline{WAGASCI fixed spill history during run %s}" \
                      "{after bit flip fixing but before data quality};;spill number" % str(self._t2krun)

    def add_run_markers(self):
        self.make_run_markers()

    def setup_graphs(self):
        self.draw_options = "AP"
        return super(WagasciFixedSpillPlotter, self).setup_graphs()
