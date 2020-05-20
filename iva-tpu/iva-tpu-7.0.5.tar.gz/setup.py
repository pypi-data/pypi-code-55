# coding: utf-8
"""Setup script for IVA TPU."""

from setuptools import find_packages, setup
from distutils.extension import Extension
from Cython.Build import cythonize

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='iva-tpu',
      packages=find_packages(where='src'),
      package_dir={'': 'src'},
      version="7.0.5",
      author="Maxim Moroz",
      author_email="m.moroz@iva-tech.ru",
      description="IVA TPU Python API",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="http://git.mmp.iva-tech.ru/tpu_sw/pytpu",
      install_requires=[
            'numpy>=1.14',
            'Cython'
      ],
      ext_modules=cythonize([
            Extension("iva_tpu.server.tpu", ['src/iva_tpu/server/tpu.pyx'], libraries=["tpu"]),
      ]),
      python_requires='>=3.6',
      )
