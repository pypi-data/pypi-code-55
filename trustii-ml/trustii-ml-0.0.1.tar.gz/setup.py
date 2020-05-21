import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="trustii-ml", # Replace with your own username
    version="0.0.1",
    author="tiwars",
    author_email="mockinbird24@gmail.com",
    description="To add Trustii Class to Python Path",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
