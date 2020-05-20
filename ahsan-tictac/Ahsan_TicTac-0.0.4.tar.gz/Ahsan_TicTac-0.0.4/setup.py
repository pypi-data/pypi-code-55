# TODO: Fill out this file with information about your package

# HINT: Go back to the object-oriented programming lesson "Putting Code on PyPi" and "Exercise: Upload to PyPi"

# HINT: Here is an example of a setup.py file
# https://packaging.python.org/tutorials/packaging-projects/
import setuptools
#twine upload --repository-url https://test.pypi.org/legacy/ dist/*
#pip install --index-url https://test.pypi.org/simple/ distributions
setuptools.setup(
    name="Ahsan_TicTac", # Replace with your own username
    version="0.0.4",
    author="Ahsan",
    author_email="author@example.com",
    description="A small tic tac toe game",
    long_description="Game, by any name, is a game, in a game!",
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/ahsan_ticktac",
)