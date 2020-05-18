from distutils.command.install import install as distutils_install
from distutils.command.sdist import sdist as distutils_sdist
from distutils.errors import DistutilsExecError

from setuptools import setup

noop = lambda *x, **y: None

def hooked_distutils_class(orig, pre=noop, post=noop):
    class hooked(orig):
        def __init__(self, *args, 
                     **kwargs):
            super().__init__(*args, **kwargs)
            self.libvis_pre_hook = pre
            self.libvis_post_hook = post

        def run(self):
            self.libvis_pre_hook()
            super().run()
            self.libvis_post_hook()

    return hooked


def hook_setup(
    install=noop, pre_install=noop,
    sdist=noop, pre_sdist=noop
):
    def _setup(*args, **kwargs):
        defaults = {
            'cmdclass':{
                'install':hooked_distutils_class(
                    distutils_install,pre=pre_install, post=install
                ),
                'sdist':hooked_distutils_class(
                    distutils_sdist, pre=pre_sdist, post=sdist)
            }
        }
        defaults.update(kwargs)
        setup(*args, **defaults)
    return _setup
