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

def _read_reqs(relpath):
    fullpath = os.path.join(os.path.dirname(__file__), relpath)
    with open(fullpath) as f:
        return [s.strip() for s in f.readlines()
                if (s.strip() and not s.startswith("#"))]

_REQUIREMENTS_TXT = _read_reqs("requirements.txt")
_INSTALL_REQUIRES = [l for l in _REQUIREMENTS_TXT if "://" not in l]

setuptools.setup(
    name = "fwg",
    version="0.2.8",
    author="Thomas Ricatte",
    install_requires=_INSTALL_REQUIRES,
    data_files=[('.', ['requirements.txt'])],
    description="Fast sliced wasserstein distance matrix computation",
    ext_modules=[extension_mod]
)