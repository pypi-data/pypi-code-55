import setuptools

with open("README.md",'r') as fh:
    long_description = fh.read()

setuptools.setup(
        name='protheus',
        version='0.0.0',
        scripts=['protheus'],
        author='Henrique Luiz',
        author_email='henrique.luiz@totvs.com.br',
        description='A command-line interface for helper managemente your environment Portheus',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/HenriqueLuizz/protheus-cli',
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
    )
