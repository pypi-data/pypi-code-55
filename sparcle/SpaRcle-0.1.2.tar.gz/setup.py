import sys 
from setuptools import setup, find_packages

setup(name='SpaRcle',
      version='0.1.2',
      #url='https://github.com/Monika0000/SpaRcle-2.0',
      license='MIT',
      author='Monika',
      author_email='rotaru5craft@gmail.com',
      description='Искусственный интеллект. Искорка :)',
      packages=['SpaRcle'],
      #packages=find_packages(exclude=['tests']),
      long_description="",
      include_package_data=True,
      #entry_points={
      #  "console_scripts": [
      #      "SpaRcle=SpaRcle.__init__:main",
      #  ]
      #},
      zip_safe=False)