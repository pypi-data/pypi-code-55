import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="svm-kernels", # Replace with your own username
    version="0.0.1",
    author="Alberto Benayas",
    author_email="benayas1@gmail.com",
    description="Orthogonal Polynomial Kernels for SVM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/benayas1/svm-kernels",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)