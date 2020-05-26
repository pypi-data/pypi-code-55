import setuptools
setuptools.setup(
    name="k3time",
    packages=["k3time"],
    version="0.1.0",
    license='MIT',
    description='Time convertion utils',
    long_description="# k3time\n\n[![Build Status](https://travis-ci.com/pykit3/k3time.svg?branch=master)](https://travis-ci.com/pykit3/k3time)\n[![Documentation Status](https://readthedocs.org/projects/k3time/badge/?version=stable)](https://k3time.readthedocs.io/en/stable/?badge=stable)\n[![Package](https://img.shields.io/pypi/pyversions/k3time)](https://pypi.org/project/k3time)\n\nTime convertion utils\n\nk3time is a component of [pykit3] project: a python3 toolkit set.\n\n\n# Install\n\n```\npip install k3time\n```\n\n# Synopsis\n\n```python\n>>> parse('2017-01-24T07:51:59.000Z', 'iso')\ndatetime.datetime(2017, 1, 24, 7, 51, 59)\n>>> format_ts(1485216000, 'iso')\n'2017-01-24T00:00:00.000Z'\n>>> format_ts(1485216000, '%Y-%m-%d')\n'2017-01-24'\n```\n\n#   Author\n\nZhang Yanpo (张炎泼) <drdr.xp@gmail.com>\n\n#   Copyright and License\n\nThe MIT License (MIT)\n\nCopyright (c) 2015 Zhang Yanpo (张炎泼) <drdr.xp@gmail.com>\n\n\n[pykit3]: https://github.com/pykit3",
    long_description_content_type="text/markdown",
    author='Zhang Yanpo',
    author_email='drdr.xp@gmail.com',
    url='https://github.com/drmingdrmer/k3time',
    keywords=['time', 'date', 'timestamp'],
    python_requires='>=3.0',

    install_requires=['semantic_version==2.6.0', 'jinja2==2.10.1', 'PyYAML==5.1', 'sphinx==3.0.3', 'tzlocal==2.0.0', 'pytz==2019.3', 'k3ut==0.1.6'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
    ] + ['Programming Language :: Python :: 3.6', 'Programming Language :: Python :: 3.7', 'Programming Language :: Python :: 3.8', 'Programming Language :: Python :: Implementation :: PyPy'],
)
