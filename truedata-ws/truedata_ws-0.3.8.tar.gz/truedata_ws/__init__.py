from . import websocket

import sys
import subprocess
from colorama import init, Style, Fore

from distutils import version

init()

__version__ = '0.3.8'

try:
    op = subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'truedata_ws=='], capture_output=True)
    latest_version = max([version.StrictVersion(i.strip()) for i in str(op.stderr).split('from versions:')[1].split(')')[0].split(',')])
    if latest_version > version.StrictVersion(__version__):
        print(f"{Style.BRIGHT}{Fore.GREEN}\tThere is a newer version of this library available ({latest_version}), while your version is {__version__}...\n"
              f"\tIt is highly advisable that you keep your libraries up-to-date... Please upgrade your library using-\n"
              f"\n\t\t python3.7 -m pip install --upgrade truedata_ws{Style.RESET_ALL}\n")
except Exception as e:
    print(f'{Style.BRIGHT}{Fore.RED}\tUnable to get latest version from PyPi...\n'
          f'\tPlease report this error to truedata...\n'  # TODO: If no error reported within a month, add this -  or raise an issue on https://github.com/paritoshjchandran/truedata/issues/new
          f'\tAlong with the following information - {e}...{Style.RESET_ALL}')
