from setuptools import setup

# Version
version = None
with open("hierarchical_classifier/__init__.py", "r") as f:
    for line in f.readlines():
        line = line.strip()
        if line.startswith("__version__"):
            version = line.split("=")[-1].strip().strip('"')
assert version is not None, "Check version in hierarchical_classifier/__init__.py"

setup(
name='hierarchical_classifier',
    version=version,
    description='Customizable scikit-learn compatible hierarchical classifiers',
    url='https://github.com/jolespin/hierarchical_classifier',
    author='Josh L. Espinoza',
    author_email='jespinoz@jcvi.org',
    license='BSD-3',
    packages=["hierarchical_classifier"],
    install_requires=[
        "pandas >= 1",
        "numpy",
        "networkx >= 2",
        "matplotlib >= 2",
      ],
)
