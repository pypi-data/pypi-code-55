from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

setup(
    name='rubus-cli',
    version='1.0.5',
    description='CLI to interact with a Rubus API instance',
    long_description=readme,
    author='xiorcale',
    author_email='quentin.vaucher@protonmail.com',
    url='https://github.com/xiorcale/rubus-cli',
    packages=find_packages(exclude=('tests', 'docs')),
    python_requires='>=3.6',
    install_requires=[
        'Click',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        rubus=rubus.rubus:cli
    '''
)
