# flake8: noqa

depthHelp =         """how many subdirectories should zoek look in?
                    defaults to 1, meaning only files in current directory."""

showpathHelp =      """adds path to file name if set"""

startswithHelp =    """require file name to start with a string"""

containsHelp =      """require file name to contain a certain string"""

minsizeHelp =       """filter on size (-size) given in Kb: the file has size n, where n could be:
                    +integer, integer -> file size bigger than integer
                    -integer -> file size smaller than integer"""

datecreatedHelp =   """on Windows, files that were created n minutes ago, where n could be:
                    +integer -> files created more than n minutes ago
                    -integer -> files created less than n minutes ago
                    integer -> files created exactly n minutes ago)
                    (uses os.stat().st_ctime, which assesses date last modified on OSX)"""

datemodifiedHelp =  """files that were modified n minutes ago, where n could be:
                    +integer -> files created more than n minutes age
                    -integer -> files created less than n minutes age
                    integer -> files created exactly n minutes ago"""
