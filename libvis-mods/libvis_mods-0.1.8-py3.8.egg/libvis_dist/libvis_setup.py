from distutils.command.sdist import sdist as distutils_sdist

from setuptools import setup
from libvis_mods.tools.setuptools_hook import hooked_distutils_class
from libvis_mods.config_gen import read_config

if __name__ == '__main__':
    config = read_config('.')
    print('Config', config)

    def message():
       print("Preparing Module {modname}".format(**config))

    defaults = {
        'cmdclass':{
            'sdist':hooked_distutils_class(
                distutils_sdist, pre=message)
        }
    }

    defaults.update(config)
    config = defaults
    config['name'] = config.get('modname')
    config['packages'] = [config['name']]
    print('config setup', config)
    setup(**config)
