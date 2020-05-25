import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='dimae',
    version='0.1.3',
    author="SynStratos",
    author_email="synstratos.dev@gmail.com",
    description="Dimensionality Autoencoder",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://github.com/SynStratos/dim_ae",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'tensorflow',
        'scikit-learn'
    ],
)
