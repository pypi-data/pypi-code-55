from setuptools import Extension, setup, find_packages
import warnings
import numpy

with open('README.md') as f:
    README = f.read()

ext_modules = [
    Extension("ddop.utils.criterion",
              ['ddop/utils/criterion.pyx'],
              include_dirs=[numpy.get_include()])]


def get_extensions(ext_modules):
    try:
        from Cython.Build import cythonize
        ext_modules = cythonize(ext_modules)
    except ImportError:
        # Cython is not installed.
        warnings.warn("cython is not installed. Only pure python subpckages will be available.")
        ext_modules = None
    return ext_modules


setup(
    name='ddop',
    version='v0.3.8',
    url='',
    license='MIT',
    author='Andreas Philippi',
    author_email='',
    description='Package for data-driven operations management',
    long_description=README,
    include_package_data=True,
    packages=find_packages(),
    package_data={"ddop.utils": ["criterion.pyx"]},
    python_requires=">=3.6",
    setup_requires=['Cython','numpy'],
    install_requires=['Cython', 'scikit-learn>=0.23.0', 'pandas', 'PuLP==2.0',
                      'tensorflow==2.1.0', 'Keras==2.3.1',
                      'numpy==1.18.2', 'scipy==1.4.1', 'lightgbm>=2.3.1'],
    ext_modules=get_extensions(ext_modules),
)
