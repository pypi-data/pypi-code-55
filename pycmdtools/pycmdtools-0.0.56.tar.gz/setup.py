import setuptools

"""
The documentation can be found at:
http://setuptools.readthedocs.io/en/latest/setuptools.html
"""
setuptools.setup(
    # the first three fields are a must according to the documentation
    name='pycmdtools',
    version='0.0.56',
    packages=[
        'pycmdtools',
        'pycmdtools.scripts',
    ],
    # from here all is optional
    description='pycmdtools is set of useful command line tools written in python',
    long_description='pycmdtools is set of useful command line tools written in python',
    author='Mark Veltzer',
    author_email='mark.veltzer@gmail.com',
    maintainer='Mark Veltzer',
    maintainer_email='mark.veltzer@gmail.com',
    keywords=[
        'utils',
        'command line',
        'python',
        'shell',
        'utilities',
    ],
    url='https://veltzer.github.io/pycmdtools',
    download_url='https://github.com/veltzer/pycmdtools',
    license='MIT',
    platforms=[
        'python3',
    ],
    install_requires=[
        'pylogconf',
        'requests',
        'tqdm',
        'click',
        'numpy',
        'pandas',
        'unidecode',
        'pyyaml',
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
        'pycmdtools_change_first_line=pycmdtools.scripts.change_first_line:main',
        'pycmdtools_count=pycmdtools.scripts.count:main',
        'pycmdtools_find_bad_symlinks=pycmdtools.scripts.find_bad_symlinks:main',
        'pycmdtools_google_drive_download=pycmdtools.scripts.google_drive_download:main',
        'pycmdtools_mcmp=pycmdtools.scripts.mcmp:main',
        'pycmdtools_print_all_args=pycmdtools.scripts.print_all_args:main',
        'pycmdtools_remove_bad_symlinks=pycmdtools.scripts.remove_bad_symlinks:main',
        'pycmdtools_stats=pycmdtools.scripts.stats:main',
        'pycmdtools_uniq=pycmdtools.scripts.uniq:main',
        'pycmdtools_validate_json=pycmdtools.scripts.validate_json:main',
        'pycmdtools_validate_yaml=pycmdtools.scripts.validate_yaml:main',
        'pycmdtools_progress=pycmdtools.scripts.progress:main',
        'pycmdtools_sample_weighted=pycmdtools.scripts.sample_weighted:main',
    ]},
    python_requires='>=3.5',
)
