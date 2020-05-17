from setuptools import find_packages, setup

setup(
    name = "conML",
    packages = find_packages(),
    version = 0.2,
    licence="MIT",
    description="constructivist machine learning",
    author="Dmitrij Denisenko",
    install_requires = [
        "numpy",
        "krippendorff",
        "scikit-learn",
        "scipy",
        "pandas"
    ]
)
