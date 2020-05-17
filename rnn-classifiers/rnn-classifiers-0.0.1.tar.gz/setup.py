import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rnn-classifiers",  # Replace with your own username
    version="0.0.1",
    author="Urchade Zaratiana",
    author_email="urchade.zaratiana@gmail.com",
    description="Pytorch RNN classifiers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/urchade/Rnn-classifiers",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)