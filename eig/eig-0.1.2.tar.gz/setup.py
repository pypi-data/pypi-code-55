from setuptools import setup, find_packages

install_requires = ['numpy', 'tensorflow', 'scikit-learn', 'statsmodels']

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='eig',
    author="BioCiphers",
    author_email="info@biociphers.org",
    version='0.1.2',
    packages=find_packages(),
    license='MIT License',
    description="Enhanced Integrated Gradients"
                " - a method of attributing the prediction of a deep network to its input features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/biociphers/eig/src/master/",
    setup_requires=['wheel'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=install_requires
)