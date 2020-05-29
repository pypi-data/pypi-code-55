import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-prefab-endpoints", # Replace with your own username
    version="0.0.1",
    author="John Synnott",
    author_email="johnsynn@gmail.com",
    description="Quick and basic endpoints for Django",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/johnsynnott/django-prefab-endpoints",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
