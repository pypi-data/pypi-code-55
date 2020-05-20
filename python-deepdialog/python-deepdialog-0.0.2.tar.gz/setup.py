import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-deepdialog",
    version="0.0.2",
    author="Yanan Zheng",
    author_email="zyanan93@gmail.com",
    description="DeepDialog is a lightweight library for deep generative dialogue models.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://zheng-yanan.github.io/deepdialog/",
    packages=setuptools.find_packages(exclude=['tests', 'tests.*',
                                    'examples', 'examples.*',
                                               'docs', 'docs.*',
                                               'data', 'data.*']),
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # 'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.4',
        # 'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['numpy>=1.17.4',
                      'nltk>=3.4.5',
                      'seaborn>=0.10.0',
                      'matplotlib>=3.2.0',
                      'pandas>=1.0.1',
                      'sklearn'],

    extras_require={
        'dev': [
            'Sphinx>=1.7.1',
            'sphinx_rtd_theme',
            'sphinxcontrib-bibtex>=0.3.6',
            'pep8',
            'scipy',
            'coverage',
            'mock'
        ],
        'examples': [
            'scipy',
            'matplotlib',
            'scikit-image',
            'progressbar2'
        ],
    },
)