import setuptools

"""
The documentation can be found at:
http://setuptools.readthedocs.io/en/latest/setuptools.html
"""
setuptools.setup(
    # the first three fields are a must according to the documentation
    name='pyfoldercheck',
    version='0.0.2',
    packages=[
        'pyfoldercheck',
        'pyfoldercheck.endpoints',
    ],
    # from here all is optional
    description='apply a set of checks on files in a folder',
    long_description='apply a set of checks on files in a folder',
    author='Mark Veltzer',
    author_email='mark.veltzer@gmail.com',
    maintainer='Mark Veltzer',
    maintainer_email='mark.veltzer@gmail.com',
    keywords=[
        'mp3',
        'pdf',
        'collection',
    ],
    url='https://veltzer.github.io/pyfoldercheck',
    download_url='https://github.com/veltzer/pyfoldercheck',
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
        'pyfoldercheck=pyfoldercheck.endpoints.main:main',
    ]},
    python_requires='>=3.5',
)
