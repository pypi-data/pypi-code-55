# Change the behavior of google.colab.data_table to my liking

# First, 
# = %load_ext google.colab.data_table
get_ipython().run_line_magic('load_ext', 'google.colab.data_table')
# Then, make the default width to fit content, instead of 100%
from google.colab.data_table import DataTable
DataTable.min_width = '0'

def unload():
    get_ipython().run_line_magic('unload_ext', 'google.colab.data_table')