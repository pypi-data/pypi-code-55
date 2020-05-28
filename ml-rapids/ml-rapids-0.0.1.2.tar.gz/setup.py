import glob
import setuptools
import os

import numpy

FLAGS = ['-JSON_DLL_BUILD', '-DSTREAMDM_EXPORTS', '-fPIC', '-shared', '-std=c++11',
         '-D_GNU_SOURCE', '-D_FILE_OFFSET_BITS=64', '-D_LARGEFILE_SOURCE64', '-O3', '-DUNIX', '-lpython']

cpp_sources = glob.glob('./code/src/**/*.cpp', recursive=True)

swig_lib = setuptools.Extension(
    name='_streamdm',
    sources=[os.path.join('code', 'src', 'streamdm_wrap.cxx'),
             *cpp_sources,
             ],
    include_dirs=[numpy.get_include(), ],
    extra_compile_args=FLAGS,
)

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='ml-rapids',  # Replace with your own username
    version='0.0.1.2',
    author='Klemen Kenda',
    author_email='klemen.kenda@ijs.si',
    description='Incremental learning written in C++ exposed in Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='GPLv3',
    url='https://github.com/JozefStefanInstitute/ml-rapids',
    packages=setuptools.find_packages(),
    install_requires=['numpy', 'scikit-learn', ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    ext_modules=[swig_lib, ],
    extra_compile_args=FLAGS,
    python_requires='>=3.6',
)
