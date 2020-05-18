from distutils.command.install import install as install_orig
from distutils.errors import DistutilsExecError

from setuptools import setup

noop = lambda *x, **y: None

def get_class(orig, pre=noop, post=noop):
    class hooked_distutils_class(orig):
        def __init__(self, *args, 
                     **kwargs):
            super().__init__(*args, **kwargs)
            self.libvis_pre_hook = pre
            self.libvis_post_hook = post
            self._args = args
            self._kwargs = kwargs

        def run(self):
            self.libvis_pre_hook()
            super().run()
            self.libvis_post_hook()

    return hooked_distutils_class

