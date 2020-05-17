import pathlib
from setuptools import find_packages, setup, Extension


HERE = pathlib.Path(__file__).parent
README = (HERE/"README.txt").read_text()


setup(
    name = "conML",
    packages = find_packages(),
    version = 0.3,
    licence="MIT",
    description="constructivist machine learning",
    long_description=README,
    long_description_content_type="text/plain",
    author="Dmitrij Denisenko",
    install_requires = [
        "numpy",
        "krippendorff",
        "scikit-learn",
        "scipy",
        "pandas"
    ]
)
