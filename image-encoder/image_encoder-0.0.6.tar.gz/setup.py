import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="image_encoder", # Replace with your own username
    version="0.0.6",
    author="Jagath Jai Kumar",
    author_email="jagath.jaikumar@gmail.com",
    description="A simple way to encode and decode images for REST calls",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jagath-jaikumar/image-encoder",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
          'Pillow>=6.2.0',
      ],
)
