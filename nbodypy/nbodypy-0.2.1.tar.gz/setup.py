from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='nbodypy',
      version='0.2.1',
      description='Package for N-body problem, and RC3BP',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://plmlab.math.cnrs.fr/mchupin/nbody',
      author='Maxime Chupin',
      author_email='chupin@ceremade.dauphine.fr',
      license='GNU GPLv3',
      packages=find_packages(exclude=['test*','bacasable']),
      install_requires=[
          'numpy',
          'matplotlib',
          'scipy',
      ],
      python_requires='>=3.6',
)
