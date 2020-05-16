import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Linq.py", # Replace with your own username
    version="0.0.1",
    author="Fateamplex",
    author_email="fateamplex@gmail.com",
    description="A small package for games and file maintenance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fateamplex/Linq.py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)