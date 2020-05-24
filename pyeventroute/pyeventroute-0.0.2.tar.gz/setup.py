import setuptools

"""
The documentation can be found at:
http://setuptools.readthedocs.io/en/latest/setuptools.html
"""
setuptools.setup(
    # the first three fields are a must according to the documentation
    name='pyeventroute',
    version='0.0.2',
    packages=[
        'pyeventroute',
    ],
    # from here all is optional
    description='pyeventroute helps you route events to loggers or to any other place',
    long_description='pyeventroute helps you route events to loggers or to any other place',
    author='Mark Veltzer',
    author_email='mark.veltzer@gmail.com',
    maintainer='Mark Veltzer',
    maintainer_email='mark.veltzer@gmail.com',
    keywords=[
        'event',
        'logging',
    ],
    url='https://veltzer.github.io/pyeventroute',
    download_url='https://github.com/veltzer/pyeventroute',
    license='MIT',
    platforms=[
        'python3',
    ],
    install_requires=[
        'pytconf',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
    data_files=[
    ],
    entry_points={'console_scripts': [
    ]},
    python_requires='>=3.5',
)
