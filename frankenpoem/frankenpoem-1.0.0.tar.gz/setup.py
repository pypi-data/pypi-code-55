import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="frankenpoem", # Replace with your own username
    version="1.0.0",
    author="Kyelee Fitts",
    author_email="kyelee.fitts@gmail.com",
    description="Generate poems cobbled together from the remains of older, better poems, with a particular emphasis on rhyme and meter consistency.",
    # long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/ruthlee/frankenpoems",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['pronouncing'],
    package_data = {'frankenpoem': ['data.pkl.compress']}
)