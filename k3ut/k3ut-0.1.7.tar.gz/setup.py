import setuptools
setuptools.setup(
    name="k3ut",
    packages=["k3ut"],
    version="0.1.7",
    license='MIT',
    description='unittest util',
    long_description='# k3ut\n\n[![Build Status](https://travis-ci.com/pykit3/k3ut.svg?branch=master)](https://travis-ci.com/pykit3/k3ut)\n\nUnittest util functions for [pykit3] packages.\n\nYou do not need this repo unless you are a pykit3 developer.\n\nTODO: add doc\n\n[pykit3]: https://github.com/pykit3/pykit3\n',
    long_description_content_type="text/markdown",
    author='Zhang Yanpo',
    author_email='drdr.xp@gmail.com',
    url='https://github.com/drmingdrmer/k3ut',
    keywords=['unittest', 'logging', 'timer'],
    python_requires='>=3.0',

    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
    ] + ['Programming Language :: Python :: 3.4', 'Programming Language :: Python :: 3.5', 'Programming Language :: Python :: 3.6', 'Programming Language :: Python :: 3.7', 'Programming Language :: Python :: 3.8', 'Programming Language :: Python :: Implementation :: PyPy'],
)
