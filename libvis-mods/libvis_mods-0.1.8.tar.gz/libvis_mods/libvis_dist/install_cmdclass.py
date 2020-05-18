from distutils.command.install import install as install_orig
from distutils.errors import DistutilsExecError

from setuptools import setup

class install(install_orig):

    def run(self):
        try:
            self.spawn(['make', 'install'])
        except DistutilsExecError:
            self.warn('listing directory failed')
        super().run()


