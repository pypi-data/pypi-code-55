from distutils.core import setup
setup(
  name = 'pyate',         # How you named your package folder (MyLib)
  packages = ['pyate'],   # Chose the same as "name"
  version = '0.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'PYthon Automated Term Extraction, running on spacy for POS tagging',   # Give a short description about your library
  author = 'Kevin Lu',                   # Type in your name
  author_email = 'kevinlu1248@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/kevinlu1248/pyate',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/kevinlu1248/pyate/archive/0.2.tar.gz',    # I explain this later on
  keywords = ['nlp', 'python3', 'spacy', 'term_extraction'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'spacy',
          'https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.2.5/en_core_web_sm-2.2.5.tar.gz',
          'numpy',
          'pandas',
          'tqdm'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3'
  ],
)