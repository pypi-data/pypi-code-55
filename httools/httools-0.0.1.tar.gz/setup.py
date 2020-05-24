import setuptools

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="httools",
    version="0.0.1",
    author="Hakan Temiz",
    author_email="htemiz@artvin.edu.tr",
    description="A Python Library for automating some works ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/htemiz/httools",
    packages= setuptools.find_packages(),
    keywords="super resolution deep learning excel automation",
    python_requires='>=3',
    include_package_data=True,
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst', '*.md', 'samples/*.*', 'docs/*.*' ],
    },

    exclude_package_data={'': ['']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    # scripts=[  'scripts/add_dsr_path'], # ['python -m pip install -r requirements.txt'],

    install_requires= [ 'scipy', 'pandas'],
    project_urls={
        'Documentation': 'https://github.com/htemiz/httools/tree/master/docs',
        'Source': 'https://github.com/htemiz/httools/tree/master/',
    },
    #
    # entry_points={
    #     'console_scripts': [
    #         'add_dsr_path = DeepSR.scripts:add'
    #     ],
    #     'gui_scripts': [
    #         '',
    #     ]
    # },
)
