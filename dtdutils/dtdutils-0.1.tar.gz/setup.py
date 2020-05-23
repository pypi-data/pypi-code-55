import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='dtdutils',
      version='0.1',
      description='Date, Time and Data utilities',
      long_description=long_description,
      url='https://pypi.org/dtdutils',
      author='Sandeep Singhal',
      author_email='sandeep.singhal@gmail.com',
      packages=setuptools.find_packages(),
      classifiers=[
           "Programming Language :: Python :: 3",
           "License :: OSI Approved :: MIT License",
           "Operating System :: OS Independent",
            ],
      python_requires='>=3.6',
      )