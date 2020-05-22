from distutils.core import setup

setup(
  name = 'LlamaLogsDev',   
  packages = ['LlamaLogsDev'],
  version = '0.1.7',
  license='MIT',    
  description = 'Client library for Llama Logs; https://llamalogs.com',
  author = 'Llama Logs',
  author_email = 'andrew@llamalogs.com',
  url = 'https://github.com/llamalogs/llamalogs-py-dev',
  download_url = 'https://github.com/llamalogs/llamalogs-py-dev/archive/0.1.7.tar.gz',
  keywords = ['llama', 'logs', 'metrics', 'llamalogs'],   
  install_requires=['requests'],
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