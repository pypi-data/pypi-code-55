from distutils.core import setup
setup(
  name = 'textpreprocess',         # How you named your package folder (MyLib)
  packages = ['textpreprocess'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Package to get Vocabulary , simple forms and vectors of sentences.',   # Give a short description about your library
  author = 'Vrutik Halani',                   # Type in your name
  author_email = 'vrutikhalani6@gmail.com',      # Type in your E-Mail
  url = 'https://dreamvrutik.github.io/',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/dreamvrutik/textpreprocess/archive/0.1.tar.gz',    # I explain this later on
  keywords = ['textpreprocess', 'remove punctuation', 'sentences to vectors','vocabulary'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'nltk',
          'textpreprocess',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
