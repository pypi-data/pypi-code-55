from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='Tbqc',
      version='0.0.2',
      description='Taiwan Bartender Quizdata Crawler',
      url='https://github.com/dapingtai/Tw-Bartender-Quizdata-crawler/',
      author='HungChang',
      author_email='zero100x@gmail.com',
      license='BSD-5',
      packages=['Tbqc'],
      python_requires='>=3.6',
)
