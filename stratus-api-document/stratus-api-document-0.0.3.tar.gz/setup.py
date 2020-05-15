import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

# with open('requirements.txt') as f:
#     requirements = f.readlines()

setuptools.setup(
    name="stratus-api-document",  # Replace with your own username
    version="0.0.3",
    author="DOT",
    author_email="dot@adara.com",
    description="An API stratus_api for simplified development",
    long_description="Sample",
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://github.com/dot-at-adara/firestore",
    setup_requires=['pytest-runner'],
    test_requires=[
        "google-api-python-client>=1.7.11",
        "google-cloud-firestore>=1.6.2",
        "stratus-api-core>=0.0.3"
    ],
    packages=setuptools.find_namespace_packages(include=['stratus_api.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "google-api-python-client>=1.7.11",
        "google-cloud-firestore>=1.6.2",
        "stratus-api-core>=0.0.3"
    ],

)
