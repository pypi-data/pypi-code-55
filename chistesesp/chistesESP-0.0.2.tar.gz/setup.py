import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chistesESP", # Replace with your own username
    version="0.0.2",
    author="netherpills",
    author_email="mari394334@gmail.com",
    description="Un paquete que contiene un comando que obtiene chistes de chistes.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/netherpills/chistesESP-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
