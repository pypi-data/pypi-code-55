from setuptools import setup, find_packages
  
long_description = 'Simple indexer for a GKE Onprem snapshot bundle'

# some more details 
CLASSIFIERS = [ 
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers', 
    'Topic :: System :: Systems Administration', 
    'License :: OSI Approved :: MIT License', 
    'Programming Language :: Python', 
    'Programming Language :: Python :: 3', 
    'Programming Language :: Python :: 3.6', 
    'Programming Language :: Python :: 3.7', 
    'Programming Language :: Python :: 3.8', 
    ] 

setup(name='gkeop-snapshot-indexer', 
      version='1.0.3', 
      description='Simple indexer for a GKE Onprem snapshot bundle', 
      long_description=long_description, 
      url='https://github.com/dialogbox/gkeop-snapshot-indexer',
      author='Jason Kim', 
      author_email='junchul@google.com', 
      license='MIT', 
      packages=find_packages(exclude=('tests')),
      entry_points ={ 
            'console_scripts': [ 
                'gkeop-snapshot-indexer=indexer.main:index'
            ] 
        }, 
      classifiers=CLASSIFIERS, 
      install_requires=[
          'PyYAML>5',
          'click>7'
      ], 
      tests_require=[
          'pytest-xdist'
      ],
      keywords='gke gkeop gke-onprem'
      ) 