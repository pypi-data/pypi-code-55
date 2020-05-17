import setuptools

with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Thomas Dewitte",
    author_email="thomasdewittecontact@gmail.com",

    name='ip_address',
    version='1.3.0',
    license="MIT",
    url='https://github.com/dewittethomas/ip-address',
    python_requires='>= 3.5',
    
    description='A simple tool to get your ip-address',
    long_description=README,
    long_description_content_type="text/markdown",

    package_dir={"ip_address": "ip_address"},
    install_requires=["requests>=2.22.0", "beautifulsoup4>=4.8.2"],
    
    packages=setuptools.find_packages(),

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3'
    ]
)