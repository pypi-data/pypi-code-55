from setuptools import setup, find_packages

setup(
    name="reverb_i2c",
    version="1.0",
    license="GPL",
    packages=find_packages(),
    author="tjreverb",
    author_email="tjreverb@gmail.com",
    description="A fake i2c library for testing purposes",
    url="https://github.com/TJREVERB/reverb_i2c",
    python_requires='>=3.7',
)
