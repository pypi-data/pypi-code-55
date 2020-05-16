import setuptools


"""
with open('README.md', 'r', encoding='utf-8') as f:
    long_description_content = f.read()


with open('LICENSE', 'r', encoding='utf-8') as f:
    license_content = f.read()
"""

with open('requirements.txt', 'r', encoding='utf-8') as f:
    install_requires_content = f.read().split()


setuptools.setup(
    name="snowglobe",
    version="0.0.3",
    author="Mohit Udupa",
    author_email="mohitudupa@gmail.com",
    description="A python package to manage docker development environments.",
    # license=license_content,
    # long_description=long_description_content,
    # long_description_content_type="text/markdown",
    url="https://github.com/mohitudupa/SnowGlobe",
    packages=['snowglobe'],
    package_data={'snowglobe': ['configs/*.json']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['snowglobe=snowglobe.__main__:main'],
    },
    install_requires=install_requires_content,
)
