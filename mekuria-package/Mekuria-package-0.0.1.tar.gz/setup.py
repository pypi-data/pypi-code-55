import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Mekuria-package",
    version="0.0.1",
    author="Mekuria Tegegne",
    author_email="mekuriategegne@gmail.com",
    description="an Example Package for Mekuria.",
    long_description=long_description, # don't touch this, this is your README.md
    long_description_content_type="text/markdown",
    url="https://repl.it/@meki2020/Mekuria-package",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)