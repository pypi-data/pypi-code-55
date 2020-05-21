import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()


setuptools.setup(
    name = "adpred",
    version="1.2.5",
    author="Ariel Erijman",
    author_email="aerijman@fredhutch.org, aerijman@neb.com",
    description="Prediction of Transcription Activation Domains from protein sequences",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FredHutch/adpred-pkg",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'setuptools==46.4.0',
        'keras==2.2.4',
        'scikit-learn==0.21.3',
        'numpy==1.17.2',
        'plotly==4.1.1',
        'tensorflow==1.14.0',
        'requests==2.23.0',
        'pandas==0.25.1',
    ],
    include_package_data=True,
    scripts=[
        'bin/run-adpred'
    ]
)
