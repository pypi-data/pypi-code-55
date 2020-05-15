import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="honeybee-radiance",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    author="Ladybug Tools",
    author_email="info@ladybug.tools",
    description="Daylight and light simulation extension for honeybee.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ladybug-tools/honeybee-radiance",
    packages=setuptools.find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=requirements,
    extras_require={
        'cli': ['click==7.1.2', 'honeybee-core[cli]==1.30.1']
    },
    entry_points={
        "console_scripts": ["honeybee-radiance = honeybee_radiance.cli:radiance"]
    },
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent"
    ],
)
