from setuptools import setup, find_packages

install_requires = [
    'matplotlib',
    'numpy',
    'pandas',
    'sklearn'
    
]

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='Basicenssembleargumentation',
    version='0.0.1',
    description='A basic argumentation process where the outcomes from different models can argue for generating a final output.',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Istiak Ahmed',
    author_email='istiak.uiu.bd@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keyword='ensembleargumentation',
    packages=find_packages(),
    python_requires=">=3.8"
   
        

)