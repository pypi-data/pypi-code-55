import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mykmeansbestkchen", # Replace with your own username
    version="0.1.1",
    author="searphYC",
    author_email="zyc199685@gmail.com",
    description="A small kmeans package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Seraph-YCZhang/Kmeans-code-assignment",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
