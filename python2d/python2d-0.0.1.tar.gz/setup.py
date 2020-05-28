from setuptools import setup

setup(name='python2d',
      version='0.0.1',
      description='Python library to easily create 2d games',
      url='http://github.com/greencarrot5/python-2d-game-library',
      author='greencarrot5',
      author_email="seppevanammel@gmail.com",
      license='MIT',
      packages=['python2d'],
      install_requires=[
          "pillow"
      ],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
      zip_safe=False)
