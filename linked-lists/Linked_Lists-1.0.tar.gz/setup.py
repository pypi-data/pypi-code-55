import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Linked_Lists", # Replace with your own username
    version="1.0",
    author="Don Mathew",
    author_email="don.19pmc325@mcka.in",
    description="Package for immplementing Linked List operations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iamdonm/Linked_List",
    packages=["Linked_Lists"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
	"Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
)