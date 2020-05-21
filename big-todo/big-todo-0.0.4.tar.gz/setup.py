import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="big-todo",
    version="0.0.4",
    author="Jake Kara",
    author_email="jake@jakekara.com",
    description="CLI tool to combine TODO files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jakekara/big-todo",
    packages=['btodo'],  # setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "glob2"
    ],
    entry_points={
        'console_scripts': ['btodo=btodo:main'],
    },
    python_requires='>=3.6',
)
