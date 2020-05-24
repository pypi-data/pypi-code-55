import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="alexa_responses", # Replace with your own username
    version="0.0.2",
    author='Eduardo Arada',
    author_email='eduardo.arada@gmail.com',
    description="Alexa responses python module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/earada/alexa-responses",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
