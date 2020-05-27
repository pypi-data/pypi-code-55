import setuptools

with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Thomas Dewitte",
    author_email="thomasdewittecontact@gmail.com",

    name='joke_generator',
    version='1.0.0',
    license="MIT",
    url='https://github.com/dewittethomas/joke-generator',
    python_requires='>= 3.5',
    
    description='Returns a random joke',
    long_description=README,
    long_description_content_type="text/markdown",

    package_dir={"joke_generator": "joke_generator"},
    install_requires=["requests>=2.22.0"],
    
    packages=setuptools.find_packages(),

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3'
    ]
)