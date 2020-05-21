from distutils.core import setup
setup(
  name = 'sharedcountsdk',         
  packages = ['sharedcountsdk'],   
  version = '0.2',     
  license='MIT',       
  description = '',   
  author = 'Sharedcount',                   
  author_email = '',      
  url = 'https://github.com/sharedcount/sharedcount-python-sdk.git',   
  download_url = 'https://github.com/sharedcount/sharedcount-python-sdk/archive/1.tar.gz',    
  keywords = [''],   
  install_requires=[           
          'requests'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
