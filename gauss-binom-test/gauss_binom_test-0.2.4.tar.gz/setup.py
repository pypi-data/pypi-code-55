from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='gauss_binom_test',
      version='0.2.4',
      description='Gaussian and Binomial distributions',
      long_description=long_description,
      long_description_content_type="text/markdown",
      license='MIT',
      author='ludovico',
      packages=['gauss_binom_test'],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
      python_requires='>=3.6',
      zip_safe=False)
