import sys, os
import setuptools
# from setuptools import setup, find_namespace_packages
import pathlib
import glob

install_requires = []
tests_require = []
dev_requires = install_requires + tests_require + ["documenteer[pipelines]"]
tools_path = pathlib.PurePosixPath(setuptools.__path__[0])
base_prefix = pathlib.PurePosixPath(sys.base_prefix)
data_files_path = tools_path.relative_to(base_prefix).parents[1]
idl_files = glob.glob("idl/*.idl")

setuptools.setup(
    name="ts_idl",
    description="Contains helper functions for the generated idl library by ts_sal.",
    # install_requires=install_requires,
    package_dir={"": "python"},
    packages=setuptools.find_namespace_packages(where="python"),
    data_files=[(os.path.join(data_files_path, "qos"), ["qos/DDS_DefaultQoS_All.xml"]),
                (os.path.join(data_files_path, "idl"), idl_files)],
    include_package_data=True,
    # scripts=[],
    # tests_require=tests_require,
    extras_require={"dev": dev_requires},
    license="GPL",
    project_url={
        "Bug Tracker": "https://jira.lsstcorp.org/secure/Dashboard.jspa",
        "Source Code": "https://github.com/lsst-ts/ts_idl",
    }
)
