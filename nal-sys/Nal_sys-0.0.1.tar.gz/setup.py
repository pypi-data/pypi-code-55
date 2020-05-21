from setuptools import setup, find_packages

with open("Readme.md", "r") as readme_file:
    long_description = readme_file.read()
setup(
    name = 'Nal_sys',
    version ="0.0.1",
    py_modules = ['nal_sys'],
    packages = find_packages(),
    #package_dir = {'': 'src'},
    author = 'Andreas Evensen',
    author_email= 'Andreas.evensen11@gmail.com',
    description = 'This is a libery for numerical anlysis, most common tools for the Bachlor program in physics.',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    license = "MIT",
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License"
    ],
    keywords = "Numerical Anlysis"
)
