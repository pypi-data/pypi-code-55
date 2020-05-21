#! /usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import salami
__doc__ = salami.__doc__

setup(name = 'salami',
      version = salami.__version__,
      packages = ["salami"],
      package_dir = {"salami" : "salami"},
      package_data = {"salami" : ["E*_P*/kfactor_weights.hdf5", "E*_P*/kfactor_objects.pkl",
                                  "E*_P*/feature_scaler.pkl", "E*_P*/xsec_scaler.pkl"]}, #< TODO: remove when all pickled
      scripts = ["salami-predict"],
      install_requires = ["pyslha", "tensorflow", "keras", "scikit-learn", "h5py"],
      author = 'Andy Buckley, Abhijeet Gangan, Jack Murphy',
      author_email = 'andy.buckley@cern.ch',
      description = 'Lightweight NLO BSM cross-sections, to go',
      long_description = __doc__,
      keywords = 'supersymmetry susy slha hep physics particle cross-section xsec prospino',
      license = 'GPL')
