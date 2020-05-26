import setuptools

"""
The documentation can be found at:
http://setuptools.readthedocs.io/en/latest/setuptools.html
"""
setuptools.setup(
    # the first three fields are a must according to the documentation
    name='pymyenv',
    version='0.0.5',
    packages=[
        'pymyenv',
        'pymyenv.endpoints',
    ],
    # from here all is optional
    description='pymyenv manages environments for you',
    long_description='pymyenv manages environments for you',
    author='Mark Veltzer',
    author_email='mark.veltzer@gmail.com',
    maintainer='Mark Veltzer',
    maintainer_email='mark.veltzer@gmail.com',
    keywords=[
        'pipenv',
        'pip',
        'virtualenv',
    ],
    url='https://veltzer.github.io/pymyenv',
    download_url='https://github.com/veltzer/pymyenv',
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
        'pymyenv=pymyenv.endpoints.main:main',
    ]},
    python_requires='>=3.4',
)
