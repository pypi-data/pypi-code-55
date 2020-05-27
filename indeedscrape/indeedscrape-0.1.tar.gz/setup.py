
from distutils.core import setup
setup(
  name = 'indeedscrape',         
  packages = ['indeedscrape'],   
  version = '0.1',     
  license='MIT',       
  description = 'scrape data from indeed',   
  author = 'Antonio Trani',                   
  author_email = 'art3kr@virginia.edu',     
  url = 'https://github.com/user/art3kr',  
  download_url = 'https://github.com/art3kr/indeedscraper/archive/v_01.tar.gz',   
  keywords = ['indeed', 'jobs', 'scraping', 'scrape','beautifulsoup'],  
  install_requires=[           
          'os',
          'beautifulsoup4',
          'time',
          'datetime',
          'json',
          'pandas',
          'configparser',
          'selenium',
          'bs4'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3.6',
  ],
)