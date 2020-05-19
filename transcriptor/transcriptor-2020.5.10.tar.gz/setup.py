from setuptools import setup, find_packages

with open("README.md") as filename:
    long_description = filename.read()


setup(
        name='transcriptor',
        version='2020.5.10',
        description='A wrapper for transcription results.',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/kjaymiller/transcriptor',
        author='Jay Miller',
        author_email='kjaymiller@gmail.com',
        license='MIT',
        packages=find_packages(),
        zip_safe=False,
        )
