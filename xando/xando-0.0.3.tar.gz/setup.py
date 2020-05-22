import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xando",
    version="0.0.3",
    author="Aziz Alfoudari",
    author_email="aziz.alfoudari@gmail.com",
    description="TicTacToe game engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abstractpaper/tictactoe",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
