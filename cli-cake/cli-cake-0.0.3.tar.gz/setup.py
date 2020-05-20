import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cli-cake", # Replace with your own username
    version="0.0.3",
    author="Matthew Fan",
    author_email="mfan@umd.edu",
    description="Turn your python functions into CLI-friendly scripts.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mattjfan/cli-cake",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)