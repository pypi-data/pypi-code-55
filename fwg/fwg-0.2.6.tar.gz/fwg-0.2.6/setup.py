import setuptools
from distutils.core import setup, Extension
import sysconfig
import numpy
import os
import platform

extra_compile_args = ["-std=c++11", "-O2"]
extra_link_args = ["-std=c++11"]

if "BOOST_ROOT" in os.environ:
    extra_compile_args += [f"-I{os.environ['BOOST_ROOT']}"]

if platform.system() == "Darwin":
    extra_compile_args += ["-stdlib=libc++", "-mmacosx-version-min=10.9"]
    extra_link_args += ["-stdlib=libc++", "-mmacosx-version-min=10.9"]

# the c++ extension module
extension_mod = Extension(
    name="fwg",
    sources=["fwgmodule.cpp", "fwg.cpp"],
    language="c++",
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args,
    include_dirs=[".", numpy.get_include()],
)

setup(
    name = "fwg",
    version="0.2.6",
    author="Thomas Ricatte",
    description="Fast sliced wasserstein distance matrix computation",
    ext_modules=[extension_mod]
)