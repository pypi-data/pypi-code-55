from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='distributions_by_rrod',
      version='0.1',
      author = "R. Rodriguez",
      description='Gaussian and Binomial distributions',
      long_description = long_description,
      long_description_content_type = "text/markdown",
      #url = "https://github.com/pypa/sampleproject",
      packages=['distributions_by_rrod'],
      zip_safe=False)
