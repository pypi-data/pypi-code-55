import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="automateWordPressPost",
    version="0.1.1",
    author="Umer Mughal",
    author_email="umermuxhal@gmail.com",
    description="Automate WordPress Block Editor. Add post using docx file or html file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/UmerMuxhal/automate-wordpress-post",
    download_url='https://github.com/UmerMuxhal/automate-wordpress-post/archive/v_0.1.tar.gz',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        'Intended Audience :: Developers',
    ],
    python_requires='>=3.6',
    keywords=['automate', 'wordpres', 'post'],
    install_requires=[
        'beautifulsoup4==4.9.0',
        'bs4==0.0.1',
        'cobble==0.1.3',
        'mammoth==1.4.10',
        'pyperclip==1.8.0',
        'random-user-agent==1.0.1',
        'selenium==3.141.0',
        'soupsieve==2.0',
        'urllib3==1.25.9',
    ]
)
