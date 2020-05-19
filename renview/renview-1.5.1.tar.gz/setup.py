from setuptools import setup

setup(
  name = 'renview',         # How you named your package folder (MyLib)
  packages = ['renview', 'renview/GraphGenerator'],   # Chose the same as "name"
  version = '1.5.1',      # Start with a small number and increase it with every change you make
  license='GNU Lesser GPL v3',        # Chose a license from here: 
  description = 'Visualizer for complex reaction systems',   # Give a short description about your library
  author = 'Udit Gupta',                   # Type in your name
  author_email = 'ugupta@udel.edu',      # Type in your E-Mail
  url = 'https://github.com/VlachosGroup/ReNView',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/VlachosGroup/ReNView/archive/1.2.tar.gz',    # I explain this later on
  keywords = ['Reaction flux analysis', 'reaction path analysis', 'visualization', 'reaction network', 'graph representation', 'data compression'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas',
          'graphviz',
		  'numpy',
		  'pydot'
      ],
  #data_files=[('data',['data/example_ammonia/reaction_rates.out','data/example_ammonia/species_comp.out'])
	#],
  include_package_data=True,
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)