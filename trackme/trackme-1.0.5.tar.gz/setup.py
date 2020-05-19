import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()
txt = '''selenium==3.141.0
Flask==1.1.1    
Flask-WTF==0.14.2
pymongo==3.9.0
WTForms==2.2.1 
urllib3==1.24.1
APScheduler==3.6.3
dnspython==1.16.0
http_request_randomizer==1.2.3
'''
required = txt.splitlines()
setuptools.setup(
    name='trackme',
    version='1.0.5',
    author='Bohdan Vey and Dmytro Lopushanskyy',
    description='Social media monitoring',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/DmytroLopushanskyy/Social-Media-Monitoring',
    packages=setuptools.find_packages(exclude=['examples']),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=required
)
