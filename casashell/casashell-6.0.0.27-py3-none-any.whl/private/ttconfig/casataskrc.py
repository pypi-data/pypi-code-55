import os as _os
import time as _time
##
## path to log file
##
logfile=_os.path.join(_os.getcwd( ),'casa-'+_time.strftime("%Y%m%d-%H%M%S",_time.gmtime())+'.log')
