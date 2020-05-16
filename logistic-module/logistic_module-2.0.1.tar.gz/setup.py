from setuptools import setup
import os


setup(
  name='logistic_module',
  version= '2.0.1',
  description='Visualization of Mandelbrot fractal in 3D',
  url='https://github.com/hannabacave/Logistic_module',
  author='Cindy Delage, Hanna Bacave, Yassine Mimouni',
  packages=['logistic_module','logistic_module.LogisticEquation','logistic_module.Mandelbrot2D', 'logistic_module.Mandelbrot3D'],
  zip_safe=False,
  install_requires= ['matplotlib==3.1.2',
'numpy==1.18.1',
'numba==0.47.0',
'plotly==4.6.0',
'scipy==1.3.1',
'memory_profiler']
)
