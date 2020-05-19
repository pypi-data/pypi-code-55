
import setuptools

setuptools.setup(
    name="classforge", # Replace with your own username
    version="0.9",
    author="Michael DeHaan",
    author_email="michael@michaeldehaan.net",
    description="A new python object system",
    long_description="ClassForge is a new python object system.",
    long_description_content_type="text/plain",
    url="https://classforge.io",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
	    "Intended Audience :: Developers",
        "Topic :: Software Development"
    ],
    python_requires='>=3.6',
    include_package_data=True,
    install_requires=[
        "PyYAML>=5.3.1",
    ]
)
