from setuptools import setup

setup(name='nlp_playground',
      version='0.15',
      description='Python package for basic NLP functions',
      packages=['nlp_playground'],
      install_requires=[
        'PyPDF2',
        'beautifulsoup4==4.8.0'
    ],
      zip_safe=False)
