import sys
from .websocket import tests
from . import __version__

if sys.argv[1] == 'run_all_tests':
    print(f'Running all tests on version = {__version__}')
    username = sys.argv[2]
    password = sys.argv[3]
    live_port = None
    hist_port = None
    symbols = None
    try:
        for arg in sys.argv[4:]:
            if arg[:2] == "--":
                arg_split = arg[2:].split('=')
                arg_key = arg_split[0]
                arg_value = arg_split[1]
                if arg_key.lower() == 'liveport':
                    live_port = int(arg_value)
                if arg_key.lower() == 'histport':
                    hist_port = int(arg_value)
                if arg_key.lower() == 'symbols':
                    symbols = arg_value.split()
                    symbols = [symbol.strip() for symbol in symbols]
    except IndexError:
        pass
    tests.run_all_tests(username, password, live_port, hist_port, symbols)
