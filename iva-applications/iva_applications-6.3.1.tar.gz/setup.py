# coding: utf-8
"""Setup script for IVA NN applications service."""

from setuptools import find_packages, setup

setup(name='iva_applications',
      version='6.3.1',
      author='IVA Technologies',
      author_email='engineering@iva-tech.ru',
      packages=find_packages(where='src'),
      package_dir={'': 'src'},
      install_requires=[
            'matplotlib',
            'Pillow',
            'opencv-python',
            'scipy',
            'numpy',
            'scikit-image',
            'keras==2.2.4'
      ])
