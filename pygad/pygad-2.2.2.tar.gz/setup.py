import setuptools  

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(  
    name="pygad",  
    version="2.2.2",  
    author="Ahmed Fawzy Gad",
    install_requires=["numpy", "matplotlib",],
    author_email="ahmed.f.gad@gmail.com",  
    description="PyGAD: A Python library for implementing the genetic algorithm.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ahmedfgad/GeneticAlgorithmPython",
    packages=setuptools.find_packages())
