import setuptools
with open("README.md", "r") as fh:
	long_description = fh.read()
setuptools.setup(
	name = 'dnaApi',   
	version = '0.2.2',      
	license='MIT',        
	description = 'This module will interact with Tor to get real time statistical and analytical information.', 
	long_description=long_description,
	long_description_content_type="text/markdown",
	author = 'Narender Singh Yadav,Divya Gupta',                   
	author_email = 'narenderyadav1999@gmail.com,2016ucp1472@mnit.ac.in',      
	url = 'https://github.com/narendersinghyadav/dnaApi',     
	keywords = ['TOR', 'ANALYSIS', 'STATISTICAL ANALYSIS TOR','TOR NETWORK ANALYSIS'],  
	install_requires=[           
		'ipaddress',
		'psutil',
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
