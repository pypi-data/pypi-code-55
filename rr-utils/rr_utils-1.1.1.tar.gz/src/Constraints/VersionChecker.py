from enum import Enum

from Constraints.BaseChecker import _BaseChecker
from Constraints.Exceptions import CheckerError
from Version.Version import Version


class VersionToCheck(Enum):
    Python = 1,
    OpenCV = 2,
    NumPy = 3,


class VersionChecker(_BaseChecker):
    def __init__(self, expected_version: Version, module: VersionToCheck):
        super().__init__()
        self._expected_version = expected_version
        self._module = module

    def check(self):
        getter_dic = {
            VersionToCheck.Python: self._get_python_version,
            VersionToCheck.OpenCV: self._get_open_cv_version,
            VersionToCheck.NumPy: self._get_numpy_version,
        }

        version = getter_dic[self._module]()
        self._check_version(version)

    def _check_version(self, current_version):
        if not current_version.compare(self._expected_version, length=len(self._expected_version)):
            raise CheckerError(self._module.name, self._expected_version, current_version)

    @staticmethod
    def _get_python_version():
        import sys
        current_version = sys.version_info
        current_version = Version([current_version[i] for i in range(3)])
        return current_version

    @staticmethod
    def _get_open_cv_version():
        import cv2 as cv
        return Version(cv.__version__)

    @staticmethod
    def _get_numpy_version():
        import numpy
        return Version(numpy.version.version)
