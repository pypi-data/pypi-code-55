import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kubernetes-explorer",
    version="1.0.1",
    author="Jonathan Donzallaz",
    author_email="jonathan.donzallaz@gmail.com",
    description="Kubernetes Explorer lets you create a graph of the objects and dependencies inside your Kubernetes cluster.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/jdonzallaz/kubernetes-explorer",
    packages=setuptools.find_packages(),
    install_requires=[
        'graphviz>=0.14',
        'kubernetes>=11.0.0',
        'pyyaml>=5.3.1'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['kubex=kubernetes_explorer.kubex:main'],
    }
)
