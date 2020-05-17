from distutils.core import setup
setup(
  name = 'coverage_strategies',         # How you named your package folder (MyLib)
  packages = ['coverage_strategies'],   # Chose the same as "name"
  version = '0.8',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Provide different coverage strategies, and means to check and validate them',
  author = 'Samson Moshe',                   # Type in your name
  author_email = 'samson.moshe@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/moshesamson1',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/moshesamson1/coverage_strategies/archive/v_08git.tar.gz',    # I explain this later on
  keywords = ['COVERAGE', 'PATHS', 'SIMULATIONS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
# uploading process:
# python setup.py sdist
# twine upload dist/*
