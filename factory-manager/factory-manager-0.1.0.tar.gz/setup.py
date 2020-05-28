from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='factory-manager',
    author='Fabian Barteld',
    author_email='fabian.barteld@rub.de',
    description="A package to create objects with their dependencies from descriptions in the form of a dictionary",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fab-bar/factory-manager",
    version='0.1.0',
    python_requires='>=3.6',
    packages=find_packages(),
    install_requires=['typing-inspect'],
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ]
)
