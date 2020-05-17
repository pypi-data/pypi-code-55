from distutils.core import setup
setup(
  name = 'AAmiles',         
  packages = ['AAmiles','AAmiles/getDataAA'],  
  version = '0.1.0',     
  license='MIT',       
  description = 'Check changes in the miles required to obtain a ticket from the AA web page',
  author = 'Aldebaran bO',  
  author_email = '19.beta.Orionis@gmail.com',   
  url = 'https://github.com/bOrionis/AAmiles',  
  download_url = 'https://github.com/bOrionis/getDataAA/archive/getDataAA-0.1.0.tar.gz', 
  keywords = ['Miles', 'airplane tickets', 'Aerolineas Argentinas'],  
  install_requires=[        
          'request',
          'bs4',
          'numpy',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha', 
    'Intended Audience :: End Users/Desktop',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',    
  ],
)