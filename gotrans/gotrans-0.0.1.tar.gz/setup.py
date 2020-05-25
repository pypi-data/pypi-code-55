import setuptools

with open("README.md", 'r') as f:
    long_desc = f.read()

setuptools.setup(
    name='gotrans',
    version='0.0.1',
    author='taner',
    author_email='taner@example.com',
    description='google trans',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    url='https://github.com/Olaful/',
    packages=['gotrans'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6'
)
