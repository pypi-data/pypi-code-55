import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="convexity_check",
    version="0.0.4",
    author="Johan Edstedt",
    author_email="edstedt.johan@gmail.com",
    description="Convexity Check is a simple package for numerically checking if a given function is convex/concave",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Parskatt/convexity_check",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['numpy'],
    python_requires='>=3.6',
)
