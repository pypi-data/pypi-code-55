from distutils.core import setup
from setuptools import find_packages


files = ["commercial/*","payment/*","util/*","commercial/ecrm/*","payment/transfermovil/*","util/apidevice/*"]

setup(
  name = 'etecsa-sdk',
  packages = ['etecsasdk'],
  package_data = {'etecsasdk' : files },
   
  version = '1.6',     
  license='MIT',       
  description = 'Etecsa SDK',  
  author = 'sebastian',
  author_email = 'sebastian.rodriguez@etecsa.cu',      
  url = 'https://github.com/sebastiancuba/etecsa-sdk',  
  download_url = 'https://github.com/sebastiancuba/etecsa-sdk/archive/v1.6.tar.gz',    
  keywords = ['sdk'], 
  install_requires=[
      'requests',
      'validators',
      'pendulum',
      'pyyaml',
      'ua-parser',
      'user-agents'
          ],
  classifiers=[
    'Programming Language :: Python :: 3.8',
  ],
)
