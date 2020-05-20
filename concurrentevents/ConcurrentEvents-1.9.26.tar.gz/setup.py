import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ConcurrentEvents",
    version="1.9.26",
    author="Reggles",
    author_email="reginaldbeakes@gmail.com",
    description="An event system build on top of the concurrent futures library, including additional threading tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Reggles44/concurrentevents",
    include_package_data=True,
    packages=['concurrentevents', 'concurrentevents.enums', 'concurrentevents.tools'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
