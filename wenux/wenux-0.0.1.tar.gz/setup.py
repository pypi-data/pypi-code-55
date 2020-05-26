import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wenux", # Replace with your own username
    version="0.0.1",
    author="Jozef Urbanovský",
    author_email="jurbanov@redhat.com.com",
    description="WAN emulator for Linux",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Axonis/DP",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)