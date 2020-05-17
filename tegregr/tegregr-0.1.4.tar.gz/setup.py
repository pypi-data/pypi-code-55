import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tegregr", # Replace with your own username
    version="0.1.4",
    author="Thomas E Gladwin",
    author_email="thomasgladwin@hotmail.com",
    description="Multiple and hierarchical regression",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thomasgladwin/tegregr",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
