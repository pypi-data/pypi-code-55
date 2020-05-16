import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="recompy",
    version="1.0.2",
    author="Can Bulguoglu, Oguz Kaplan, Onur Boyar, Emre Yuksel",
    author_email="canbulguoglu@gmail.com",
    description="A recommender library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/canbul/recompy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["numpy==1.18.4"],
    python_requires='>=3.5',
    include_package_data=True,
    package_data={
        '': ['*.csv']
    }
)
