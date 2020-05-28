import setuptools
import mmanalyser as package


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mmanalyser",
    version=package.__version__,
    author="xujc",
    author_email="",
    description="a tool for multimedia",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires=[
        "pydub==0.23.1",
        "pandas==0.25.3",
        "etools==0.0.10",
        "pyAudioAnalysis==0.3.0",
        "webrtcvad==2.0.10",
        "python-Levenshtein==0.12.0",
        "pypinyin==0.37.0"

    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    package_data={'mmanalyser': ['data/*', 'utils/*']}
)
