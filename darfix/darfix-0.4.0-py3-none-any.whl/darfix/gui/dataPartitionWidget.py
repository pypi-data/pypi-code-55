# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/


__authors__ = ["J. Garriga"]
__license__ = "MIT"
__date__ = "11/05/2020"

import logging

import numpy

from silx.gui import qt
from silx.gui.plot import Plot1D

from .operationThread import OperationThread

_logger = logging.getLogger(__file__)


class DataPartitionWidget(qt.QMainWindow):

    sigComputed = qt.Signal()

    def __init__(self, parent=None):
        qt.QMainWindow.__init__(self, parent)

        self._plot = Plot1D()
        self._plot.setDataMargins(0.05, 0.05, 0.05, 0.05)

        binsNumberLabel = qt.QLabel("Number of bins:")
        self.binsNumber = qt.QLineEdit("1")
        self.binsNumber.setToolTip("Number of bins of the histogram of intensities that \
            will be considered as low intensity data")
        self.binsNumber.setValidator(qt.QIntValidator())
        self.computeHistogram = qt.QPushButton("Compute histogram")
        self.computePartition = qt.QPushButton("Compute partition")
        widget = qt.QWidget(parent=self)
        layout = qt.QGridLayout()
        layout.addWidget(binsNumberLabel, 0, 0, 1, 1)
        layout.addWidget(self.binsNumber, 0, 1, 1, 1)
        layout.addWidget(self.computeHistogram, 0, 2, 1, 1)
        layout.addWidget(self.computePartition, 1, 2, 1, 1)
        layout.addWidget(self._plot, 2, 0, 1, 3)
        widget.setLayout(layout)
        widget.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
        self.setCentralWidget(widget)
        self._plot.hide()

    def _computeHistogram(self):
        self.computeHistogram.setEnabled(False)
        try:
            self._thread = OperationThread(self._dataset.compute_frames_intensity)
            self._thread.finished.connect(self._showHistogram)
            self._thread.start()
        except Exception as e:
            self.computeHistogram.setEnabled(True)
            raise e

    def _computePartition(self):
        self.computePartition.setEnabled(False)
        try:
            self._thread = OperationThread(self._dataset.partition_by_intensity)
            self._thread.setArgs(num_bins=int(self.binsNumber.text()))
            self._thread.finished.connect(self._filterData)
            self._thread.start()
        except Exception as e:
            self.computePartition.setEnabled(True)
            raise e

    def setDataset(self, dataset, indices=None, bg_indices=None, bg_dataset=None):
        """
        Dataset setter.

        :param Dataset dataset: dataset
        """
        self._dataset = dataset
        self.indices = indices
        self.bg_indices = bg_indices
        self.bg_dataset = bg_dataset
        self.computeHistogram.pressed.connect(self._computeHistogram)
        self.computePartition.pressed.connect(self._computePartition)

    def _showHistogram(self):
        """
        Plots the eigenvalues.
        """
        self._thread.finished.disconnect(self._showHistogram)
        self.computeHistogram.setEnabled(True)
        frames_intensity = self._thread.data
        self._plot.remove()
        self._plot.show()
        values, bins = numpy.histogram(frames_intensity, len(frames_intensity))
        self._plot.addHistogram(values, bins)

    def _filterData(self):
        """
        Plots the eigenvalues.
        """
        self._thread.finished.disconnect(self._filterData)
        self.computePartition.setEnabled(True)
        self.bg_indices, self.indices = self._thread.data
        self.sigComputed.emit()

    def getDataset(self):
        return self._dataset, self.indices, self.bg_indices, self. bg_dataset
