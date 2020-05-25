from setuptools import setup
import DateVersioning

with open("README.md") as f:
    readme = f.read()

setup(
    name="DateVersioning",
    version=DateVersioning.generate(),
    description="Git commit date based version generator",
    long_description_content_type="text/markdown",
    long_description=readme,
    author="Einar Arnason",
    author_email="einar@gmail.com",
    url="https://github.com/EinarArnason/DateVersioning",
    py_modules=["DateVersioning"],
    license="MIT",
    test_suite="tests",
)
