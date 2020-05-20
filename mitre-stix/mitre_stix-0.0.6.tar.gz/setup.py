import setuptools

with open('README.md')as f:
    long_description = f.read()

setuptools.setup(
    name="mitre_stix",
    version="0.0.6",
    author="Henry Alarcon Jr.",
    author_email="henry_alarconjr@trendmicro.com",
    description="A Python package that scans mitre signatures from STIX2.0 json log format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.trendmicro.com/henryal/mitre-stix",
    keywords="Cyber threat intelligence",
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Topic :: Security',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.0',
)