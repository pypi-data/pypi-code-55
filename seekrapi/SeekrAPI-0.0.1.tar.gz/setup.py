import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SeekrAPI",
    version="0.0.1",
    author="Santiago Melo Medina",
    author_email="santiagodevelopment001@gmail.com",
    description="Simple documentation for flask api",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/santiagoMeloMedina/Seekr",
    packages=["seekrApi"],
    package_data={'seekrApi': ['data/*']},
    install_requires=['Flask==1.1.2'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    python_requires='>=3.6'
)
