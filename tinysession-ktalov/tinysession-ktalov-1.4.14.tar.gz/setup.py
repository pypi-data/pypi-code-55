import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="tinysession-ktalov",
    version="1.4.14",
    author="Jose Morales Ventura",
    author_email="jomorales.ventura@gmail.com",
    description="A session manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/ktalov/tinysession.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
