import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="Simis",
  version="0.1.6",
  author="Simis AS",
  author_email="support@simis.io",
  description="A package for communicating with the Ashes wind turbine simulation software in order to run custom simulation code.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://www.simis.io",
  packages=setuptools.find_packages(),
  classifiers=[
    "Development Status :: 3 - Alpha",
    "Programming Language :: Python :: 3",
    "License :: Other/Proprietary License",
    "Operating System :: Microsoft :: Windows"
  ],
  install_requires=[
    "PySide2 >= 5.13.2"
  ]
)