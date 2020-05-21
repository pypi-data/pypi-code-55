import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="anda",
    version="0.0.8",
    author="Vojtech Kase",
    author_email="vojtech.kase@gmail.com",
    description="A package collecting various functions to work with ancient Mediterranean datasets (textual, spatial, etc.)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sdam-au/anda",
    packages=setuptools.find_packages(),
    package_dir={"anda": "anda"},
    package_data={"anda" : ["data/morpheus_by_lemma.json", "data/morpheus_dict.json"]},
    include_package_data=True,
    #package_data={
    #"": ["data/*.json"]
    #},
    #install_requires=[        
    #    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
)
