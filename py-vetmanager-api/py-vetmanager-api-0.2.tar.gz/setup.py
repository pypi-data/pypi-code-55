from setuptools import setup

setup(
    name='py-vetmanager-api',
    version='0.2',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=['tests', 'vetmanager'],
    url='https://github.com/otis22/PyVetmanagerApi',
    license='MIT',
    author='otis',
    author_email='vromanichev24@gmail.com',
    descriptions='Vetmanager Api for Python',
    install_requires=["requests"]
)
