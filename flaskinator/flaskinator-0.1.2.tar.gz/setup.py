from distutils.core import setup
setup(
  name = 'flaskinator',         # How you named your package folder (MyLib)
  packages = ['flaskinator'],   # Chose the same as "name"
  version = '0.1.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Quick library to generate ready to use APIs for Flask environment',   # Give a short description about your library
  author = 'Divs',                   # Type in your name
  url = 'https://github.com/Divsatwork/flaskinator',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Divsatwork/flaskinator/archive/v_0.1.2.tar.gz',    # I explain this later on
  keywords = ['Flask', 'Ready to use', 'API'],   # Keywords that define your package best
  install_requires=[ ], #no dependencies
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)