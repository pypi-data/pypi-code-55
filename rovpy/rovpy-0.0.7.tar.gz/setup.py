from setuptools import setup


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="rovpy",
    version="0.0.7",
    description="Ardusub based Rov Library",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/enisgetmez",
    author="Enis Getmez",
    author_email="enis@enisgetmez.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ],
    packages=["rovpy"],
    include_package_data=True,
     install_requires=[            
          'numpy',
          'pymavlink',
          'imutils',
          'opencv-python',
          'serial'
      ],
)