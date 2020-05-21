import setuptools

"""
The documentation can be found at:
http://setuptools.readthedocs.io/en/latest/setuptools.html
"""
setuptools.setup(
    # the first three fields are a must according to the documentation
    name='pyunique',
    version='0.0.1',
    packages=[
        'pyunique',
        'pyunique.endpoints',
    ],
    # from here all is optional
    description='help you get ridd of duplicate files',
    long_description='help you get ridd of duplicate files',
    author='Mark Veltzer',
    author_email='mark.veltzer@gmail.com',
    maintainer='Mark Veltzer',
    maintainer_email='mark.veltzer@gmail.com',
    keywords=[
        'duplicates',
        'remove',
        'hash',
    ],
    url='https://veltzer.github.io/pyunique',
    download_url='https://github.com/veltzer/pyunique',
    license='MIT',
    platforms=[
        'python3',
    ],
    install_requires=[
        'pytconf',
        'pylogconf',
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
        'pyunique=pyunique.endpoints.main:main',
    ]},
    python_requires='>=3.5',
)
