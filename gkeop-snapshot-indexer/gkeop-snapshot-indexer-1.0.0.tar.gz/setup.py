from setuptools import setup, find_packages
  
# reading long description from file 
with open('DESCRIPTION.txt') as file: 
    long_description = file.read() 

with open('requirements.txt') as f: 
    REQUIREMENTS = f.readlines() 
with open('test-requirements.txt') as f: 
    TEST_REQUIREMENTS = f.readlines() 

# some more details 
CLASSIFIERS = [ 
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers', 
    'Topic :: System :: Systems Administration', 
    'License :: OSI Approved :: MIT License', 
    'Programming Language :: Python', 
    'Programming Language :: Python :: 2.7', 
    'Programming Language :: Python :: 3', 
    'Programming Language :: Python :: 3.6', 
    'Programming Language :: Python :: 3.7', 
    'Programming Language :: Python :: 3.8', 
    ] 

setup(name='gkeop-snapshot-indexer', 
      version='1.0.0', 
      description='Simple indexer for a GKE Onprem snapshot bundle', 
      long_description=long_description, 
      url='https://github.com/dialogbox/gkeop-snapshot-indexer',
      author='Jason Kim', 
      author_email='junchul@google.com', 
      license='MIT', 
      packages=find_packages(),
      entry_points ={ 
            'console_scripts': [ 
                'gkeop-snapshot-indexer = indexer.main:index'
            ] 
        }, 
      classifiers=CLASSIFIERS, 
      install_requires=REQUIREMENTS, 
      tests_require=TEST_REQUIREMENTS,
      keywords='gke gkeop gke-onprem'
      ) 