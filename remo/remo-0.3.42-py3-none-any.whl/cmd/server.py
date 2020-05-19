import logging
import os
from multiprocessing import Process
import atexit

from .config import Config
from .killer import is_port_in_use, try_to_terminate_another_remo_app, terminate_electron_app, kill_ui_process


def delayed_browse(config, debug=False):
    if config.viewer == 'electron':
        from .viewer.electron import browse
    else:
        from .viewer.browser import browse

    url = build_url(config)
    browse(url, debug)


def build_url(config, initial_page='datasets'):
    page = initial_page.strip('/')
    return '{}/{}/'.format(config.get_host_address(), page)


def run_server(config, debug=False):
    debug = debug or config.debug
    if debug:
        os.environ['DJANGO_DEBUG'] = 'True'
    from remo_app.config.standalone.wsgi import application

    if config.is_local_server() and is_port_in_use(config.port):
        print('Failed to start remo-app, port {} already in use.'.format(config.port))

        ok = try_to_terminate_another_remo_app(config)
        if not ok:
            print('You can change default port in config file: {}'.format(Config.path()))
            return
    else:
        terminate_electron_app()

    if config.is_local_server():
        ui_process = Process(target=delayed_browse, args=(config, debug), daemon=True)
        ui_process.start()

        atexit.register(kill_ui_process, ui_process)
        start_server(application, config.port)

    else:
        print('Remo is running on remote server:', config.get_host_address())
        delayed_browse(config, debug)


def start_server(application, port: str = Config.default_port):
    from waitress import serve

    logging.basicConfig()
    logger = logging.getLogger('waitress')
    logger.setLevel(logging.ERROR)

    print('Serving on http://localhost:{}'.format(port))
    serve(application, _quiet=True, port=port, threads=3)
