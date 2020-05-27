import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    packages=setuptools.find_packages("src/"),
    package_dir={"appen": "src/appen"},
    setup_requires=["pbr", "setuptools", "setuptools_scm"],
    pbr=True,
    use_scm_version=True
)
