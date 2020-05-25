# TODO: Fill out this file with information about your package

# HINT: Go back to the object-oriented programming lesson "Putting Code on PyPi" and "Exercise: Upload to PyPi"

# HINT: Here is an example of a setup.py file
# https://packaging.python.org/tutorials/packaging-projects/
from setuptools import setup

setup(name='bike_geo',
      version='0.4',
      description='Calculates actual stack and reach, and other bike geometry',
      packages=['bike_geo'],
      author = 'Matt Bray',
      author_email = 'blazetolliver@icloud.com',
      zip_safe=True)