
from distutils.core import setup
setup(
  name = 'test_code1997',         # How you named your package folder (MyLib)
  packages = ['test_code1997'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='Apache 2.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = ' pandas_ui helps you wrangle & explore your data and create custom visualizations without digging through StackOverflow. All inside your Jupyter Notebook or JupyterLab ( alternative to Bamboolib ).',   # Give a short description about your library
  author = 'Arunn Thangavel',                   # Type in your name
  author_email = 'arunnbabainfo@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/arunnbaba/',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/arunnbaba/test_code1997/archive/v4.0.zip',
  keywords = ['Pands_ui', 'bamboolib', 'ui for pandas'],
  install_requires=[            # I get to this in a second
          'future',
          'ipywidgets',
          'ipython',
          'pandas',
          'qgrid',
          'traitlets',
          'pandas-profiling',
          'bokeh',
          'plotly',
          'numpy'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.7'      #Specify which pyhton versions that you want to support
    
  ],
)