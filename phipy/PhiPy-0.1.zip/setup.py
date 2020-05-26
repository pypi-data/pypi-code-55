from distutils.core import setup
setup(
  name = 'PhiPy',         
  packages = ['PhiPy'],   
  version = '0.1',      
  license='MIT',       
  description = 'A Physics calculation library for Python',   
  author = 'Kubilay AYTEMIZ',
  author_email = 'meneskaytemiz@hotmail.com',      
  url = 'https://github.com/Kobemeka/PhiPy',   
  download_url = 'https://github.com/Kobemeka/PhiPy/archive/v0.1.tar.gz',    
  keywords = ['Physics', 'Calculation', 'Simulation'],   
  install_requires=[            
          'numpy'
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