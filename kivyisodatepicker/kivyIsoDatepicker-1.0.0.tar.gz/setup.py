import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kivyIsoDatepicker",  # Replace with your own username
    version="1.0.0",
    author="Ricardo Vogel",
    author_email="info@ricardovogel.nl",
    description="Python 3.3+ version of Oleg Kozlov KivyCalandar in ISO 8601 date format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ricardovogel/datepicker",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.3',
)
