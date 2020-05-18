import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ztext", # Replace with your own username
    version="0.0.5",
    author="Zack Dai",
    author_email="zdai@brocku.ca",
    description="An easy to use NLP tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZackAnalysis/ztext",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    install_requires=["IPython","bokeh","pandas","xlrd","gensim","spacy",
        "textacy","textblob","pyvis","pyLDAvis"],
    python_requires='>=3.6',
)