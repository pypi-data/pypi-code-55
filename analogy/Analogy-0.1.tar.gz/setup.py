import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Analogy",
    version="0.1",
    author="Jim Macwan",
    author_email="jimmacwan94@gmail.com",
    description="Experimental Open-source Natural Language Processing project for similiarity and difference retrieval",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jmacwan/Analogy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'pycorenlp',
          'numpy'
      ]
)