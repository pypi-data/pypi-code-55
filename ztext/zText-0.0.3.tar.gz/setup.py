import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zText", # Replace with your own username
    version="0.0.3",
    author="Zack Dai",
    author_email="author@example.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["zText"],
    install_requires=["IPython","bokeh","pandas","xlrd","gensim","spacy","textacy","textblob","pyvis","pyLDAvis"],
    python_requires='>=3.6',
)