import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="KnnRegressionRobGin", # Replace with your own username
    version="1.0.0",
    author="Md Robiuddin",
    author_email="mrrobi040@hotmail.com",
    description="A package for KNN Regression",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Mrrobi/python/packages/knnRegression",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
