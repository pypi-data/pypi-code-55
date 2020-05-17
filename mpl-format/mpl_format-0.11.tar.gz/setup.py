from distutils.core import setup

setup(
    name='mpl_format',
    packages=['mpl_format'],
    version='0.11',
    license='MIT',
    description='Library for easier formatting of matplotlib plots written in a functional style.',
    author='Vahndi Minah',
    url='https://github.com/vahndi/mpl-format',
    download_url='https://github.com/vahndi/reponame/archive/v_0.11.tar.gz',
    keywords=['matplotlib'],
    install_requires=[
        'matplotlib',
        'seaborn',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
)
