from setuptools import setup
from os.path import join, dirname

setup(name='saladware',
      version='0.5.4.1',
      description='two bears',
      long_description=open(join(dirname(__file__), "README.md")).read(),
      packages=['saladware'],
      author='SALAD37',
      author_email='nonemovo@gmail.com',
      zip_safe=False,
      license="MIT")