import re
import setuptools


def read_file(path):
    with open(path, "r") as handle:
        return handle.read()


def read_version():
    try:
        s = read_file("VERSION")
        print(s)
        m = re.match(r"v(\d+\.\d+\.\d+)", s)
        print(m)
        return m.group(1)
    except FileNotFoundError:
        return "0.0.0"


long_description = read_file("docs/source/description.rst")
version = read_version()

setuptools.setup(
    name='scenario-optimiser',
    version=version,
    description="""
    optimisation tool for discrete points (scenarios) with different techniques 
    """,
    include_package_data=True,
    url="https://gitlab.com/GreenhouseGroup/ai/libraries/scenario-optimiser",
    author="Greenhouse AI team",
    author_email="ai@greenhousegroup.com",
    license='MIT',
    package_dir={'scenario_optimiser': "src/scenario_optimiser"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],

    install_requires=[
        "pandas>=0.23.0,<=0.25.3",
        "numpy>=1.16.0,<=1.18.0",
        "scipy>=1.3,<=2.0.0",
        "mip>=1.8.0,<=2.0.0",
    ],
    data_files=[(".", ["VERSION"])],
    setup_requires=["pytest-runner"],
    tests_require=["pytest>=4"],
    packages=setuptools.find_packages("src"),
)
