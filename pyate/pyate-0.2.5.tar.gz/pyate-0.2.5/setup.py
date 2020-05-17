from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="pyate",  # How you named your package folder (MyLib)
    # packages=["pyate"],  # Chose the same as "name"
    version="0.2.5",  # Start with a small number and increase it with every change you make
    license="MIT",  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description="PYthon Automated Term Extraction",  # Give a short description about your library
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Kevin Lu",  # Type in your name
    author_email="kevinlu1248@gmail.com",  # Type in your E-Mail
    url="https://github.com/kevinlu1248/pyate",  # Provide either the link to your github or to your website
    download_url="https://github.com/kevinlu1248/pyate/archive/0.2.tar.gz",  # I explain this later on
    keywords=[
        "nlp",
        "python3",
        "spacy",
        "term_extraction",
    ],  # Keywords that define your package best
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=["pandas==1.0.3", "numpy==1.18.4", "spacy==2.2.4"],
    classifiers=[
        "Development Status :: 3 - Alpha",  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        "Intended Audience :: Developers",  # Define that your audience are developers
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",  # Again, pick a license
        "Programming Language :: Python :: 3",
    ],
)
