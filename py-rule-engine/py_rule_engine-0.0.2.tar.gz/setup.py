from setuptools import setup, find_packages

setup(
    name="py_rule_engine",
    version="0.0.2",
    description="Rule Engine",
    author="Shuttl",
    author_email="author@example.com",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests", "pyshuttlis"],
    extras_require={
        "test": ["pytest", "pytest-runner", "pytest-cov", "pytest-pep8"],
        "dev": ["flake8"],
    },
)
