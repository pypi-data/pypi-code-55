import setuptools

"""
The documentation can be found at:
http://setuptools.readthedocs.io/en/latest/setuptools.html
"""
setuptools.setup(
    # the first three fields are a must according to the documentation
    name='pymakehelper',
    version='0.0.3',
    packages=[
        'pymakehelper',
        'pymakehelper.endpoints',
    ],
    # from here all is optional
    description='pymakehelper helps doing things with the make system',
    long_description='pymakehelper helps doing things with the make system',
    author='Mark Veltzer',
    author_email='mark.veltzer@gmail.com',
    maintainer='Mark Veltzer',
    maintainer_email='mark.veltzer@gmail.com',
    keywords=[
        'make',
        'scons',
    ],
    url='https://veltzer.github.io/pymakehelper',
    download_url='https://github.com/veltzer/pymakehelper',
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
        'pymakehelper=pymakehelper.endpoints.main:main',
    ]},
    python_requires='>=3.5',
)
