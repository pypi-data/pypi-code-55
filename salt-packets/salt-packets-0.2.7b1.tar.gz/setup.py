from setuptools import setup, find_packages
from salt_packets.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()


setup(
    name='salt-packets',
    version=VERSION,
    description='portable, reusable, self-managed salt projects',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Leeward Bound',
    author_email='lee@netprophet.tech',
    url='https://code.netprophet.tech/netp/salt-packets',
    license='unlicensed',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'salt-packets': []},
    include_package_data=True,
    install_requires = [
        'cement==3.0.4',
        'jinja2',
        'pyyaml',
        'colorlog',
        'colored',
        'pyfiglet',
        'python-dotenv',
        'influxdb',
    ],
    entry_points="""
        [console_scripts]
        salt-packets = salt_packets.main:main
    """,
)
