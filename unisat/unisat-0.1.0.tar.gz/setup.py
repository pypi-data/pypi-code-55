from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='unisat',
    version='0.1.0',
    description='UniSat Software Environtment for Python',
    long_description=readme,
    author='Yaakov Azat',
    author_email='yaakovazat@gmail.com',
    url='https://github.com/unisatkz/USK',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)