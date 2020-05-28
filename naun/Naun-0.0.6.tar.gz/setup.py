from setuptools import setup, find_packages

with open("readme.md", "r") as readme_file:
    long_description = readme_file.read()

setup(
    name = 'Naun',
    version = "0.0.6",
    author = "Andreas Evensen",
    author_email = "Andreas.evensen11@gmail.com",
    description = "This package implements video, and picture recognition using dlib and face_recognition.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    py_modules=["Nuan"],
    package_dir={'':'src'},
    packages = find_packages(),
    Lisence = "Mit",
    install_requires = ["dlib", "face_recognition"],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License"
    ],
    keywords = "Facial Detection"
    
)